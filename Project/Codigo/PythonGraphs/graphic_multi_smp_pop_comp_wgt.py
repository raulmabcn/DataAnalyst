"""Figuras del análisis descriptivo y de calidad muestral."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from graph_style import (
    BACKGROUND_COLOR,
    GRID_COLOR,
    MUTED_COLOR,
    PROFILE_PALETTE,
    TEXT_COLOR,
    YEAR_COLORS,
)

def create_sample_units_figure(sample_overview):
    fig, ax = plt.subplots(figsize=(10, 5.8))
    sns.barplot(
        data=sample_overview, x="año", y="personas_muestra", hue="año",
        palette=YEAR_COLORS, width=0.58, legend=False, ax=ax,
    )
    ax.set_title("Personas incluidas en cada encuesta (en miles)", loc="left", fontsize=16, pad=16)
    ax.set_xlabel("")
    ax.set_ylabel("Número de observaciones")
    ax.spines[["top", "right"]].set_visible(False)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=4, fontsize=10, color=TEXT_COLOR)
    fig.tight_layout(rect=[0, 0.045, 1, 1])
    return fig


def create_population_figure(sample_overview):
    fig, ax = plt.subplots(figsize=(10, 5.8))
    sns.barplot(
        data=sample_overview, x="año", y="poblacion_millones", hue="año",
        palette=YEAR_COLORS, width=0.58, legend=False, ax=ax,
    )
    ax.set_title("Población representada por cada encuesta (en millones)", loc="left", fontsize=16, pad=16)
    ax.set_xlabel("")
    ax.set_ylabel("Millones de personas")
    ax.spines[["top", "right"]].set_visible(False)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f M", padding=4, fontsize=10, color=TEXT_COLOR)
    fig.tight_layout(rect=[0, 0.045, 1, 1])
    return fig


def _composition_table(composition, variable, category_order):
    categories = list(category_order)
    values = composition[variable].astype("string")
    if "No consta" in values.values and "No consta" not in categories:
        categories.append("No consta")
    table = (
        composition.pivot(index="encuesta_year", columns=variable, values="porcentaje")
        .reindex(index=[2003, 2011, 2024], columns=categories)
        .fillna(0)
    )
    return table


def create_stacked_composition_figure(
    composition, variable, title, category_order, palette=PROFILE_PALETTE
):
    table = _composition_table(composition, variable, category_order)
    colors = palette[:len(table.columns)]
    fig, ax = plt.subplots(figsize=(10, 6))

    table.plot(
        kind="bar", stacked=True, width=0.62, color=colors,
        edgecolor="none", legend=False, ax=ax
    )

    cumulative = np.zeros(len(table))
    for category in table.columns:
        values = table[category].to_numpy()
        for position, (bottom, value) in enumerate(zip(cumulative, values)):
            if value >= 4:
                ax.text(
                    position, bottom + value / 2, f"{value:.1f}%",
                    ha="center", va="center", fontsize=9,
                    fontweight="bold", color="white"
                )
        cumulative += values

    ax.set(xlabel="", ylabel="Porcentaje de la población ponderada", ylim=(0, 100))
    ax.set_xticklabels([str(int(year)) for year in table.index], rotation=0)
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.75)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right"]].set_visible(False)

    fig.suptitle(
        title, x=0.03, y=0.98, ha="left", va="top",
        fontsize=16, fontweight="bold", color=TEXT_COLOR
    )

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="none")
        for color in colors
    ]

    fig.legend(
        handles, table.columns, loc="upper left",
        bbox_to_anchor=(0.68, 0.985), ncols=min(2, len(table.columns)),
        frameon=False, fontsize=9, handlelength=1.2,
        handletextpad=0.5, columnspacing=1.1
    )

    fig.text(
        0.04, 0.01, "Porcentajes calculados utilizando el factor de elevación.",
        fontsize=9, color=MUTED_COLOR
    )

    fig.tight_layout(rect=[0, 0.05, 1, 0.88])
    return fig

def create_composition_pies_figure(
    composition, variable, title, category_order, colors,
):
    table = _composition_table(composition, variable, category_order)
    palette = [colors.get(category, "#A8B3BA") for category in table.columns]
    fig, axes = plt.subplots(1, 3, figsize=(10, 4.5))

    def percentage_label(value):
        return f"{value:.1f}%" if value >= 3 else ""

    wedges = []
    for ax, (year, values) in zip(axes, table.iterrows()):
        wedges, _, autotexts = ax.pie(
            values, colors=palette, startangle=90, counterclock=False,
            autopct=percentage_label, pctdistance=0.75,
            wedgeprops={"width": 0.48, "edgecolor": BACKGROUND_COLOR, "linewidth": 2},
        )
        for text in autotexts:
            text.set_color("white")
            text.set_fontsize(9)
            text.set_fontweight("bold")
        ax.text(0, 0, str(int(year)), ha="center", va="center", fontsize=14,
                fontweight="bold", color=TEXT_COLOR)
        ax.set_aspect("equal")
    fig.suptitle(title, x=0.03, y=0.98, ha="left", va="top", fontsize=16,
                 fontweight="bold", color=TEXT_COLOR)
    fig.legend(wedges, table.columns, title="", loc="upper left",
               bbox_to_anchor=(0.68, 0.985), ncols=min(1, len(table.columns)), frameon=False,
               fontsize=9, handlelength=1.2, handletextpad=0.5, columnspacing=1.1 )
    fig.text(0.04, -0.05, "Porcentajes calculados utilizando el factor de elevación.",
             fontsize=9, color=MUTED_COLOR)
    fig.tight_layout(rect=[0, 0.05, 1, 0.88])
    return fig


def create_weighted_vs_unweighted_figure(comparison, variable, title, category_order):
    categories = list(category_order)
    if "No consta" in comparison[variable].astype("string").values and "No consta" not in categories:
        categories.append("No consta")
    working = comparison.copy()
    working[variable] = working[variable].astype("string")
    ncols = 2
    nrows = int(np.ceil(len(categories) / ncols))
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(12, 4.5 * nrows), sharey=True)
    axes = np.atleast_1d(axes).flatten()
    method_colors = {"Sin ponderar": "#A8B3BA", "Ponderado": "#2F6FAE"}
    for ax, category in zip(axes, categories):
        subset = working[working[variable].eq(category)]
        sns.barplot(
            data=subset, x="encuesta_year", y="porcentaje", hue="estimacion",
            hue_order=["Sin ponderar", "Ponderado"], palette=method_colors, width=0.65, ax=ax,
        )
        ax.set_title(str(category), loc="left", fontsize=13, weight="bold")
        ax.set_xlabel("")
        ax.set_ylabel("Porcentaje" if ax in axes[::ncols] else "")
        ax.set_ylim(0, max(5, working["porcentaje"].max() * 1.16))
        ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.75)
        ax.grid(axis="x", visible=False)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f%%", padding=3, fontsize=9)
        if ax.get_legend() is not None:
            ax.get_legend().remove()
    for ax in axes[len(categories):]:
        ax.set_visible(False)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.96, 0.97),
               ncols=2, frameon=False)
    fig.suptitle(title, x=0.06, y=0.99, ha="left", fontsize=17,
                 weight="bold", color=TEXT_COLOR)
    fig.text(0.06, 0.01,
             "Sin ponderar: composición de la muestra. Ponderado: estimación de la población.",
             fontsize=9, color=MUTED_COLOR)
    fig.tight_layout(rect=[0.04, 0.04, 1, 0.94])
    return fig


def create_effective_sample_figure(weight_quality):
    fig, ax = plt.subplots(figsize=(10, 5.8))
    years = weight_quality["encuesta_year"].to_numpy()
    positions = np.arange(len(years))
    width = 0.32
    observed = ax.bar(positions - width / 2, weight_quality["n_muestra"], width=width,
                      color="#A8B3BA", label="Muestra observada")
    effective = ax.bar(positions + width / 2, weight_quality["n_efectivo"], width=width,
                       color=[YEAR_COLORS[year] for year in years], label="Muestra efectiva")
    ax.bar_label(observed, fmt="{:,.0f}", padding=4, fontsize=10, color=TEXT_COLOR)
    ax.bar_label(effective, fmt="{:,.0f}", padding=4, fontsize=10,
                 fontweight="bold", color=TEXT_COLOR)
    for position, (_, row) in enumerate(weight_quality.iterrows()):
        ax.text(position, max(row["n_muestra"], row["n_efectivo"]) * 1.10,
                f'Eficiencia: {row["eficiencia_pct"]:.1f}%', ha="center", va="bottom",
                fontsize=9, color=MUTED_COLOR)
    ax.set_title("Muestra observada y tamaño muestral efectivo", loc="left", fontsize=16, pad=16)
    ax.set_xlabel("")
    ax.set_ylabel("Número de personas")
    ax.set_xticks(positions, years)
    ax.yaxis.set_major_formatter(lambda value, position: f"{value:,.0f}")
    ax.set_ylim(0, weight_quality["n_muestra"].max() * 1.25)
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.75)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(title="", loc="upper left", ncols=2)
    fig.text(0.125, 0.01,
             "El tamaño efectivo disminuye cuando los factores de elevación son desiguales.",
             fontsize=9, color=MUTED_COLOR)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    return fig


def create_weight_dispersion_figure(weights_plot):
    fig, ax = plt.subplots(figsize=(10, 5.8))
    sns.boxplot(
        data=weights_plot, x="encuesta_year", y="peso_normalizado", hue="encuesta_year",
        palette=YEAR_COLORS, width=0.55, whis=(5, 95), showfliers=False, legend=False, ax=ax,
    )
    ax.axhline(1, color=TEXT_COLOR, linestyle=":", linewidth=1.2)
    ax.set_title("Dispersión de los factores de elevación", loc="left", fontsize=16, pad=16)
    ax.set_xlabel("")
    ax.set_ylabel("Factor de elevación normalizado")
    ax.set_yscale("log")
    ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.8, alpha=0.75)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.text(0.125, 0.01,
             "Pesos divididos por la media de cada año. Bigotes correspondientes a los percentiles 5 y 95.",
             fontsize=9, color=MUTED_COLOR)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    return fig


def create_temporal_composition_figure(
    composition,
    variable,
    title,
    category_order,
    colors,
):
    table = _composition_table(
        composition,
        variable,
        category_order,
    )

    fig, ax = plt.subplots(figsize=(13.5, 5.8))

    table.plot(
        kind="bar",
        stacked=True,
        width=0.60,
        color=[
            colors.get(category, "#A8B3BA")
            for category in table.columns
        ],
        edgecolor="none",
        ax=ax,
    )

    cumulative = np.zeros(len(table))

    for category in table.columns:
        values = table[category].to_numpy()

        for position, (bottom, value) in enumerate(
            zip(cumulative, values)
        ):
            if value >= 4:
                ax.text(
                    position,
                    bottom + value / 2,
                    f"{value:.1f}%",
                    ha="center",
                    va="center",
                    fontsize=10,
                    fontweight="bold",
                    color="white",
                )

        cumulative += values

    ax.set_title(
        title,
        loc="left",
        fontsize=16,
        pad=60,
    )

    ax.set_xlabel("")
    ax.set_ylabel("Porcentaje ponderado")
    ax.set_ylim(0, 100)

    ax.set_xticklabels(
        [str(int(year)) for year in table.index],
        rotation=0,
    )

    ax.grid(
        axis="y",
        color=GRID_COLOR,
        linestyle="--",
        linewidth=0.8,
        alpha=0.75,
    )
    ax.grid(axis="x", visible=False)

    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)

    ax.legend(
        title="",
        loc="upper left",
        bbox_to_anchor=(0.8, 1.2),
        ncols=2,
        frameon=False,
        fontsize=9,
        columnspacing=1.3,
        handletextpad=0.5,
    )

    fig.text(
        0.08,
        0.03,
        "Distribución calculada utilizando el factor de elevación.",
        fontsize=9,
        color=MUTED_COLOR,
    )

    fig.subplots_adjust(
        left=0.08,
        right=0.67,
        top=0.82,
        bottom=0.15,
    )

    return fig
