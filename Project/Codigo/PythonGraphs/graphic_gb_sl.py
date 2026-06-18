"""Configuración de la figura: Vida social, diversión y ocio pasivo."""

from graphic_gb_act import build_grouped_activity_data, create_grouped_activity_figure


ACTIVITIES = {'min_vs_vida_social': 'Vida social', 'min_vs_diversion_cultura': 'Diversión y cultura', 'min_vs_ocio_pasivo': 'Ocio pasivo'}
COLORS = {'Vida social': '#2F6FAE', 'Diversión y cultura': '#159A8C', 'Ocio pasivo': '#FF7417'}
TITLE = 'Vida social, diversión y ocio pasivo'


def build_data(data):
    return build_grouped_activity_data(data, ACTIVITIES)


def create_figure(summary, max_y_range):
    return create_grouped_activity_figure(summary, ACTIVITIES, TITLE, COLORS, max_y_range)
