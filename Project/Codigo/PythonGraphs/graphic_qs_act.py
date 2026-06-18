"""Cambio de participación y tiempo medio por actividad, 2003-2024."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from eut_common import ACTIVITY_LABELS, MAIN_TIME_COLS
from eut_statistics import effective_sample_size, weighted_mean
from graph_style import QUADRANT_COLORS


def _weighted_variance(values, weights):
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)

    valid = (
        np.isfinite(values)
        & np.isfinite(weights)
        & (weights > 0)
    )
    values = values[valid]
    weights = weights[valid]

    if values.size < 2:
        return np.nan

    mean = np.average(values, weights=weights)
    return np.average((values - mean) ** 2, weights=weights)


def _activity_statistics(data, variable):
    working = data[
        [variable, "factor_elevacion"]
    ].dropna()

    working = working[
        working["factor_elevacion"] > 0
    ]

    values = working[variable].to_numpy(dtype=float)
    weights = working["factor_elevacion"].to_numpy(dtype=float)
    participants = values > 0

    n_effective = effective_sample_size(weights)
    population_mean = weighted_mean(values, weights)
    participation = weighted_mean(participants, weights)

    mean_se = np.sqrt(
        _weighted_variance(values, weights) / n_effective
    )

    participation_se = np.sqrt(
        participation * (1 - participation) / n_effective
    )

    participant_values = values[participants]
    participant_weights = weights[participants]

    return {
        "media_poblacional": population_mean,
        "se_media_poblacional": mean_se,
        "participacion_pct": 100 * participation,
        "se_participacion_pct": 100 * participation_se,
        "media_participantes": (
            weighted_mean(participant_values, participant_weights)
            if participants.any()
            else np.nan
        ),
        "n_muestra": len(working),
        "n_efectivo": n_effective,
    }


def _classify_change(row):
    more_minutes = row["cambio_media_min"] >= 0
    more_participation = row["cambio_participacion_pp"] >= 0

    if more_minutes and more_participation:
        return "Más minutos y más participación"
    if more_minutes:
        return "Más minutos y menos participación"
    if more_participation:
        return "Menos minutos y más participación"
    return "Menos minutos y menos participación"


def build_change_data(
    data,
    start_year=2003,
    end_year=2024,
):
    rows = []

    for variable in MAIN_TIME_COLS:
        for year in [start_year, end_year]:
            group = data[data["encuesta_year"].eq(year)]

            rows.append({
                "variable": variable,
                "actividad": ACTIVITY_LABELS[variable],
                "encuesta_year": year,
                **_activity_statistics(group, variable),
            })

    long_data = pd.DataFrame(rows)

    index_columns = ["variable", "actividad"]

    values = [
        "media_poblacional",
        "se_media_poblacional",
        "participacion_pct",
        "se_participacion_pct",
        "media_participantes",
        "n_muestra",
        "n_efectivo",
    ]

    wide = long_data.pivot(
        index=index_columns,
        columns="encuesta_year",
        values=values,
    )

    wide.columns = [
        f"{metric}_{year}"
        for metric, year in wide.columns
    ]
    wide = wide.reset_index()

    wide["cambio_media_min"] = (
        wide[f"media_poblacional_{end_year}"]
        - wide[f"media_poblacional_{start_year}"]
    )

    wide["cambio_participacion_pp"] = (
        wide[f"participacion_pct_{end_year}"]
        - wide[f"participacion_pct_{start_year}"]
    )

    wide["cambio_media_participantes_min"] = (
        wide[f"media_participantes_{end_year}"]
        - wide[f"media_participantes_{start_year}"]
    )

    # Intervalos aproximados del 95 % para diferencias entre encuestas.
    wide["se_cambio_media"] = np.sqrt(
        wide[f"se_media_poblacional_{start_year}"] ** 2
        + wide[f"se_media_poblacional_{end_year}"] ** 2
    )

    wide["se_cambio_participacion"] = np.sqrt(
        wide[f"se_participacion_pct_{start_year}"] ** 2
        + wide[f"se_participacion_pct_{end_year}"] ** 2
    )

    wide["ic95_media"] = 1.96 * wide["se_cambio_media"]
    wide["ic95_participacion"] = (
        1.96 * wide["se_cambio_participacion"]
    )

    wide["tipo_cambio"] = wide.apply(
        _classify_change,
        axis=1,
    )

    return wide

def create_change_figure(change_data):
    figure = go.Figure()

    for change_type, color in QUADRANT_COLORS.items():
        subset = change_data[
            change_data["tipo_cambio"].eq(change_type)
        ]

        customdata = np.column_stack([
            subset["media_poblacional_2003"],
            subset["media_poblacional_2024"],
            subset["participacion_pct_2003"],
            subset["participacion_pct_2024"],
            subset["media_participantes_2003"],
            subset["media_participantes_2024"],
            subset["cambio_media_participantes_min"],
            subset["n_efectivo_2003"],
            subset["n_efectivo_2024"],
        ])

        figure.add_trace(go.Scatter(
            x=subset["cambio_participacion_pp"],
            y=subset["cambio_media_min"],
            mode="markers+text",
            name=change_type,
            text=subset["actividad"],
            textposition="top center",
            textfont={"size": 11},
            marker={
                "size": 15,
                "color": color,
                "line": {
                    "color": "#FFFFFF",
                    "width": 1.5,
                },
            },
            customdata=customdata,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Cambio participación: %{x:+.2f} pp<br>"
                "Cambio media poblacional: %{y:+.2f} min/día<br>"
                "<br><b>Media poblacional</b><br>"
                "2003: %{customdata[0]:.1f} min<br>"
                "2024: %{customdata[1]:.1f} min<br>"
                "<br><b>Participación</b><br>"
                "2003: %{customdata[2]:.1f}%<br>"
                "2024: %{customdata[3]:.1f}%<br>"
                "<br><b>Media entre participantes</b><br>"
                "2003: %{customdata[4]:.1f} min<br>"
                "2024: %{customdata[5]:.1f} min<br>"
                "Cambio: %{customdata[6]:+.1f} min<br>"
                "<br>n efectivo 2003: %{customdata[7]:,.0f}<br>"
                "n efectivo 2024: %{customdata[8]:,.0f}"
                "<extra></extra>"
            ),
        ))

    figure.add_vline(
        x=0,
        line_color="#7A8A93",
        line_width=1.2,
        line_dash="dash",
    )

    figure.add_hline(
        y=0,
        line_color="#7A8A93",
        line_width=1.2,
        line_dash="dash",
    )

    figure.update_layout(
        title={
            "text": (
                "Cambio en el uso del tiempo, 2003-2024"
                "<br><sup>Variación de los minutos diarios y "
                "de la participación por actividad principal</sup>"
            ),
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 25,
                "color": "#0D1826",
            },
        },
        height=760,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={
            "family": "Arial, sans-serif",
            "color": "#0D1826",
        },
        xaxis={
            "title": "Cambio de participación (puntos porcentuales)",
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        yaxis={
            "title": "Cambio de la media poblacional (minutos diarios)",
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        legend={
            "orientation": "h",
            "x": 0,
            "y": 1.06,
            "xanchor": "left",
            "yanchor": "bottom",
        },
        margin={
            "l": 90,
            "r": 50,
            "t": 170,
            "b": 100,
        },
        hoverlabel={
            "bgcolor": "#FFFFFF",
            "font_size": 13,
        },
    )

    return figure