"""Cascada de redistribución agregada del día, 2003-2024."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def build_redistribution_data(change_data, start_year=2003, end_year=2024):
    """Descompone el cambio medio en efectos participación e intensidad."""
    result = change_data.copy()

    p_start = result[f"participacion_pct_{start_year}"] / 100
    p_end = result[f"participacion_pct_{end_year}"] / 100
    m_start = result[f"media_participantes_{start_year}"]
    m_end = result[f"media_participantes_{end_year}"]

    result["efecto_participacion_min"] = (
        (p_end - p_start) * (m_start + m_end) / 2
    )
    result["efecto_intensidad_min"] = (
        (m_end - m_start) * (p_start + p_end) / 2
    )
    result["cambio_reconstruido_min"] = (
        result["efecto_participacion_min"]
        + result["efecto_intensidad_min"]
    )
    result["error_descomposicion_min"] = (
        result["cambio_media_min"] - result["cambio_reconstruido_min"]
    )
    result["direccion"] = np.where(
        result["cambio_media_min"] >= 0,
        "Gana tiempo",
        "Pierde tiempo",
    )

    # Primero aparecen las pérdidas más intensas y después las ganancias.
    result = result.sort_values("cambio_media_min").reset_index(drop=True)

    if not np.allclose(
        result["cambio_media_min"],
        result["cambio_reconstruido_min"],
        atol=1e-8,
    ):
        raise AssertionError("La descomposición participación-intensidad no cierra")

    if not np.isclose(result["cambio_media_min"].sum(), 0, atol=1e-8):
        raise AssertionError("Los cambios de las actividades no suman cero minutos")

    return result


def create_redistribution_figure(redistribution_data):
    """Representa los minutos ganados y perdidos como una cascada interactiva."""
    data = redistribution_data.copy()
    customdata = np.column_stack([
        data["media_poblacional_2003"],
        data["media_poblacional_2024"],
        data["participacion_pct_2003"],
        data["participacion_pct_2024"],
        data["media_participantes_2003"],
        data["media_participantes_2024"],
        data["efecto_participacion_min"],
        data["efecto_intensidad_min"],
        data["cambio_participacion_pp"],
        data["n_efectivo_2003"],
        data["n_efectivo_2024"],
    ])

    figure = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative"] * len(data) + ["total"],
        x=data["actividad"].tolist() + ["Balance del día"],
        y=data["cambio_media_min"].tolist() + [0],
        text=[f"{value:+.1f}" for value in data["cambio_media_min"]] + ["0.0"],
        textposition="outside",
        customdata=np.vstack([
            customdata,
            np.full((1, customdata.shape[1]), np.nan),
        ]),
        increasing={"marker": {"color": "#159A8C"}},
        decreasing={"marker": {"color": "#DD2121"}},
        totals={"marker": {"color": "#FF7417"}},
        connector={"line": {"color": "#9AA4AB", "width": 1}},
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Cambio total: %{y:+.2f} min/día<br>"
            "<br><b>Media poblacional</b><br>"
            "2003: %{customdata[0]:.1f} min<br>"
            "2024: %{customdata[1]:.1f} min<br>"
            "<br><b>Participación</b><br>"
            "2003: %{customdata[2]:.1f}%<br>"
            "2024: %{customdata[3]:.1f}%<br>"
            "Cambio: %{customdata[8]:+.1f} pp<br>"
            "<br><b>Media entre participantes</b><br>"
            "2003: %{customdata[4]:.1f} min<br>"
            "2024: %{customdata[5]:.1f} min<br>"
            "<br><b>Descomposición del cambio</b><br>"
            "Efecto participación: %{customdata[6]:+.2f} min<br>"
            "Efecto intensidad: %{customdata[7]:+.2f} min<br>"
            "<br>n efectivo 2003: %{customdata[9]:,.0f}<br>"
            "n efectivo 2024: %{customdata[10]:,.0f}"
            "<extra></extra>"
        ),
    ))

    figure.add_hline(
        y=0,
        line_color="#7A8A93",
        line_width=1.1,
        line_dash="dash",
    )
    figure.update_layout(
        title={
            "text": (
                "Redistribución del día, 2003-2024"
                "<br><sup>Minutos medios ganados y perdidos por las actividades principales</sup>"
            ),
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 25, "color": "#0D1826"},
        },
        height=760,
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font={"family": "Arial, sans-serif", "color": "#0D1826"},
        showlegend=False,
        xaxis={
            "title": "",
            "tickangle": -28,
            "showgrid": False,
        },
        yaxis={
            "title": "Cambio acumulado de minutos diarios",
            "showgrid": True,
            "gridcolor": "#D9DEE3",
            "griddash": "dash",
            "zeroline": False,
        },
        margin={"l": 85, "r": 40, "t": 135, "b": 175},
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )
    
    return figure
