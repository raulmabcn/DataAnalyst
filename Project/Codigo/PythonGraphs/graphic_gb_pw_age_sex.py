"""Dos gráficos interactivos del tiempo de trabajo por edad, sexo y año."""
from eut_statistics import effective_sample_size, weighted_mean
from graph_style import AGE_ORDER, SEX_ORDER, YEAR_ORDER
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from graph_style import (
    AGE_COLORS,
    SEX_COLORS,
    YEAR_COLORS
)

def summarize(group):
    working = group[['min_trabajo_remunerado', 'factor_elevacion']].dropna()
    working = working[working['factor_elevacion'] > 0]
    minutes = working['min_trabajo_remunerado'].to_numpy(dtype=float)
    weights = working['factor_elevacion'].to_numpy(dtype=float)
    participants = minutes > 0
    return {'media_poblacional_min': weighted_mean(minutes, weights), 'participacion_pct': 100 * weighted_mean(participants, weights), 'media_participantes_min': weighted_mean(minutes[participants], weights[participants]) if participants.any() else np.nan, 'n_muestra': len(working), 'n_efectivo': effective_sample_size(weights)}

def weighted_composition(group, variable):
    composition = group.groupby(variable, observed=True)['factor_elevacion'].sum()
    return 100 * composition / composition.sum()

def build_age_summary(data):
    rows = []
    for year in YEAR_ORDER:
        for age in AGE_ORDER:
            group = data[data['encuesta_year'].eq(year) & data['tramo_edad'].eq(age)]
            metrics = summarize(group)
            sex_composition = weighted_composition(group, 'sexo')
            rows.append({'encuesta_year': year, 'tramo_edad': age, **metrics, 'pct_hombres_en_grupo': sex_composition.get('Hombre', 0), 'pct_mujeres_en_grupo': sex_composition.get('Mujer', 0)})
    result = pd.DataFrame(rows)
    assert len(result) == len(YEAR_ORDER) * len(AGE_ORDER)
    return result

def build_sex_summary(data):
    rows = []
    for year in YEAR_ORDER:
        for sex in SEX_ORDER:
            group = data[data['encuesta_year'].eq(year) & data['sexo'].eq(sex)]
            metrics = summarize(group)
            age_composition = weighted_composition(group, 'tramo_edad')
            rows.append({'encuesta_year': year, 'sexo': sex, **metrics, **{f'pct_{age}': age_composition.get(age, 0) for age in AGE_ORDER}})
    result = pd.DataFrame(rows)
    assert len(result) == len(YEAR_ORDER) * len(SEX_ORDER)
    return result

def base_layout(figure, title, subtitle, y_max):
    figure.update_layout(
        title={
            "text": f"{title}<br><sup>{subtitle}</sup>",
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 25, "color": "#0D1826"},
        },
        barmode="group",
        bargap=0.22,
        bargroupgap=0.06,
        height=620,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={
            "family": "Arial, sans-serif",
            "color": "#0D1826",
        },
        xaxis={
            "title": "",
            "type": "category",
            "categoryorder": "array",
            "categoryarray": YEAR_ORDER,
            "showgrid": False,
        },
        yaxis={
            "title": "Minutos medios por persona y día",
            "range": [0, y_max],
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        legend={
            "orientation": "h",
            "x": 0.58,
            "y": 1.08,
            "xanchor": "left",
            "yanchor": "bottom",
            "title": {"text": ""},
        },
        margin={"l": 80, "r": 45, "t": 135, "b": 90},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )


def create_age_figure(summary, y_max):
    figure = go.Figure()

    for age in AGE_ORDER:
        subset = (
            summary[summary["tramo_edad"].eq(age)]
            .sort_values("encuesta_year")
        )

        customdata = np.column_stack([
            subset["participacion_pct"],
            subset["media_participantes_min"],
            subset["pct_hombres_en_grupo"],
            subset["pct_mujeres_en_grupo"],
            subset["n_muestra"],
            subset["n_efectivo"],
        ])

        figure.add_trace(
            go.Bar(
                x=subset["encuesta_year"].astype(str),
                y=subset["media_poblacional_min"],
                name=age,
                marker={"color": AGE_COLORS[age]},
                customdata=customdata,
                text=subset["media_poblacional_min"],
                texttemplate="%{text:.0f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    f"<b>{age}</b><br>"
                    "Año: %{x}<br>"
                    "Media poblacional: %{y:.1f} min<br>"
                    "Trabajó ese día: %{customdata[0]:.1f}%<br>"
                    "Media entre quienes trabajaron: "
                    "%{customdata[1]:.1f} min<br>"
                    "Composición del grupo:<br>"
                    "&nbsp;&nbsp;Hombres: "
                    "%{customdata[2]:.1f}%<br>"
                    "&nbsp;&nbsp;Mujeres: "
                    "%{customdata[3]:.1f}%<br>"
                    "Muestra: %{customdata[4]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[5]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

    base_layout(
        figure,
        "Tiempo de trabajo remunerado por grupo de edad",
        (
            "El tooltip muestra la composición por sexo "
            "dentro de cada grupo edad-año"
        ),
        y_max,
    )

    return figure


def create_sex_figure(summary, y_max):
    figure = go.Figure()

    for sex in SEX_ORDER:
        subset = (
            summary[summary["sexo"].eq(sex)]
            .sort_values("encuesta_year")
        )

        age_columns = [
            subset[f"pct_{age}"]
            for age in AGE_ORDER
        ]

        customdata = np.column_stack([
            subset["participacion_pct"],
            subset["media_participantes_min"],
            *age_columns,
            subset["n_muestra"],
            subset["n_efectivo"],
        ])

        figure.add_trace(
            go.Bar(
                x=subset["encuesta_year"].astype(str),
                y=subset["media_poblacional_min"],
                name=sex,
                marker={"color": SEX_COLORS[sex]},
                customdata=customdata,
                text=subset["media_poblacional_min"],
                texttemplate="%{text:.0f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    f"<b>{sex}</b><br>"
                    "Año: %{x}<br>"
                    "Media poblacional: %{y:.1f} min<br>"
                    "Trabajó ese día: %{customdata[0]:.1f}%<br>"
                    "Media entre quienes trabajaron: "
                    "%{customdata[1]:.1f} min<br>"
                    "Composición por edad:<br>"
                    "&nbsp;&nbsp;10-24: "
                    "%{customdata[2]:.1f}%<br>"
                    "&nbsp;&nbsp;25-44: "
                    "%{customdata[3]:.1f}%<br>"
                    "&nbsp;&nbsp;45-64: "
                    "%{customdata[4]:.1f}%<br>"
                    "&nbsp;&nbsp;65 o más: "
                    "%{customdata[5]:.1f}%<br>"
                    "Muestra: %{customdata[6]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[7]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

    base_layout(
        figure,
        "Tiempo de trabajo remunerado por sexo",
        (
            "El tooltip muestra la composición por edad "
            "dentro de cada grupo sexo-año"
        ),
        y_max,
    )

    return figure


def create_year_age_figure(summary, y_max):
    figure = go.Figure()

    for year in YEAR_ORDER:
        subset = (
            summary[summary["encuesta_year"].eq(year)]
            .set_index("tramo_edad")
            .reindex(AGE_ORDER)
            .reset_index()
        )

        customdata = np.column_stack([
            subset["participacion_pct"],
            subset["media_participantes_min"],
            subset["pct_hombres_en_grupo"],
            subset["pct_mujeres_en_grupo"],
            subset["n_muestra"],
            subset["n_efectivo"],
        ])

        figure.add_trace(
            go.Bar(
                x=subset["tramo_edad"],
                y=subset["media_poblacional_min"],
                name=str(year),
                marker={"color": YEAR_COLORS[year]},
                customdata=customdata,
                text=subset["media_poblacional_min"],
                texttemplate="%{text:.0f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    f"<b>{year}</b><br>"
                    "Grupo de edad: %{x}<br>"
                    "Media poblacional: %{y:.1f} min<br>"
                    "Trabajo ese día: %{customdata[0]:.1f}%<br>"
                    "Media entre quienes trabajaron: "
                    "%{customdata[1]:.1f} min<br>"
                    "Composición del grupo:<br>"
                    "&nbsp;&nbsp;Hombres: %{customdata[2]:.1f}%<br>"
                    "&nbsp;&nbsp;Mujeres: %{customdata[3]:.1f}%<br>"
                    "Muestra: %{customdata[4]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[5]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

    base_layout(
        figure,
        "Tiempo de trabajo remunerado por grupo de edad",
        (
            "El tooltip muestra la composición por sexo "
            "dentro de cada grupo edad-año"
        ),
        y_max,
    )

    return figure

def create_year_sex_figure(summary, y_max):
    figure = go.Figure()

    for year in YEAR_ORDER:
        subset = (
            summary[summary["encuesta_year"].eq(year)]
            .set_index("sexo")
            .reindex(SEX_ORDER)
            .reset_index()
        )

        age_columns = [
            subset[f"pct_{age}"]
            for age in AGE_ORDER
        ]

        customdata = np.column_stack([
            subset["participacion_pct"],
            subset["media_participantes_min"],
            *age_columns,
            subset["n_muestra"],
            subset["n_efectivo"],
        ])

        figure.add_trace(
            go.Bar(
                x=subset["sexo"],
                y=subset["media_poblacional_min"],
                name=str(year),
                marker={"color": YEAR_COLORS[year]},
                customdata=customdata,
                text=subset["media_poblacional_min"],
                texttemplate="%{text:.0f}",
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    f"<b>{year}</b><br>"
                    "Sexo: %{x}<br>"
                    "Media poblacional: %{y:.1f} min<br>"
                    "Trabajo ese día: %{customdata[0]:.1f}%<br>"
                    "Media entre quienes trabajaron: "
                    "%{customdata[1]:.1f} min<br>"
                    "Composición por edad:<br>"
                    "&nbsp;&nbsp;10-24: "
                    "%{customdata[2]:.1f}%<br>"
                    "&nbsp;&nbsp;25-44: "
                    "%{customdata[3]:.1f}%<br>"
                    "&nbsp;&nbsp;45-64: "
                    "%{customdata[4]:.1f}%<br>"
                    "&nbsp;&nbsp;65 o más: "
                    "%{customdata[5]:.1f}%<br>"
                    "Muestra: %{customdata[6]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[7]:,.0f}"
                    "Muestra: %{customdata[6]:,.0f}<br>"
                    "Muestra efectiva: %{customdata[7]:,.0f}"
                    "<extra></extra>"
                ),
            )
        )

    base_layout(
        figure,
        "Tiempo de trabajo remunerado por sexo",
        (
            "El tooltip muestra la composición por edad "
            "dentro de cada grupo sexo-año"
        ),
        y_max,
    )

    return figure
