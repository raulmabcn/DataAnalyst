"""Matriz de cambio en la ocupacion por sexo y grupo de edad."""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

from eut_statistics import effective_sample_size, weighted_mean
from graph_style import (
    AGE_ORDER,
    SEX_ORDER,
    BACKGROUND_COLOR,
    MUTED_COLOR,
    TEXT_COLOR,
    configure_theme,
)

START_YEAR = 2003
END_YEAR = 2024
WORK_STATUS = "Ocupado"


def summarize_group(group):
    working = group[["situacion_laboral", "factor_elevacion"]].dropna()
    working = working[working["factor_elevacion"] > 0]
    occupied = working["situacion_laboral"].eq(WORK_STATUS).to_numpy(dtype=float)
    weights = working["factor_elevacion"].to_numpy(dtype=float)
    return {
        "pct_ocupados": 100 * weighted_mean(occupied, weights),
        "n_muestra": len(working),
        "n_efectivo": effective_sample_size(weights),
    }


def build_data(data):
    rows = []
    for year in [START_YEAR, END_YEAR]:
        year_data = data[data["encuesta_year"].eq(year)]
        for sex in SEX_ORDER:
            for age in AGE_ORDER:
                group = year_data[
                    year_data["sexo"].eq(sex) & year_data["tramo_edad"].eq(age)
                ]
                rows.append({
                    "encuesta_year": year,
                    "sexo": sex,
                    "tramo_edad": age,
                    **summarize_group(group),
                })

    result = pd.DataFrame(rows)
    wide = (
        result.pivot_table(
            index=["sexo", "tramo_edad"],
            columns="encuesta_year",
            values=["pct_ocupados", "n_muestra", "n_efectivo"],
            observed=True,
        )
        .sort_index(axis=1)
    )
    wide.columns = [f"{metric}_{year}" for metric, year in wide.columns]
    wide = wide.reset_index()
    wide["diferencia_pp"] = (
        wide[f"pct_ocupados_{END_YEAR}"] - wide[f"pct_ocupados_{START_YEAR}"]
    )

    expected_rows = len(SEX_ORDER) * len(AGE_ORDER)
    assert len(wide) == expected_rows
    return wide


def create_figure(summary):
    configure_theme()

    matrix = (
        summary.pivot(index="sexo", columns="tramo_edad", values="diferencia_pp")
        .reindex(index=SEX_ORDER, columns=AGE_ORDER)
    )
    annotations = matrix.map(lambda value: f"{value:+.1f} pp")
    abs_limit = np.nanmax(np.abs(matrix.to_numpy(dtype=float)))
    cmap = LinearSegmentedColormap.from_list(
        "employment_change",
        ["#B45D7A", "#F6F3EE", "#3E8E63"],
    )

    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    sns.heatmap(
        matrix,
        ax=ax,
        cmap=cmap,
        center=0,
        vmin=-abs_limit,
        vmax=abs_limit,
        annot=annotations,
        fmt="",
        linewidths=1.2,
        linecolor=BACKGROUND_COLOR,
        cbar=False,
    )

    ax.set_title(
        "Cambio en la proporcion de personas ocupadas 2024 - 2003",
        loc="left",
        fontsize=16,
        pad=16,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="x", rotation=0)
    ax.tick_params(axis="y", rotation=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.text(
        0.125,
        0.02,
        (
            "Diferencia en puntos porcentuales del peso de personas ocupadas "
            "dentro de cada grupo. Estimaciones ponderadas."
        ),
        fontsize=9,
        color=MUTED_COLOR,
    )
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    return fig
