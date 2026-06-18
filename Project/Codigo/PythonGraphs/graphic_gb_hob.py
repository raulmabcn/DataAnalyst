"""Configuración de la figura: Aficiones, informática y juegos."""

from graphic_gb_act import build_grouped_activity_data, create_grouped_activity_figure


ACTIVITIES = {'min_ai_arte_aficiones': 'Arte y aficiones', 'min_ai_informatica': 'Informática', 'min_ai_juegos': 'Juegos'}
COLORS = {'Arte y aficiones': '#2F6FAE', 'Informática': '#159A8C', 'Juegos': '#FF7417'}
TITLE = 'Aficiones, informática y juegos'


def build_data(data):
    return build_grouped_activity_data(data, ACTIVITIES)


def create_figure(summary, max_y_range):
    return create_grouped_activity_figure(summary, ACTIVITIES, TITLE, COLORS, max_y_range)
