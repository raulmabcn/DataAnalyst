"""Barras apiladas de medios de comunicacion por edad y ano."""
from eut_statistics import effective_sample_size, weighted_mean
from graph_style import AGE_ORDER, SEX_ORDER, YEAR_ORDER, YEAR_COLORS
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ACTIVITIES = {'min_mc_lectura': 'Lectura', 'min_mc_television_video': 'Televisión y vídeo', 'min_mc_radio_grabaciones': 'Radio y grabaciones'}

def summarize(group, variable):
    working = group[['sexo', variable, 'factor_elevacion']].dropna()
    working = working[working['factor_elevacion'] > 0].copy()
    values = working[variable].to_numpy(dtype=float)
    weights = working['factor_elevacion'].to_numpy(dtype=float)
    participants = values > 0
    population_weight = weights.sum()
    weighted_minutes = np.sum(values * weights)
    result = {'media_poblacional_min': weighted_mean(values, weights), 'participacion_pct': 100 * weighted_mean(participants, weights), 
              'media_participantes_min': weighted_mean(values[participants], weights[participants]) if participants.any() else np.nan, 
              'n_muestra': len(working), 'n_efectivo': effective_sample_size(weights)}
    
    for sex in SEX_ORDER:
        sex_mask = working['sexo'].eq(sex).to_numpy()
        sex_weight = weights[sex_mask].sum()
        sex_weighted_minutes = np.sum(values[sex_mask] * weights[sex_mask])
        result[f'representacion_{sex.lower()}_pct'] = 100 * sex_weight / population_weight if population_weight > 0 else np.nan
        result[f'contribucion_{sex.lower()}_pct'] = 100 * sex_weighted_minutes / weighted_minutes if weighted_minutes > 0 else np.nan
    
    return result

def build_data(data):
    rows = []
    for age in AGE_ORDER:
        for year in YEAR_ORDER:
            group = data[data['tramo_edad'].eq(age) & data['encuesta_year'].eq(year)]
            for variable, activity in ACTIVITIES.items():
                rows.append({'encuesta_year': year, 'tramo_edad': age, 'variable': variable, 'actividad': activity, **summarize(group, variable)})
    result = pd.DataFrame(rows)
    result['total_medios_min'] = result.groupby(['encuesta_year', 'tramo_edad'], observed=True)['media_poblacional_min'].transform('sum')
    result['peso_segmento_pct'] = np.where(result['total_medios_min'] > 0, 
                                           100 * result['media_poblacional_min'] / result['total_medios_min'], 
                                           np.nan)
    expected = len(YEAR_ORDER) * len(AGE_ORDER) * len(ACTIVITIES)
    assert len(result) == expected
    assert result['media_poblacional_min'].notna().all()
    
    return result

def create_figure(summary):
    figure = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=AGE_ORDER,
        shared_yaxes=True,
        vertical_spacing=0.15,
        horizontal_spacing=0.09,
    )

    category_order = list(ACTIVITIES.values())

    max_value = summary["media_poblacional_min"].max()
    y_max = max_value * 1.15

    for panel, age in enumerate(AGE_ORDER):
        row = panel // 2 + 1
        col = panel % 2 + 1
        age_data = summary[summary["tramo_edad"].eq(age)]

        for year in YEAR_ORDER:
            subset = (
                age_data[age_data["encuesta_year"].eq(year)]
                .set_index("actividad")
                .reindex(category_order)
                .reset_index()
            )

            customdata = np.column_stack([
                subset["participacion_pct"],
                subset["media_participantes_min"],
                subset["peso_segmento_pct"],
                subset["representacion_hombre_pct"],
                subset["representacion_mujer_pct"],
                subset["contribucion_hombre_pct"],
                subset["contribucion_mujer_pct"],
                subset["n_muestra"],
                subset["n_efectivo"],
                subset["total_medios_min"],
            ])

            figure.add_trace(
                go.Bar(
                    x=subset["actividad"],
                    y=subset["media_poblacional_min"],
                    name=str(year),
                    legendgroup=str(year),
                    showlegend=panel == 0,
                    marker={"color": YEAR_COLORS[year]},
                    customdata=customdata,
                    hovertemplate=(
                        f"<b>{year}</b><br>"
                        f"{age} · %{{x}}<br>"
                        "Media poblacional: %{y:.1f} min/día<br>"
                        "Participación: %{customdata[0]:.1f}%<br>"
                        "Media entre participantes: %{customdata[1]:.1f} min/día<br>"
                        "Peso en el total de medios: %{customdata[2]:.1f}%<br><br>"
                        "<b>Composición del grupo</b><br>"
                        "Hombres: %{customdata[3]:.1f}% · "
                        "Mujeres: %{customdata[4]:.1f}%<br>"
                        "Contribución al tiempo - H: %{customdata[5]:.1f}% · "
                        "M: %{customdata[6]:.1f}%<br>"
                        "Muestra: %{customdata[7]:,.0f} · "
                        "n efectivo: %{customdata[8]:,.0f}<br>"
                        "Total de medios: %{customdata[9]:.1f} min/día"
                        "<extra></extra>"
                    ),
                ),
                row=row,
                col=col,
            )

    figure.update_layout(
        barmode="group",
        title={
            "text": "Tiempo diario dedicado a medios de comunicación",
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 25, "color": "#0D1826"},
        },
        height=790,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Arial, sans-serif", "color": "#0D1826"},
        legend={
            "orientation": "h",
            "x": 0.6,
            "y": 1.10,
            "xanchor": "left",
            "yanchor": "bottom",
            "title": {"text": "Año"},
        },
        margin={"l": 75, "r": 35, "t": 145, "b": 75},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )

    figure.update_xaxes(
        title_text="",
        type="category",
        categoryorder="array",
        categoryarray=category_order,
        showgrid=False,
        tickfont={"size": 12},
    )
    figure.update_yaxes(
        title_text="Minutos diarios",
        range=[0, y_max],
        showgrid=True,
        gridcolor="#D9DEE3",
        griddash="dash",
        zeroline=False,
    )

    return figure