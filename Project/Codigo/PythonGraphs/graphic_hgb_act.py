"""Barras horizontales agrupadas: minutos entre participantes por actividad."""

import plotly.graph_objects as go

from eut_common import ACTIVITY_LABELS, MAIN_TIME_COLS
from graph_style import YEAR_COLORS, YEAR_ORDER


def create_figure(summary):
    activity_order = [
        ACTIVITY_LABELS[column]
        for column in MAIN_TIME_COLS
    ]
    category_order = activity_order[::-1]
    figure = go.Figure()

    for year in YEAR_ORDER:
        subset = (
            summary[summary["encuesta_year"].eq(year)]
            .set_index("actividad")
            .reindex(activity_order)
            .reset_index()
        )
        customdata = list(zip(
            subset["participacion_pct"],
            subset["media_poblacion"],
            subset["n_muestra"],
            subset["n_efectivo"],
        ))
        figure.add_trace(
            go.Bar(
                x=subset["media_participantes"],
                y=subset["actividad"],
                orientation="h",
                name=str(year),
                marker={"color": YEAR_COLORS[year]},
                customdata=customdata,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    f"Ano: {year}<br>"
                    "Minutos entre participantes: %{x:.1f}<br>"
                    "Participacion ponderada: %{customdata[0]:.1f}%<br>"
                    "Media poblacional: %{customdata[1]:.1f} min/dia<br>"
                    "Muestra: %{customdata[2]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[3]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

    x_max = summary["media_participantes"].max() * 1.12
    figure.update_layout(
        title={
            "text": (
                "Minutos diarios entre quienes realizan "
                "cada actividad principal"
            ),
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 25, "color": "#0D1826"},
        },
        barmode="group",
        bargap=0.22,
        bargroupgap=0.10,
        height=720,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Arial, sans-serif", "color": "#0D1826"},
        legend={
            "orientation": "h",
            "x": 3.02,
            "y": 1.06,
            "xanchor": "left",
            "yanchor": "bottom",
            "title": {"text": ""},
        },
        xaxis={
            "title": "Minutos diarios entre participantes",
            "range": [0, x_max],
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "categoryorder": "array",
            "categoryarray": category_order,
            "showgrid": False,
        },
        margin={"l": 235, "r": 40, "t": 125, "b": 105},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )
    figure.add_annotation(
        text=(
            "Las barras muestran intensidad entre quienes si realizan la "
            "actividad; el tooltip anade participacion y media sobre el "
            "conjunto de la poblacion."
        ),
        xref="paper",
        yref="paper",
        x=0,
        y=-0.14,
        showarrow=False,
        xanchor="left",
        font={"size": 12, "color": "#4B535C"},
    )
    return figure


def create_figure_participans(summary):
    activity_order = [
        ACTIVITY_LABELS[column]
        for column in MAIN_TIME_COLS
    ]
    category_order = activity_order[::-1]
    figure = go.Figure()

    for year in YEAR_ORDER:
        subset = (
            summary[summary["encuesta_year"].eq(year)]
            .set_index("actividad")
            .reindex(activity_order)
            .reset_index()
        )
        customdata = list(zip(
            subset["media_participantes"],
            subset["media_poblacion"],
            subset["n_muestra"],
            subset["n_efectivo"],
            subset["pct_10_24"],
            subset["pct_25_44"],
            subset["pct_45_64"],
            subset["pct_65_mas"],
        ))
        figure.add_trace(
            go.Bar(
                x=subset["participacion_pct"],
                y=subset["actividad"],
                orientation="h",
                name=str(year),
                marker={"color": YEAR_COLORS[year]},
                customdata=customdata,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    f"Ano: {year}<br>"
                    "Participacion ponderada: %{x:.1f}%<br>"
                    "Minutos diarios participantes: %{customdata[0]:.1f}<br>"
                    "Media poblacional: %{customdata[1]:.1f} min/dia<br>"
                    "Muestra: %{customdata[2]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[3]:,.0f}<br>"
                    "<br><b>Participantes por edad</b><br>"
                    "10-24: %{customdata[4]:.1f}%<br>"
                    "25-44: %{customdata[5]:.1f}%<br>"
                    "45-64: %{customdata[6]:.1f}%<br>"
                    "65 o mas: %{customdata[7]:.1f}%"
                    "<extra></extra>"
                ),
            )
        )

    x_max = summary["participacion_pct"].max() * 1.12
    figure.update_layout(
        title={
            "text": (
                "Porcentaje de participación en cada actividad"
            ),
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 25, "color": "#0D1826"},
        },
        barmode="group",
        bargap=0.22,
        bargroupgap=0.10,
        height=720,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Arial, sans-serif", "color": "#0D1826"},
        legend={
            "orientation": "h",
            "x": 3.02,
            "y": 1.06,
            "xanchor": "left",
            "yanchor": "bottom",
            "title": {"text": ""},
        },
        xaxis={
            "title": "% de participantes",
            "range": [0, x_max],
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "categoryorder": "array",
            "categoryarray": category_order,
            "showgrid": False,
        },
        margin={"l": 235, "r": 40, "t": 125, "b": 105},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )
    
    return figure
