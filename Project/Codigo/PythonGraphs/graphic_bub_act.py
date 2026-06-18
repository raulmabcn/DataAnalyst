"""Gráfico interactivo temporal: intensidad y participación por actividad."""
import pandas as pd
import plotly.express as px
from eut_common import ACTIVITY_LABELS, MAIN_TIME_COLS, weighted_activity_summary
from graph_style import ACTIVITY_COLORS, AGE_ORDER

AGE_SUFFIXES = {
    "10-24 años": "10_24",
    "25-44 años": "25_44",
    "45-64 años": "45_64",
    "65 o más": "65_mas",
}


def build_age_profile(data, activity):
    rows = []
    for year, group in data.groupby("encuesta_year", observed=True):
        valid = group[[activity, "tramo_edad", "factor_elevacion"]].dropna()
        valid = valid[valid["factor_elevacion"] > 0]
        participants = valid[valid[activity] > 0]
        weights = (
            participants.groupby("tramo_edad", observed=True)["factor_elevacion"]
            .sum()
        )
        total = weights.sum()
        row = {"encuesta_year": int(year)}
        for age in AGE_ORDER:
            suffix = AGE_SUFFIXES[age]
            row[f"pct_{suffix}"] = 100 * weights.get(age, 0) / total if total else 0
        rows.append(row)
    return pd.DataFrame(rows)

def build_bubble_data(data):
    frames = []
    for activity in MAIN_TIME_COLS:
        summary = weighted_activity_summary(data, activity)
        summary = summary.merge(
            build_age_profile(data, activity),
            on="encuesta_year",
            how="left",
        )
        summary['actividad_codigo'] = activity
        summary['actividad'] = summary['actividad_codigo'].map(ACTIVITY_LABELS)
        frames.append(summary)
    result = pd.concat(frames, ignore_index=True)
    result['encuesta_year'] = result['encuesta_year'].astype(int)
    result['media_poblacion'] = result['media_poblacion'].astype(float)
    result['media_participantes'] = result['media_participantes'].astype(float)
    result['participacion_pct'] = result['participacion_pct'].astype(float)
    expected_rows = len(MAIN_TIME_COLS) * 3
    assert len(result) == expected_rows, f'Se esperaban {expected_rows} combinaciones actividad-año y se obtuvieron {len(result)}.'
    assert result[['media_poblacion', 'media_participantes', 'participacion_pct']].notna().all().all(), 'Hay indicadores ausentes en los datos del gráfico.'
    assert result['participacion_pct'].between(0, 100).all(), 'La participación debe estar comprendida entre 0 y 100.'
    return result

def create_bubble_chart(bubble_data):
    activity_order = [
        ACTIVITY_LABELS[column]
        for column in MAIN_TIME_COLS
    ][::-1]

    x_max = bubble_data["media_participantes"].max() * 1.12

    figure = px.scatter(
        bubble_data,
        x="media_participantes",
        y="actividad",
        animation_frame="encuesta_year",
        animation_group="actividad_codigo",
        size="participacion_pct",
        color="actividad",
        color_discrete_map=ACTIVITY_COLORS,
        category_orders={
            "actividad": activity_order,
            "encuesta_year": [2003, 2011, 2024],
        },
        hover_name="actividad",
        hover_data={
            "encuesta_year": True,
            "media_participantes": ":.1f",
            "participacion_pct": ":.1f",
            "media_poblacion": ":.1f",
            "n_muestra": ":,.0f",
            "n_efectivo": ":,.0f",
            "actividad_codigo": False,
            "actividad": False,
        },
        labels={
            "encuesta_year": "Año",
            "media_participantes": "Minutos entre participantes",
            "participacion_pct": "Participación ponderada (%)",
            "media_poblacion": "Media poblacional (minutos)",
            "n_muestra": "Muestra",
            "n_efectivo": "Muestra efectiva",
            "actividad": "Actividad principal",
        },
        size_max=48,
        range_x=[0, x_max],
        title=(
            "Intensidad y participación en las "
            "actividades principales"
        ),
        template="plotly_white",
    )

    figure.update_traces(
        marker={
            "line": {
                "color": "#FFFFFF",
                "width": 1.5,
            },
            "opacity": 0.88,
        }
    )

    figure.update_layout(
        height=720,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={
            "family": "Arial, sans-serif",
            "color": "#0D1826",
        },
        title={
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 25,
                "color": "#0D1826",
            },
            "subtitle": {
                "text": (
                    "Posición: minutos medios entre participantes · "
                    "Tamaño: porcentaje ponderado que realiza "
                    "la actividad"
                ),
                "font": {
                    "size": 14,
                    "color": "#4B535C",
                },
            },
        },
        xaxis={
            "title": (
                "Minutos diarios entre quienes realizan "
                "la actividad"
            ),
            "range": [0, x_max],
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dot",
            "zeroline": False,
        },
        yaxis={
            "title": "",
            "categoryorder": "array",
            "categoryarray": activity_order,
            "showgrid": True,
            "gridcolor": "#E5E8EA",
            "griddash": "dot",
            "gridwidth": 0.7,
            "zeroline": False,
        },
        showlegend=False,
        margin={
            "l": 190,
            "r": 40,
            "t": 115,
            "b": 180,
        },
        hoverlabel={
            "bgcolor": "#FFFFFF",
            "font_size": 13,
        },
    )

    if figure.layout.updatemenus:
        play_button = figure.layout.updatemenus[0].buttons[0]
        play_button.args[1]["frame"]["duration"] = 900
        play_button.args[1]["transition"]["duration"] = 500

    figure.add_annotation(
        text=(
            "La media de participantes se calcula únicamente "
            "entre personas con más de 0 minutos en la actividad."
        ),
        xref="paper",
        yref="paper",
        x=-0.10,
        y=-0.35,
        xanchor="left",
        yanchor="top",
        showarrow=False,
        font={
            "size": 12,
            "color": "#4B535C",
        },
    )

    return figure
