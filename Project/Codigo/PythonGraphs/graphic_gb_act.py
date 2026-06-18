"""Motor común para columnas agrupadas de subcategorías."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from eut_statistics import effective_sample_size, weighted_mean
from graph_style import SEX_ORDER, YEAR_ORDER, DEFAULT_COLORS, YEAR_COLORS


def group_stats(group, variable):
    working = group[[variable, "factor_elevacion"]].dropna()
    working = working[working["factor_elevacion"] > 0]
    values = working[variable].to_numpy(dtype=float)
    weights = working["factor_elevacion"].to_numpy(dtype=float)
    participants = values > 0
    return {
        "media_poblacional_min": weighted_mean(values, weights),
        "participacion_pct": 100 * weighted_mean(participants, weights),
        "media_participantes_min": (
            weighted_mean(values[participants], weights[participants])
            if participants.any() else np.nan
        ),
        "n_muestra": len(working),
        "n_participantes": int(participants.sum()),
        "n_efectivo": effective_sample_size(weights),
        "poblacion_representada": weights.sum(),
    }


def build_grouped_activity_data(data, activities):
    rows = []
    for year in YEAR_ORDER:
        year_data = data[data["encuesta_year"].eq(year)]
        for variable, activity in activities.items():
            row = {
                "encuesta_year": year,
                "variable": variable,
                "actividad": activity,
                **group_stats(year_data, variable),
            }
            for sex in SEX_ORDER:
                stats = group_stats(year_data[year_data["sexo"].eq(sex)], variable)
                suffix = "hombres" if sex == "Hombre" else "mujeres"
                row[f"media_{suffix}_min"] = stats["media_poblacional_min"]
                row[f"participacion_{suffix}_pct"] = stats["participacion_pct"]
                row[f"media_participantes_{suffix}_min"] = stats["media_participantes_min"]
                row[f"n_{suffix}"] = stats["n_muestra"]
                row[f"n_efectivo_{suffix}"] = stats["n_efectivo"]

            sample = row["n_hombres"] + row["n_mujeres"]
            row["muestra_hombres_pct"] = 100 * row["n_hombres"] / sample
            row["muestra_mujeres_pct"] = 100 * row["n_mujeres"] / sample
            rows.append(row)

    result = pd.DataFrame(rows)
    assert len(result) == len(YEAR_ORDER) * len(activities)
    return result


def create_grouped_activity_figure(summary, activities, title, colors=None, max_y_range=None):
    labels = list(activities.values())
    colors = colors or dict(zip(labels, DEFAULT_COLORS))
    figure = go.Figure()

    for year in YEAR_ORDER:
        subset = (
            summary[summary["encuesta_year"].eq(year)]
            .set_index("actividad")
            .reindex(labels)
            .reset_index()
        )

        customdata = np.column_stack([
            subset["participacion_pct"],
            subset["media_participantes_min"],
            subset["media_hombres_min"],
            subset["media_mujeres_min"],
            subset["participacion_hombres_pct"],
            subset["participacion_mujeres_pct"],
            subset["media_participantes_hombres_min"],
            subset["media_participantes_mujeres_min"],
            subset["muestra_hombres_pct"],
            subset["muestra_mujeres_pct"],
            subset["n_muestra"],
            subset["n_participantes"],
            subset["n_efectivo"],
            subset["poblacion_representada"],
        ])

        figure.add_trace(
            go.Bar(
                x=subset["actividad"],
                y=subset["media_poblacional_min"],
                name=str(year),
                marker={
                    "color": YEAR_COLORS[year],
                },
                customdata=customdata,
                hovertemplate=(
                    f"<b>{year}</b><br>"
                    "Subcategoria: %{x}<br>"
                    "Media poblacional: %{y:.2f} min/dia<br>"
                    "Participacion total: %{customdata[0]:.2f}%<br>"
                    "Media entre participantes: %{customdata[1]:.1f} min/dia<br>"
                    "<br><b>Hombres</b><br>"
                    "Media poblacional: %{customdata[2]:.2f} min/dia<br>"
                    "Participacion: %{customdata[4]:.2f}%<br>"
                    "Media entre participantes: %{customdata[6]:.1f} min/dia<br>"
                    "<br><b>Mujeres</b><br>"
                    "Media poblacional: %{customdata[3]:.2f} min/dia<br>"
                    "Participacion: %{customdata[5]:.2f}%<br>"
                    "Media entre participantes: %{customdata[7]:.1f} min/dia<br>"
                    "<br><b>Base estadistica</b><br>"
                    "Muestra por sexo - H: %{customdata[8]:.1f}% · "
                    "M: %{customdata[9]:.1f}%<br>"
                    "Muestra total: %{customdata[10]:,.0f}<br>"
                    "Participantes muestrales: %{customdata[11]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[12]:,.0f}<br>"
                    "Poblacion representada: %{customdata[13]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )


    yaxis_params ={
            "title": "Minutos diarios",
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
    }
    if not max_y_range:
        yaxis_params[ "rangemode"] = "tozero"
    else:
        yaxis_params[ "range"] = [0, max_y_range]

    figure.update_layout(
        barmode="group",
        bargap=0.20,
        bargroupgap=0.06,
        title={
            "text": title,
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 25, "color": "#0D1826"},
        },
        height=680,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Arial, sans-serif", "color": "#0D1826"},
        legend={
            "orientation": "h",
            "x": 0.6,
            "y": 1.07,
            "xanchor": "left",
            "yanchor": "bottom",
            "title": {"text": ""},
        },
        xaxis={
            "title": "",
            "type": "category",
            "categoryorder": "array",
            "categoryarray": labels,
            "showgrid": False,
        },
        yaxis={**yaxis_params},
        margin={"l": 80, "r": 35, "t": 145, "b": 85},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )

    figure.add_annotation(
        text=(
            "Las columnas incluyen a toda la poblacion. "
            "Consulte el tooltip para separar participacion e intensidad entre participantes."
        ),
        xref="paper",
        yref="paper",
        x=0,
        y=-0.13,
        showarrow=False,
        xanchor="left",
        font={"size": 12, "color": "#4B535C"},
    )

    return figure