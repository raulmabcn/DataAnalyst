"""Órdenes y colores reutilizados por los módulos gráficos."""

import seaborn as sns

YEAR_ORDER = [2003, 2011, 2024]
AGE_ORDER = ["10-24 años", "25-44 años", "45-64 años", "65 o más"]
SEX_ORDER = ["Hombre", "Mujer"]

DEFAULT_COLORS = ["#2F6FAE", "#159A8C", "#FF7417", "#7C6EA8"]

AGE_COLORS = {
    "10-24 años": "#F5C200",
    "25-44 años": "#6BAF2A",
    "45-64 años": "#C03B2C",
    "65 o más": "#8A8A8A",
}

SEX_COLORS = {
    "Hombre": "#7B2FBF",
    "Mujer": "#D4387A",
}

TEXT_COLOR = "#0D1826"
MUTED_COLOR = "#4B535C"
BACKGROUND_COLOR = "#FFFFFF"
GRID_COLOR = "#D9DEE3"

YEAR_COLORS = {
    2003: "#2F6FAE",
    2011: "#159A8C",
    2024: "#FF7417",
}

QUARTER_COLORS = {
    "Ene-Mar": "#2F6FAE", "Abr-Jun": "#159A8C", "Jul-Sep": "#FFB25B",
    "Oct-Dic": "#FF7417", "No consta": "#A8B3BA",
}

DAY_COLORS = {"Lunes-Jueves": "#2F6FAE", "Viernes-Domingo": "#FF7417", "No consta": "#A8B3BA"}

PROFILE_PALETTE = [
    "#2F6FAE",
    "#159A8C",
    "#FF7417",
    "#7C6EA8",
    "#D4A72C",
    "#7A8A93",
]
ACTIVITY_COLORS = {'Cuidados personales': '#2F6FAE', 'Trabajo remunerado': '#159A8C', 'Estudios': '#FF7417', 'Hogar y familia': '#7C6EA8', 'Voluntariado y reuniones': '#D4A72C', 'Vida social y diversión': '#D95F76', 'Deporte y aire libre': '#49A65E', 'Aficiones e informática': '#925E9F', 'Medios de comunicación': '#5F7D8A', 'Trayectos': '#A56A43'}
SUBCATEGORY_COLORS = {'Clases y formación': '#2F6FAE', 'Estudio fuera de clases': '#FF7417'}

TRAVEL_COLORS = {'Trabajo': '#2F6FAE', 'Estudios': '#159A8C', 'Hogar y familia': '#FF7417', 'Voluntariado': '#D4A72C', 'Vida social': '#D95F76', 'Deporte y otro ocio': '#7C6EA8', 'Cambio de municipio': '#49A65E', 'Otros no especificados': '#7A8A93', 'Sin clasificar': '#D7DCE0'}
MEDIA_COLORS = {'Lectura': '#0F2027', 'Televisión y vídeo': '#8D5B4C', 'Radio y grabaciones': '#C9A054'}
VOLUNTARY_COLORS = {'Voluntariado organizado': "#0F2717", 'Ayuda a otros hogares': "#8D4C6A", 'Participación y religión': "#98C954"}

STRATUM_COLORS = {
    "Municipio pequeño / Área rural": "#2F6FAE",
    "Ciudad media / Área semidensa": "#159A8C",
    "Gran ciudad / Área densa": "#FF7417", "No consta": "#A8B3BA",
}

QUADRANT_COLORS = {
    "Más minutos y más participación": "#159A8C",
    "Más minutos y menos participación": "#2F6FAE",
    "Menos minutos y más participación": "#FFB25B",
    "Menos minutos y menos participación": "#FF7417",
}

COMPARABILITY_COLORS = {
    "Alta": "#DCEAE6",
    "Media-alta": "#E8F0F7",
    "Media": "#FFF0DE",
    "Limitada": "#FADFD7",
}

def configure_theme():
    """Aplica el tema visual común a Matplotlib y Seaborn."""
    sns.set_theme(
        style="whitegrid",
        context="notebook",
        font="DejaVu Sans",
        rc={
            "figure.facecolor": BACKGROUND_COLOR,
            "axes.facecolor": BACKGROUND_COLOR,
            "axes.edgecolor": TEXT_COLOR,
            "axes.labelcolor": TEXT_COLOR,
            "axes.titlecolor": TEXT_COLOR,
            "axes.titleweight": "bold",
            "text.color": TEXT_COLOR,
            "xtick.color": TEXT_COLOR,
            "ytick.color": TEXT_COLOR,
            "grid.color": GRID_COLOR,
            "grid.linestyle": "--",
            "grid.linewidth": 0.8,
            "grid.alpha": 0.75,
            "legend.frameon": False,
        },
    )


def highlight_comparability(value):
    color = COMPARABILITY_COLORS.get(value)

    if color is None:
        return ""

    return (
        f"background-color: {color};"
        f"color: {TEXT_COLOR};"
        "font-weight: bold;"
    )

def comparability_styled( table ):
    return (
    table.style
    .hide(axis="index")
    .map(
        highlight_comparability,
        subset=["Comparabilidad"],
    )
    .set_properties(
        **{
            "background-color": "#FCFCFB",
            "color": "#0D1826",
        }
    )
    .set_properties(
        subset=["Dimensión", "Variable"],
        **{
            "background-color": "#E8EDF1",
            "color": "#0D1826",
            "font-weight": "bold",
            "text-align": "left",
        },
    )
    .set_properties(
        subset=["Observaciones"],
        **{
            "color": "#263238",
            "text-align": "left",
            "max-width": "420px",
        },
    )
    .set_properties(
        subset=["2003", "2011", "2024", "Comparabilidad"],
        **{
            "text-align": "center",
        },
    )
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#0D1826"),
                ("color", "#FFFFFF"),
                ("font-weight", "bold"),
                ("text-align", "center"),
                ("padding", "9px"),
            ],
        },
        {
            "selector": "td",
            "props": [
                ("border-bottom", "1px solid #D9DEE3"),
                ("padding", "9px"),
                ("vertical-align", "top"),
            ],
        },
        {
            "selector": "td.col0, td.col1",
            "props": [
                ("background-color", "#E8EDF1 !important"),
                ("color", "#0D1826 !important"),
                ("font-weight", "bold"),
            ],
        },
        {
            "selector": "table",
            "props": [
                ("background-color", "#FCFCFB"),
                ("border-collapse", "collapse"),
                ("width", "100%"),
                ("font-size", "13px"),
            ],
        },
    ])
)