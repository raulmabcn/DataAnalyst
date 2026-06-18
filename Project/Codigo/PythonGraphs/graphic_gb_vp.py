"""Configuración de la figura: Voluntariado y participación social."""

from graphic_gb_act import build_grouped_activity_data, create_grouped_activity_figure

ACTIVITIES = {'min_vr_voluntariado_organizado': 'Voluntariado organizado', 'min_vr_ayuda_otros_hogares': 'Ayuda a otros hogares', 'min_vr_participacion_religion': 'Participación y religión'}
TITLE = 'Voluntariado y participación social'

def build_data(data):
    return build_grouped_activity_data(data, ACTIVITIES)


def create_figure(summary):
    return create_grouped_activity_figure(summary, ACTIVITIES, TITLE)
