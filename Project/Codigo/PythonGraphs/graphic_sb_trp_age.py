"""Trayectos por finalidad, edad y año, incluyendo residual sin clasificar."""
from graph_style import ( 
    AGE_ORDER, YEAR_ORDER, BACKGROUND_COLOR, GRID_COLOR, MUTED_COLOR, TEXT_COLOR, TRAVEL_COLORS, configure_theme
    )

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from eut_common import  weighted_group_mean

TRAVEL_CATEGORIES = {'min_tray_trabajo': 'Trabajo', 'min_tray_estudios': 'Estudios', 'min_tray_hogar_familia': 'Hogar y familia', 'min_tray_voluntariado': 'Voluntariado', 'min_tray_vida_social': 'Vida social', 'min_tray_otro_ocio': 'Deporte y otro ocio', 'min_tray_cambio_municipio': 'Cambio de municipio', 'min_tray_otros_no_especificado': 'Otros no especificados'}

def add_residual(data):
    result = data.copy()
    classified_columns = [column for column in TRAVEL_CATEGORIES ]
    classified_sum = result[classified_columns].sum(axis=1)
    residual = result['min_trayectos_noespec'] - classified_sum
    assert residual.min() >= -1e-08, 'La suma de subcategorías supera el total de trayectos en alguna fila.'
    result['min_trayectos_noespec'] = result['min_trayectos_noespec'] + residual.clip(lower=0)
    return result

def build_summary(data):
    rows = []
    for variable, label in TRAVEL_CATEGORIES.items():
        summary = weighted_group_mean(data, value=variable, groups=['encuesta_year', 'tramo_edad'])
        summary['variable'] = variable
        summary['finalidad'] = label
        rows.append(summary)
    result = pd.concat(rows, ignore_index=True)
    result['encuesta_year'] = result['encuesta_year'].astype(int)
    expected = len(TRAVEL_CATEGORIES) * len(AGE_ORDER) * len(YEAR_ORDER)
    assert len(result) == expected
    assert result['media_ponderada'].notna().all()
    return result

def build_change_table(summary):
    changes = summary[summary['encuesta_year'].isin([2003, 2024])].pivot_table(index=['tramo_edad', 'variable', 'finalidad'], columns='encuesta_year', values='media_ponderada', observed=True).reset_index()
    changes['cambio_2003_2024'] = changes[2024] - changes[2003]
    changes['cambio_pct'] = np.where(changes[2003].ne(0), 100 * changes['cambio_2003_2024'] / changes[2003], np.nan)
    age_rank = {age: index for index, age in enumerate(AGE_ORDER)}
    category_rank = {label: index for index, label in enumerate(TRAVEL_CATEGORIES.values())}
    changes['_age_rank'] = changes['tramo_edad'].map(age_rank)
    changes['_category_rank'] = changes['finalidad'].map(category_rank)
    return changes.sort_values(['_age_rank', '_category_rank']).drop(columns=['_age_rank', '_category_rank']).reset_index(drop=True)

def create_chart(summary):
    configure_theme()
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), sharex=True, sharey=True)
    axes = axes.flatten()

    category_order = (
        summary.groupby("finalidad", observed=True)["media_ponderada"]
        .sum()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    total_by_panel = summary.groupby(
        ["encuesta_year", "tramo_edad"], observed=True
    )["media_ponderada"].sum()
    y_max = total_by_panel.max() * 1.2

    for ax, age in zip(axes, AGE_ORDER):
        subset = (
            summary[summary["tramo_edad"].eq(age)]
            .pivot(
                index="encuesta_year",
                columns="finalidad",
                values="media_ponderada",
            )
            .reindex(index=YEAR_ORDER, columns=category_order)
            .fillna(0)
        )

        x = np.arange(len(YEAR_ORDER))
        bottom = np.zeros(len(YEAR_ORDER))

        for category in category_order:
            values = subset[category].to_numpy()
            ax.bar(
                x,
                values,
                bottom=bottom,
                width=0.62,
                color=TRAVEL_COLORS[category],
                edgecolor=BACKGROUND_COLOR,
                linewidth=0.7,
                label=category,
            )
            bottom += values

        for position, total in zip(x, bottom):
            ax.text(
                position,
                total + y_max * 0.025,
                f"{total:.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=TEXT_COLOR,
            )

        ax.set_title(age, loc="left", fontsize=15, pad=14)
        ax.set_xticks(x)
        ax.set_xticklabels(YEAR_ORDER)
        ax.set_ylim(0, y_max)
        ax.set_xlabel("")
        ax.set_ylabel("Minutos al día")
        ax.set_axisbelow(True)
        ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.75)
        ax.grid(axis="x", visible=False)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.91),
        ncols=4,
        frameon=False,
    )
    fig.suptitle(
        "Tiempo de trayectos por finalidad y edad",
        x=0.06,
        y=0.985,
        ha="left",
        fontsize=20,
        fontweight="bold",
        color=TEXT_COLOR,
    )
    fig.text(
        0.06,
        0.94,
        "Medias diarias ponderadas · La cifra superior indica el total medio de trayectos",
        fontsize=11,
        color=MUTED_COLOR,
    )
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    plt.tight_layout(rect=[0.05, 0.05, 0.99, 0.86], h_pad=3, w_pad=2.5)

    return fig