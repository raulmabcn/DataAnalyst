"""Dumbbell de subcategorías de estudio por sexo, edad y año."""
from graph_style import ( 
    AGE_ORDER, SEX_ORDER, YEAR_ORDER, BACKGROUND_COLOR, GRID_COLOR, MUTED_COLOR, TEXT_COLOR, SUBCATEGORY_COLORS, configure_theme
    )
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STUDY_SUBCATEGORIES = {'min_est_clases_formacion': 'Clases y formación', 'min_est_estudio_tiempo_libre': 'Estudio fuera de clases'}

def weighted_activity_metrics(group, variable, weight='factor_elevacion'):
    valid = group[[variable, weight]].dropna()
    valid = valid[valid[weight] > 0]
    values = valid[variable].to_numpy(dtype=float)
    weights = valid[weight].to_numpy(dtype=float)
    participants = values > 0
    return pd.Series({'media_poblacion': np.average(values, weights=weights), 'participacion_pct': 100 * np.average(participants, weights=weights), 'media_participantes': np.average(values[participants], weights=weights[participants]) if participants.any() else np.nan, 'n_muestra': len(valid), 'n_efectivo': weights.sum() ** 2 / np.square(weights).sum()})

def build_data(data):
    frames = []
    for variable, label in STUDY_SUBCATEGORIES.items():
        summary = data.groupby(['encuesta_year', 'sexo', 'tramo_edad'], observed=True).apply(lambda group: weighted_activity_metrics(group, variable), include_groups=False).reset_index()
        summary['variable'] = variable
        summary['subcategoria'] = label
        frames.append(summary)
    result = pd.concat(frames, ignore_index=True)
    result['encuesta_year'] = result['encuesta_year'].astype(int)
    expected = len(STUDY_SUBCATEGORIES) * len(AGE_ORDER) * len(SEX_ORDER) * len(YEAR_ORDER)
    assert len(result) == expected, f'Se esperaban {expected} resultados y se obtuvieron {len(result)}.'
    assert result[['media_poblacion', 'participacion_pct']].notna().all().all()
    assert result['participacion_pct'].between(0, 100).all()
    return result

def size_scale(percentages):
    """Escala por área con un mínimo visible para participaciones pequeñas."""
    return 38 + percentages * 8

def create_chart(data):
    configure_theme()
    fig, axes = plt.subplots(2, 3, figsize=(17, 10), sharex=True, sharey=True)
    x_max = data['media_poblacion'].max() * 1.18
    positions = np.arange(len(AGE_ORDER))
    for row, sex in enumerate(SEX_ORDER):
        for column, year in enumerate(YEAR_ORDER):
            ax = axes[row, column]
            subset = data[data['sexo'].eq(sex) & data['encuesta_year'].eq(year)]
            wide_mean = subset.pivot(index='tramo_edad', columns='subcategoria', values='media_poblacion').reindex(AGE_ORDER)
            wide_participation = subset.pivot(index='tramo_edad', columns='subcategoria', values='participacion_pct').reindex(AGE_ORDER)
            first_label, second_label = STUDY_SUBCATEGORIES.values()
            for position, age in zip(positions, AGE_ORDER):
                first = wide_mean.loc[age, first_label]
                second = wide_mean.loc[age, second_label]
                ax.plot([first, second], [position, position], color='#AAB4BA', linewidth=2.5, solid_capstyle='round', zorder=1)
                ax.scatter(first, position, s=size_scale(wide_participation.loc[age, first_label]), color=SUBCATEGORY_COLORS[first_label], edgecolor='white', linewidth=1.2, alpha=0.9, zorder=2)
                ax.scatter(second, position, s=size_scale(wide_participation.loc[age, second_label]), color=SUBCATEGORY_COLORS[second_label], edgecolor='white', linewidth=1.2, alpha=0.9, zorder=2)
            if row == 0:
                ax.set_title(str(year), fontsize=15, pad=14)
            if column == 0:
                ax.set_ylabel(sex, fontsize=14, fontweight='bold', labelpad=20)
            else:
                ax.set_ylabel('')
            if row == 1:
                ax.set_xlabel('Minutos medios al día')
            ax.set_xlim(0, x_max)
            ax.set_axisbelow(True)
            ax.grid(axis='x', color=GRID_COLOR, linestyle='--', linewidth=0.8, alpha=0.75)
            ax.grid(axis='y', visible=False)
            ax.spines[['top', 'right', 'left']].set_visible(False)
            ax.tick_params(axis='y', length=0)
    axes[0, 0].set_yticks(positions)
    axes[0, 0].set_yticklabels(AGE_ORDER)
    axes[0, 0].invert_yaxis()
    category_handles = [plt.Line2D([0], [0], marker='o', color='none', markerfacecolor=SUBCATEGORY_COLORS[label], markeredgecolor='white', markersize=10, label=label) for label in STUDY_SUBCATEGORIES.values()]
    size_examples = [5, 15, 30]
    size_handles = [plt.scatter([], [], s=size_scale(value), color='#B8C0C5', edgecolor='white', linewidth=1, label=f'{value}%') for value in size_examples]
    category_legend = fig.legend(handles=category_handles, title='Subcategoría', loc='upper center', bbox_to_anchor=(0.38, 0.925), ncols=2, frameon=False)
    fig.add_artist(category_legend)
    fig.legend(handles=size_handles, title='Participación', loc='upper center', bbox_to_anchor=(0.77, 0.925), ncols=3, frameon=False)
    fig.suptitle('Modalidades de estudio por sexo, edad y año', x=0.06, y=0.985, ha='left', fontsize=20, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.06, 0.95, 'Posición: media diaria ponderada en toda la población · Tamaño: porcentaje que realiza la actividad', fontsize=11, color=MUTED_COLOR)
    fig.text(0.06, 0.015, 'Los valores bajos pueden reflejar tanto poca participación como menor tiempo; la intensidad entre participantes está disponible en el CSV.', fontsize=9, color=MUTED_COLOR)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    plt.tight_layout(rect=[0.05, 0.05, 0.99, 0.88], h_pad=2.5, w_pad=2.5)
    return fig
