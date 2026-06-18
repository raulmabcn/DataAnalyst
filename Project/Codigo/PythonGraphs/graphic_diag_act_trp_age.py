"""Diagnóstico ponderado de actividad y trayectos por edad y año."""
from eut_statistics import effective_sample_size, weighted_mean
from graph_style import AGE_ORDER, YEAR_ORDER
import numpy as np
import pandas as pd
ACTIVITY_TRAVEL_PAIRS = {'Trabajo remunerado': {'activity_columns': ['min_trabajo_remunerado'], 'travel_column': 'min_tray_trabajo'}, 'Hogar y familia': {'activity_columns': ['min_hogar_familia'], 'travel_column': 'min_tray_hogar_familia'}, 'Voluntariado y reuniones': {'activity_columns': ['min_voluntario_reuniones'], 'travel_column': 'min_tray_voluntariado'}, 'Vida social y diversión': {'activity_columns': ['min_vida_social_diversion'], 'travel_column': 'min_tray_vida_social'}, 'Deporte, aficiones y otros ocios': {'activity_columns': ['min_deportes_airelibre', 'min_aficiones_informatica'], 'travel_column': 'min_tray_otro_ocio'}}

def weighted_percentage(condition, weights):
    return 100 * weighted_mean(np.asarray(condition, dtype=float), weights)

def stability_label(n_effective_activity, n_effective_both):
    """Clasificación conservadora para orientar la interpretación."""
    if n_effective_activity < 30 or n_effective_both < 20:
        return 'Muy inestable'
    if n_effective_activity < 100 or n_effective_both < 50:
        return 'Inestable'
    return 'Adecuada'

def summarize_group(group, activity_columns, travel_column):
    working = group[[*activity_columns, travel_column, 'factor_elevacion']].copy()
    working = working.dropna(subset=[*activity_columns, travel_column, 'factor_elevacion'])
    working = working[working['factor_elevacion'] > 0]
    activity = working[activity_columns].sum(axis=1).to_numpy(dtype=float)
    travel = working[travel_column].to_numpy(dtype=float)
    weights = working['factor_elevacion'].to_numpy(dtype=float)
    does_activity = activity > 0
    does_travel = travel > 0
    both = does_activity & does_travel
    activity_no_travel = does_activity & ~does_travel
    travel_no_activity = ~does_activity & does_travel
    neither = ~does_activity & ~does_travel
    participant_weights = weights[does_activity]
    both_weights = weights[both]
    probability_travel_given_activity = weighted_percentage(does_travel[does_activity], participant_weights) if does_activity.any() else np.nan
    travel_duration_among_both = weighted_mean(travel[both], both_weights) if both.any() else np.nan
    activity_duration_among_participants = weighted_mean(activity[does_activity], participant_weights) if does_activity.any() else np.nan
    if does_activity.any():
        weighted_travel_total = np.sum(travel[does_activity] * participant_weights)
        weighted_combined_total = np.sum((activity[does_activity] + travel[does_activity]) * participant_weights)
        mobility_share = 100 * weighted_travel_total / weighted_combined_total if weighted_combined_total > 0 else np.nan
    else:
        mobility_share = np.nan
    n_effective_total = effective_sample_size(weights)
    n_effective_activity = effective_sample_size(participant_weights)
    n_effective_both = effective_sample_size(both_weights)
    diagnostics = {'n_muestra_total': len(working), 'n_efectivo_total': n_effective_total, 'n_muestra_actividad': int(does_activity.sum()), 'n_efectivo_actividad': n_effective_activity, 'n_muestra_actividad_y_trayecto': int(both.sum()), 'n_efectivo_actividad_y_trayecto': n_effective_both, 'participacion_actividad_pct': weighted_percentage(does_activity, weights), 'prob_trayecto_dado_actividad_pct': probability_travel_given_activity, 'duracion_trayecto_entre_desplazados_min': travel_duration_among_both, 'duracion_actividad_entre_participantes_min': activity_duration_among_participants, 'trayecto_medio_poblacional_min': weighted_mean(travel, weights), 'actividad_media_poblacional_min': weighted_mean(activity, weights), 'proporcion_movilidad_pct': mobility_share, 'estado_no_actividad_no_trayecto_pct': weighted_percentage(neither, weights), 'estado_actividad_sin_trayecto_pct': weighted_percentage(activity_no_travel, weights), 'estado_actividad_y_trayecto_pct': weighted_percentage(both, weights), 'estado_trayecto_sin_actividad_pct': weighted_percentage(travel_no_activity, weights), 'estabilidad': stability_label(n_effective_activity, n_effective_both)}
    return diagnostics

def build_diagnostics(data):
    rows = []
    for activity_name, specification in ACTIVITY_TRAVEL_PAIRS.items():
        for year in YEAR_ORDER:
            for age in AGE_ORDER:
                group = data[data['encuesta_year'].eq(year) & data['tramo_edad'].eq(age)]
                diagnostics = summarize_group(group, specification['activity_columns'], specification['travel_column'])
                rows.append({'actividad': activity_name, 'variable_actividad': ' + '.join(specification['activity_columns']), 'variable_trayecto': specification['travel_column'], 'encuesta_year': year, 'tramo_edad': age, **diagnostics})
    result = pd.DataFrame(rows)
    expected = len(ACTIVITY_TRAVEL_PAIRS) * len(YEAR_ORDER) * len(AGE_ORDER)
    assert len(result) == expected
    state_columns = ['estado_no_actividad_no_trayecto_pct', 'estado_actividad_sin_trayecto_pct', 'estado_actividad_y_trayecto_pct', 'estado_trayecto_sin_actividad_pct']
    assert np.allclose(result[state_columns].sum(axis=1), 100), 'Los cuatro estados no suman el 100 %.'
    return result

def build_state_table(diagnostics):
    state_labels = {'estado_no_actividad_no_trayecto_pct': 'No actividad / no trayecto', 'estado_actividad_sin_trayecto_pct': 'Actividad sin trayecto', 'estado_actividad_y_trayecto_pct': 'Actividad y trayecto', 'estado_trayecto_sin_actividad_pct': 'Trayecto sin actividad'}
    return diagnostics.melt(id_vars=['actividad', 'encuesta_year', 'tramo_edad', 'estabilidad'], value_vars=list(state_labels), var_name='estado_codigo', value_name='porcentaje_ponderado').assign(estado=lambda frame: frame['estado_codigo'].map(state_labels))[['actividad', 'encuesta_year', 'tramo_edad', 'estado', 'porcentaje_ponderado', 'estabilidad']]
