"""Mecanismos del cambio en trayectos laborales por grupo de edad."""
from eut_statistics import effective_sample_size, weighted_mean
from graph_style import ( 
    AGE_ORDER,  YEAR_ORDER, BACKGROUND_COLOR, GRID_COLOR, MUTED_COLOR, TEXT_COLOR, AGE_COLORS, configure_theme
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

METRICS = {'participacion_actividad_pct': {'title': 'Participación en trabajo remunerado', 'ylabel': 'Porcentaje ponderado', 'suffix': '%'}, 'prob_trayecto_dado_actividad_pct': {'title': 'Desplazamiento entre quienes trabajan', 'ylabel': 'Porcentaje ponderado', 'suffix': '%'}, 'duracion_trayecto_entre_desplazados_min': {'title': 'Duración entre quienes se desplazan', 'ylabel': 'Minutos de trayecto', 'suffix': ' min'}, 'trayecto_medio_poblacional_min': {'title': 'Tiempo poblacional de trayecto laboral', 'ylabel': 'Minutos por persona y día', 'suffix': ' min'}}

def summarize(group):
    working = group[['min_trabajo_remunerado', 'min_tray_trabajo', 'factor_elevacion']].dropna()
    working = working[working['factor_elevacion'] > 0]
    activity = working['min_trabajo_remunerado'].to_numpy(dtype=float)
    travel = working['min_tray_trabajo'].to_numpy(dtype=float)
    weights = working['factor_elevacion'].to_numpy(dtype=float)
    works = activity > 0
    travels = travel > 0
    both = works & travels
    participant_weights = weights[works]
    both_weights = weights[both]
    n_eff_activity = effective_sample_size(participant_weights)
    n_eff_both = effective_sample_size(both_weights)
    return pd.Series({'participacion_actividad_pct': 100 * weighted_mean(works, weights), 'prob_trayecto_dado_actividad_pct': 100 * weighted_mean(travels[works], participant_weights) if works.any() else np.nan, 'duracion_trayecto_entre_desplazados_min': weighted_mean(travel[both], both_weights) if both.any() else np.nan, 'trayecto_medio_poblacional_min': weighted_mean(travel, weights), 'actividad_media_poblacional_min': weighted_mean(activity, weights), 'n_muestra_actividad': int(works.sum()), 'n_efectivo_actividad': n_eff_activity, 'n_muestra_actividad_y_trayecto': int(both.sum()), 'n_efectivo_actividad_y_trayecto': n_eff_both})

def build_data(data):
    result = data.groupby(['encuesta_year', 'tramo_edad'], observed=True).apply(summarize, include_groups=False).reset_index()
    result['encuesta_year'] = result['encuesta_year'].astype(int)
    assert len(result) == len(AGE_ORDER) * len(YEAR_ORDER)
    assert result[list(METRICS)].notna().all().all()
    return result

def create_chart(data):
    configure_theme()
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    for ax, (metric, specification) in zip(axes.flat, METRICS.items()):
        for age in AGE_ORDER:
            subset = data[data['tramo_edad'].eq(age)].sort_values('encuesta_year')
            ax.plot(subset['encuesta_year'], subset[metric], color=AGE_COLORS[age], linewidth=2.3, alpha=0.9, zorder=1)
            for _, row in subset.iterrows():
                ax.scatter(row['encuesta_year'], row[metric], s=72, facecolor=AGE_COLORS[age], edgecolor=AGE_COLORS[age], linewidth=1, zorder=2)
        ax.set_title(specification['title'], loc='left', fontsize=14, pad=14)
        ax.set_ylabel(specification['ylabel'])
        ax.set_xticks(YEAR_ORDER)
        ax.set_xlim(2001.5, 2025.5)
        ax.set_axisbelow(True)
        ax.grid(axis='y', color=GRID_COLOR, linestyle='--', linewidth=0.8, alpha=0.75)
        ax.grid(axis='x', visible=False)
        ax.spines[['top', 'right', 'left']].set_visible(False)
        ax.tick_params(axis='y', length=0)

    age_handles = [plt.Line2D([0], [0], color=AGE_COLORS[age], marker='o', markersize=7, linewidth=2, label=age) for age in AGE_ORDER]
    fig.legend(handles=age_handles, loc='upper right', bbox_to_anchor=(0.95, 0.98), ncols=2, frameon=False)
    fig.suptitle('¿Por qué cambia el tiempo de trayecto al trabajo?', x=0.06, y=0.985, ha='left', fontsize=20, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.06, 0.015, 'Una menor duración no demuestra por sí sola una menor distancia recorrida.', fontsize=9, color=MUTED_COLOR)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    plt.tight_layout(rect=[0.05, 0.05, 0.99, 0.95], h_pad=3, w_pad=2.5)
    return fig