"""Línea temporal interactiva de acontecimientos sociales."""

import html
import textwrap

import plotly.graph_objects as go

from graph_style import BACKGROUND_COLOR, MUTED_COLOR, TEXT_COLOR, YEAR_COLORS


MILESTONE_YEARS = {2003, 2011, 2024}
EVENT_COLOR = "#7A8A93"
LEVELS_ABOVE = [1.20, 2.15, 3.10, 4.05, 5.00]
LEVELS_BELOW = [-1.20, -2.15, -3.10, -4.05, -5.00]


def _wrap_label(value, width=25):
    return "<br>".join(
        textwrap.wrap(value, width=width, break_long_words=False)
    )


def _hex_to_rgba(color, alpha):
    color = color.lstrip("#")
    red, green, blue = (
        int(color[index:index + 2], 16)
        for index in (0, 2, 4)
    )
    return f"rgba({red},{green},{blue},{alpha})"


def _prepare_events(events):
    prepared = [dict(event) for event in events]

    for event in prepared:
        event["anio_inicio"] = int(event["anio_inicio"])
        event["anio_fin"] = int(event["anio_fin"])

    return sorted(
        prepared,
        key=lambda event: (event["anio_inicio"], event["categoria"]),
    )


def _assign_positions(events):
    year_counts = {}

    for index, event in enumerate(events):
        year = event["anio_inicio"]
        occurrence = year_counts.get(year, 0)
        year_counts[year] = occurrence + 1
        above = (index + occurrence) % 2 == 0
        levels = LEVELS_ABOVE if above else LEVELS_BELOW
        level_index = (index // 2 + occurrence) % len(levels)
        event["label_y"] = levels[level_index]


def create_figure(events):
    """Construye la línea temporal a partir de una secuencia de eventos."""
    events = _prepare_events(events)
    _assign_positions(events)
    figure = go.Figure()

    for event in events:
        if event["anio_fin"] <= event["anio_inicio"]:
            continue

        figure.add_shape(
            type="rect",
            x0=event["anio_inicio"],
            x1=event["anio_fin"],
            y0=-0.12,
            y1=0.12,
            fillcolor=_hex_to_rgba(EVENT_COLOR, 0.25),
            line={"color": _hex_to_rgba(EVENT_COLOR, 0.55), "width": 1},
            layer="below",
        )

    figure.add_trace(go.Scatter(
        x=[2000, 2024],
        y=[0, 0],
        mode="lines",
        line={"color": TEXT_COLOR, "width": 2},
        hoverinfo="skip",
        showlegend=False,
    ))

    for event in events:
        anchor_year = (event["anio_inicio"] + event["anio_fin"]) / 2
        figure.add_shape(
            type="line",
            x0=anchor_year,
            x1=anchor_year,
            y0=0,
            y1=event["label_y"] * 0.82,
            line={"color": EVENT_COLOR, "width": 1.2},
            layer="below",
        )

        period = str(event["anio_inicio"])
        if event["anio_fin"] != event["anio_inicio"]:
            period = f'{event["anio_inicio"]}-{event["anio_fin"]}'

        label = (
            f"<b>{period}</b><br>"
            f"{_wrap_label(event['descripcion'])}"
        )
        figure.add_trace(go.Scatter(
            x=[anchor_year],
            y=[event["label_y"]],
            mode="markers",
            marker={
                "symbol": "circle",
                "size": 170,
                "color": _hex_to_rgba(EVENT_COLOR, 0.13),
                "line": {"color": EVENT_COLOR, "width": 2},
            },
            hoverinfo="skip",
            showlegend=False,
        ))
        figure.add_annotation(
            x=anchor_year,
            y=event["label_y"],
            text=label,
            showarrow=False,
            xanchor="center",
            yanchor="middle",
            align="center",
            font={"size": 10, "color": MUTED_COLOR},
        )

    standard_events = [
        event for event in events
        if event["anio_inicio"] not in MILESTONE_YEARS
    ]
    figure.add_trace(go.Scatter(
        x=[event["anio_inicio"] for event in standard_events],
        y=[0] * len(standard_events),
        mode="markers",
        marker={
            "size": 8,
            "color": EVENT_COLOR,
            "line": {"color": "white", "width": 1},
        },
        customdata=[
            [event["periodo"], event["descripcion"]]
            for event in standard_events
        ],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "%{customdata[1]}<extra></extra>"
        ),
        showlegend=False,
    ))

    for year in sorted(MILESTONE_YEARS):
        matching = [
            event for event in events
            if event["anio_inicio"] == year or event["anio_fin"] == year
        ]
        descriptions = "<br>".join(
            f"• {html.escape(event['descripcion'])}"
            for event in matching
        )
        color = YEAR_COLORS[year]
        figure.add_trace(go.Scatter(
            x=[year],
            y=[0],
            mode="markers+text",
            marker={
                "size": 24,
                "symbol": "circle-open",
                "color": color,
                "line": {"color": color, "width": 4},
            },
            text=[f"<b>{year}</b>"],
            textposition="bottom center",
            textfont={"size": 13, "color": color},
            hovertemplate=(
                f"<b>{year}</b><br>{descriptions}<extra></extra>"
            ),
            showlegend=False,
        ))

    figure.update_yaxes(
        range=[-6.2, 6.2],
        visible=False,
        fixedrange=True,
    )
    figure.update_layout(
        title={
            "text": (
                "Línea temporal de acontecimientos (2003-2024)"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24, "color": TEXT_COLOR},
        },
        template="plotly_white",
        height=620,
        margin={"l": 35, "r": 35, "t": 70, "b": 55},
        showlegend=False,
        hoverlabel={"bgcolor": "white", "font_size": 13},
        plot_bgcolor=BACKGROUND_COLOR,
        paper_bgcolor=BACKGROUND_COLOR,
        font={"family": "Arial, sans-serif", "color": TEXT_COLOR},
    )
    return figure
