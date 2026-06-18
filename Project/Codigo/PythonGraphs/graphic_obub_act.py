"""Comparación superpuesta 2003-2024 de intensidad y participación."""
import pandas as pd
import plotly.graph_objects as go
from eut_common import ACTIVITY_LABELS, MAIN_TIME_COLS, weighted_activity_summary
from graph_style import YEAR_COLORS, ACTIVITY_COLORS


def build_data(data):
    frames = []
    for activity in MAIN_TIME_COLS:
        summary = weighted_activity_summary(data, activity)
        summary = summary[summary['encuesta_year'].isin([2003, 2024])].copy()
        summary['actividad_codigo'] = activity
        summary['actividad'] = ACTIVITY_LABELS[activity]
        frames.append(summary)
    result = pd.concat(frames, ignore_index=True)
    result['encuesta_year'] = result['encuesta_year'].astype(int)
    result['media_participantes'] = result['media_participantes'].astype(float)
    result['participacion_pct'] = result['participacion_pct'].astype(float)
    assert len(result) == len(MAIN_TIME_COLS) * 2
    assert result.groupby('actividad_codigo')['encuesta_year'].nunique().eq(2).all()
    return result

def marker_sizes(percentages, max_diameter=52):
    """Escala por área: Plotly interpreta size como diámetro."""
    max_value = percentages.max()
    return percentages.pow(0.5) / max_value ** 0.5 * max_diameter

def create_figure(data):
    order = [
        ACTIVITY_LABELS[column]
        for column in MAIN_TIME_COLS
    ][::-1]

    y_positions = {
        activity: index
        for index, activity in enumerate(order)
    }

    data = data.assign(
        marker_size=marker_sizes(data["participacion_pct"])
    )

    figure = go.Figure()

    year_style = {
        2003: {
            "opacity": 0.52,
            "border": YEAR_COLORS[2003],
            "width": 3,
        },
        2024: {
            "opacity": 0.78,
            "border": YEAR_COLORS[2024],
            "width": 3,
        },
    }

    # Burbujas correspondientes a cada actividad y año.
    for year in [2003, 2024]:
        for activity in order:
            row = data[
                data["encuesta_year"].eq(year)
                & data["actividad"].eq(activity)
            ].iloc[0]

            figure.add_trace(
                go.Scatter(
                    x=[row["media_participantes"]],
                    y=[y_positions[activity]],
                    mode="markers",
                    marker={
                        "size": row["marker_size"],
                        "color": ACTIVITY_COLORS[activity],
                        "opacity": year_style[year]["opacity"],
                        "line": {
                            "color": year_style[year]["border"],
                            "width": year_style[year]["width"],
                        },
                    },
                    customdata=[[
                        year,
                        row["participacion_pct"],
                        row["media_poblacion"],
                    ]],
                    hovertemplate=(
                        f"<b>{activity}</b><br>"
                        "Año: %{customdata[0]}<br>"
                        "Minutos entre participantes: %{x:.1f}<br>"
                        "Participación ponderada: "
                        "%{customdata[1]:.1f}%<br>"
                        "Media poblacional: "
                        "%{customdata[2]:.1f} min"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

    # Leyenda específica para diferenciar los años.
    for year in [2003, 2024]:
        figure.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker={
                    "size": 18,
                    "color": "#B8C0C5",
                    "opacity": year_style[year]["opacity"],
                    "line": {
                        "color": year_style[year]["border"],
                        "width": 3,
                    },
                },
                name=str(year),
                hoverinfo="skip",
            )
        )

    x_max = data["media_participantes"].max() * 1.1

    figure.update_layout(
        title={
            "text": (
                "Dedicación y participación: 2003 frente a 2024"
                "<br><sup>Tamaño: porcentaje ponderado · Borde: año</sup>"
            ),
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 25,
                "color": "#0D1826",
            },
        },
        height=720,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={
            "family": "Arial, sans-serif",
            "color": "#0D1826",
        },
        xaxis={
            "title": (
                "Minutos diarios entre quienes realizan "
                "la actividad"
            ),
            "range": [0, x_max],
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "tickmode": "array",
            "tickvals": list(range(len(order))),
            "ticktext": order,
            "range": [-0.65, len(order) - 0.35],
            "showgrid": False,
        },
        legend={
            "orientation": "h",
            "x": 0.7,
            "y": 1.1,
            "xanchor": "left",
            "yanchor": "bottom",
        },
        margin={
            "l": 195,
            "r": 55,
            "t": 135,
            "b": 105,
        },
        hoverlabel={
            "bgcolor": "#FFFFFF",
            "font_size": 13,
        },
    )

    return figure
