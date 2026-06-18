"""Evolución de subcategorías de cuidados personales por sexo y edad."""
from graph_style import ( 
    AGE_ORDER, SEX_ORDER, YEAR_ORDER, BACKGROUND_COLOR, GRID_COLOR, MUTED_COLOR, TEXT_COLOR, AGE_COLORS, configure_theme
    )
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PERSONAL_CARE = {'min_cp_dormir': 'Dormir', 'min_cp_comer_beber': 'Comer y beber', 'min_cp_higiene_salud': 'Higiene y salud'}

def weighted_mean_summary(group, value, weight="factor_elevacion"):
    valid = group[[value, weight]].dropna()
    valid = valid[valid[weight] > 0]

    values = valid[value].to_numpy(dtype=float)
    weights = valid[weight].to_numpy(dtype=float)

    return pd.Series({
        "media_ponderada": np.average(values, weights=weights),
        "n_muestra": len(valid),
        "n_efectivo": weights.sum() ** 2 / np.square(weights).sum(),
    })


def build_data(data):
    frames = []

    groups = ["encuesta_year", "sexo", "tramo_edad"]

    for variable, label in PERSONAL_CARE.items():
        summary = (
            data.groupby(groups, observed=True)
            .apply(
                lambda group: weighted_mean_summary(group, variable),
                include_groups=False,
            )
            .reset_index()
        )

        summary["variable"] = variable
        summary["subcategoria"] = label
        frames.append(summary)

    result = pd.concat(frames, ignore_index=True)
    result["encuesta_year"] = result["encuesta_year"].astype(int)

    expected = (
        len(PERSONAL_CARE)
        * len(SEX_ORDER)
        * len(AGE_ORDER)
        * len(YEAR_ORDER)
    )

    assert len(result) == expected, (
        f"Se esperaban {expected} estimaciones "
        f"y se obtuvieron {len(result)}."
    )
    assert result["media_ponderada"].notna().all(), (
        "Existen estimaciones ausentes."
    )

    return result


def create_chart(result):
    configure_theme()

    fig, axes = plt.subplots(
        nrows=3,
        ncols=2,
        figsize=(14, 13),
        sharex=True,
        sharey="row",
    )

    for row, (variable, subcategory) in enumerate(
        PERSONAL_CARE.items()
    ):
        category_data = result[result["variable"].eq(variable)]
        lower = max(0, category_data["media_ponderada"].min())
        upper = category_data["media_ponderada"].max()
        margin = max((upper - lower) * 0.18, 4)

        for column, sex in enumerate(SEX_ORDER):
            ax = axes[row, column]
            sex_data = category_data[
                category_data["sexo"].eq(sex)
            ]

            for age in AGE_ORDER:
                age_data = (
                    sex_data[sex_data["tramo_edad"].eq(age)]
                    .sort_values("encuesta_year")
                )

                ax.plot(
                    age_data["encuesta_year"],
                    age_data["media_ponderada"],
                    color=AGE_COLORS[age],
                    marker="o",
                    markersize=6.5,
                    linewidth=2.2,
                    alpha=0.95,
                    label=age,
                )

            if row == 0:
                ax.set_title(sex, fontsize=16, pad=14)

            if column == 0:
                ax.set_ylabel(
                    f"{subcategory}\nMinutos al día",
                    fontsize=11,
                )
            else:
                ax.set_ylabel("")

            ax.set_xticks(YEAR_ORDER)
            ax.set_xlim(2001.5, 2025.5)
            ax.set_ylim(
                max(0, lower - margin * 0.25),
                upper + margin,
            )

            ax.grid(
                axis="y",
                color=GRID_COLOR,
                linestyle="--",
                linewidth=0.8,
                alpha=0.75,
            )
            ax.grid(axis="x", visible=False)
            ax.spines[["top", "right", "left"]].set_visible(False)
            ax.tick_params(axis="y", length=0)

    handles, labels = axes[0, 0].get_legend_handles_labels()

    fig.legend(
        handles,
        labels,
        title="Tramo de edad",
        loc="upper right",
        bbox_to_anchor=(0.95, 0.98),
        ncols=2,
        frameon=False,
    )

    fig.suptitle(
        "Evolución de los cuidados personales por sexo y edad",
        x=0.06,
        y=0.985,
        ha="left",
        fontsize=20,
        fontweight="bold",
        color=TEXT_COLOR,
    )

    fig.text(
        0.06,
        0.015,
        "Las líneas conectan tres encuestas transversales "
        "y no representan seguimiento individual.",
        fontsize=9,
        color=MUTED_COLOR,
    )

    fig.patch.set_facecolor(BACKGROUND_COLOR)

    plt.tight_layout(
        rect=[0.05, 0.045, 0.99, 0.94],
        h_pad=2.5,
        w_pad=2.5,
    )

    return fig