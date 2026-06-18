"""Gráfico dumbbell de subcategorías de hogar y familia por sexo y año."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from eut_common import weighted_group_mean

from graph_style import ( 
    SEX_COLORS, BACKGROUND_COLOR, GRID_COLOR, MUTED_COLOR, TEXT_COLOR
    )

HOUSEHOLD_SUBCATEGORIES = {'min_hf_actividades_culinarias': 'Actividades culinarias', 'min_hf_mantenimiento_hogar': 'Mantenimiento del hogar', 'min_hf_ropa': 'Cuidado de la ropa', 'min_hf_jardineria_animales': 'Jardinería y animales', 'min_hf_construccion_reparaciones': 'Construcción y reparaciones', 'min_hf_compras_servicios': 'Compras y servicios', 'min_hf_gestiones_hogar': 'Gestiones del hogar', 'min_hf_cuidado_menores': 'Cuidado de menores', 'min_hf_cuidado_adultos': 'Cuidado de adultos'}

def build_data(data):
    frames = []
    for column, label in HOUSEHOLD_SUBCATEGORIES.items():
        summary = weighted_group_mean(data, value=column, groups=['encuesta_year', 'sexo'])
        summary['variable'] = column
        summary['subcategoria'] = label
        frames.append(summary)
    result = pd.concat(frames, ignore_index=True)
    result['encuesta_year'] = result['encuesta_year'].astype(int)
    expected_rows = len(HOUSEHOLD_SUBCATEGORIES) * 2 * 3
    assert len(result) == expected_rows, f'Se esperaban {expected_rows} resultados y se obtuvieron {len(result)}.'
    assert result['media_ponderada'].notna().all(), 'Existen medias ponderadas ausentes.'
    wide = result.pivot_table(index=['encuesta_year', 'variable', 'subcategoria'], columns='sexo', values='media_ponderada', observed=True).reset_index()
    wide['brecha_mujer_menos_hombre'] = wide['Mujer'] - wide['Hombre']
    return (result, wide)

def category_order(data):
    data_2024 = data[data['encuesta_year'].eq(2024)]
    return data_2024.groupby('subcategoria', observed=True)['media_ponderada'].mean().sort_values(ascending=False).index.tolist()

def create_chart(wide_data, order):
    years = [2003, 2011, 2024]
    y_positions = np.arange(len(order))
    x_max = wide_data[['Hombre', 'Mujer']].max().max() * 1.18
    fig, axes = plt.subplots(1, 3, figsize=(17, 7.5), sharex=True, sharey=True)
    for ax, year in zip(axes, years):
        subset = wide_data[wide_data['encuesta_year'].eq(year)].set_index('subcategoria').reindex(order)
        for position, category in zip(y_positions, order):
            man = subset.loc[category, 'Hombre']
            woman = subset.loc[category, 'Mujer']
            gap = woman - man
            ax.plot([man, woman], [position, position], color='#AAB4BA', linewidth=3, solid_capstyle='round', zorder=1)
            ax.scatter(man, position, s=95, color=SEX_COLORS['Hombre'], edgecolor='white', linewidth=1.2, zorder=2)
            ax.scatter(woman, position, s=95, color=SEX_COLORS['Mujer'], edgecolor='white', linewidth=1.2, zorder=2)
            right = max(man, woman)
            ax.text(right + x_max * 0.018, position, f'{gap:+.0f}', va='center', ha='left', fontsize=8.5, color=MUTED_COLOR)
        ax.set_title(str(year), fontsize=15, pad=14)
        ax.set_xlabel('Minutos al día')
        ax.set_xlim(0, x_max)
        ax.set_axisbelow(True)
        ax.grid(axis='x', color=GRID_COLOR, linestyle='--', linewidth=0.8, alpha=0.75)
        ax.grid(axis='y', visible=False)
        ax.spines[['top', 'right', 'left']].set_visible(False)
        ax.tick_params(axis='y', length=0)
    axes[0].set_yticks(y_positions)
    axes[0].set_yticklabels(order)
    axes[0].invert_yaxis()
    legend_handles = [plt.Line2D([0], [0], marker='o', color='none', markerfacecolor=SEX_COLORS[sex], markeredgecolor='white', markersize=9, label=sex) for sex in ['Hombre', 'Mujer']]
    fig.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(0.90, 0.95), ncols=2, frameon=False)
    fig.suptitle('Tiempo dedicado al hogar y a la familia, por sexo', x=0.06, y=0.97, ha='left', fontsize=20, fontweight='bold', color=TEXT_COLOR)
    fig.text(0.06, 0.9, 'Media diaria ponderada · La cifra junto a cada línea es la brecha Mujer − Hombre', fontsize=11, color=MUTED_COLOR)
    fig.text(0.06, 0.015, 'El orden de las subcategorías se fija según la media total de 2024 para facilitar la comparación temporal.', fontsize=9, color=MUTED_COLOR)
    fig.patch.set_facecolor(BACKGROUND_COLOR)
    plt.tight_layout(rect=[0.05, 0.06, 0.99, 0.89], w_pad=2.5)
    return fig

