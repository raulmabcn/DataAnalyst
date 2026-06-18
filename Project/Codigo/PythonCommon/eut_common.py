"""Utilidades compartidas para el análisis de las EUT 2003, 2011 y 2024."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "CleanDataSets"
ANALYSIS_DATA_DIR = DATA_DIR
PREPARED_DATA = DATA_DIR / "eut_analisis_preparado.csv"

DATA_FILES = {
    2003: DATA_DIR / "eut2003.csv",
    2011: DATA_DIR / "eut2011.csv",
    2024: DATA_DIR / "eut2024.csv",
}

ID_DTYPES = {
    "hogar_uid": "string",
    "persona_uid": "string",
    "id_hogar": "string",
    "n_pers": "string",
}

MAIN_TIME_COLS = [
    "min_cuidados_personales",
    "min_trabajo_remunerado",
    "min_estudios",
    "min_hogar_familia",
    "min_voluntario_reuniones",
    "min_vida_social_diversion",
    "min_deportes_airelibre",
    "min_aficiones_informatica",
    "min_medios_comunicacion",
    "min_trayectos_noespec",
]

CATEGORY_ORDERS = {
    "encuesta_year": [2003, 2011, 2024],
    "tramo_edad": ["10-24 años", "25-44 años", "45-64 años", "65 o más"],
    "sexo": ["Hombre", "Mujer"],
    "nivel_estudios": [
        "Primaria o inferior",
        "Sec. primera etapa",
        "Sec. segunda etapa",
        "Educación superior",
    ],
    "situacion_laboral": [
        "Ocupado",
        "Desocupado",
        "Jubilado o prejubilado",
        "Otra inactividad",
    ],
    "estrato": [
        "Municipio pequeño / Área rural",
        "Ciudad media / Área semidensa",
        "Gran ciudad / Área densa",
    ],
    "estado_salud": ["Muy bueno", "Bueno", "Aceptable", "Malo", "Muy malo"],
    "trimestre": ["Ene-Mar", "Abr-Jun", "Jul-Sep", "Oct-Dic"],
    "dia_semana": ["Lunes-Jueves", "Viernes-Domingo"],
    "tipo_dia": ["Día habitual", "Día inusual"],
}

ACTIVITY_LABELS = {
    "min_cuidados_personales": "Cuidados personales",
    "min_trabajo_remunerado": "Trabajo remunerado",
    "min_estudios": "Estudios",
    "min_hogar_familia": "Hogar y familia",
    "min_voluntario_reuniones": "Voluntariado y reuniones",
    "min_vida_social_diversion": "Vida social y diversión",
    "min_deportes_airelibre": "Deporte y aire libre",
    "min_aficiones_informatica": "Aficiones e informática",
    "min_medios_comunicacion": "Medios de comunicación",
    "min_trayectos_noespec": "Trayectos",
}

SOCIAL_VARIABLES = [
    "sexo",
    "tramo_edad",
    "nivel_estudios",
    "situacion_laboral",
    "estrato",
    "estado_salud",
    "dia_semana",
]

PROFILE_VARIABLES = {
    "sexo": "Sexo",
    "tramo_edad": "Edad",
    "nivel_estudios": "Nivel educativo",
    "situacion_laboral": "Situación laboral",
    "estrato": "Estrato territorial",
}


def minute_columns(data):
    all_minutes = [column for column in data.columns if column.startswith("min_")]
    internet = [column for column in all_minutes if column.startswith("min_internet")]
    subactivities = [
        column for column in all_minutes
        if column not in MAIN_TIME_COLS + internet
    ]
    return all_minutes, subactivities, internet


def apply_analysis_types(data):
    """Devuelve una copia con tipos numéricos y categorías ordenadas."""
    result = data.copy()
    all_minutes, _, _ = minute_columns(result)

    for column, categories in CATEGORY_ORDERS.items():
        if column in result:
            result[column] = pd.Categorical(
                result[column], categories=categories, ordered=True
            )

    result[all_minutes] = result[all_minutes].apply(pd.to_numeric, errors="coerce")
    result["factor_elevacion"] = pd.to_numeric(
        result["factor_elevacion"], errors="coerce"
    )
    return result


def load_harmonized_data():
    missing = [str(path) for path in DATA_FILES.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"No se encuentran los ficheros: {missing}")
    return {
        year: pd.read_csv(path, dtype=ID_DTYPES)
        for year, path in DATA_FILES.items()
    }


def validate_harmonized_datasets(datasets):
    reference_columns = list(datasets[2003].columns)
    for year, data in datasets.items():
        if list(data.columns) != reference_columns:
            raise AssertionError(f"{year}: esquema distinto")
        if not data["encuesta_year"].eq(year).all():
            raise AssertionError(f"{year}: año incorrecto")
        if not data["persona_uid"].notna().all():
            raise AssertionError(f"{year}: persona_uid vacío")
        if data["persona_uid"].duplicated().any():
            raise AssertionError(f"{year}: persona_uid duplicado")
        if not data["factor_elevacion"].notna().all():
            raise AssertionError(f"{year}: faltan pesos")
        if not data["factor_elevacion"].gt(0).all():
            raise AssertionError(f"{year}: pesos no positivos")
        if not data["dia_semana"].isin(
            ["Lunes-Jueves", "Viernes-Domingo"]
        ).all():
            raise AssertionError(f"{year}: valores inesperados en dia_semana")
        if not np.isclose(data[MAIN_TIME_COLS].sum(axis=1), 1440).all():
            raise AssertionError(f"{year}: diario distinto de 1.440 minutos")
    return True


def prepare_harmonized_data(datasets):
    return apply_analysis_types(pd.concat(datasets.values(), ignore_index=True))


def save_prepared_data(data, path=PREPARED_DATA):
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False, encoding="utf-8")
    return path

def missing_summary(data):
    overall = (
        data.isna().sum().rename("n_ausentes").to_frame()
        .assign(pct_ausentes=lambda frame: 100 * frame["n_ausentes"] / len(data))
        .query("n_ausentes > 0")
        .sort_values("n_ausentes", ascending=False)
    )
    by_year = (
        data.groupby("encuesta_year", observed=True)
        .apply(lambda group: group.isna().sum(), include_groups=False)
        .T
    )
    by_year = by_year.loc[by_year.sum(axis=1).gt(0)]
    return overall, by_year


def weighted_mean(data, value, weight="factor_elevacion"):
    valid = data[[value, weight]].dropna()
    valid = valid[valid[weight] > 0]
    if valid.empty:
        return np.nan
    return np.average(valid[value], weights=valid[weight])


def weighted_percentage(data, category, weight="factor_elevacion"):
    valid = data[[category, weight]].dropna()
    valid = valid[valid[weight] > 0]
    counts = valid.groupby(category, observed=False)[weight].sum()
    return (100 * counts / counts.sum()).rename("porcentaje")


def weighted_group_mean(data, value, groups, weight="factor_elevacion"):
    groups = [groups] if isinstance(groups, str) else list(groups)
    return (
        data.groupby(groups, observed=True)
        .apply(lambda group: weighted_mean(group, value, weight), include_groups=False)
        .rename("media_ponderada")
        .reset_index()
    )


def weighted_composition(data, variable, weight="factor_elevacion", include_missing=True):
    working = data[["encuesta_year", variable, weight]].copy()
    working[weight] = pd.to_numeric(working[weight], errors="coerce")
    working = working[working[weight].notna() & working[weight].gt(0)]
    working[variable] = working[variable].astype("string")
    if include_missing:
        working[variable] = working[variable].fillna("No consta")
    else:
        working = working.dropna(subset=[variable])
    result = (
        working.groupby(["encuesta_year", variable], observed=True)[weight]
        .sum().rename("poblacion_ponderada").reset_index()
    )
    result["porcentaje"] = (
        100 * result["poblacion_ponderada"]
        / result.groupby("encuesta_year")["poblacion_ponderada"].transform("sum")
    )
    return result


def effective_sample_size(weights):
    weights = pd.to_numeric(weights, errors="coerce").dropna()
    weights = weights[weights > 0]
    if weights.empty:
        return np.nan
    return weights.sum() ** 2 / np.square(weights).sum()


def temporal_composition(data, variable, weight="factor_elevacion", weighted=True):
    working = data[["encuesta_year", variable, weight]].copy()
    working[variable] = working[variable].astype("string").fillna("No consta")
    working[weight] = pd.to_numeric(working[weight], errors="coerce")
    working = working[working[weight].notna() & working[weight].gt(0)]
    if weighted:
        result = (
            working.groupby(["encuesta_year", variable], observed=True)[weight]
            .sum().rename("cantidad").reset_index()
        )
    else:
        result = (
            working.groupby(["encuesta_year", variable], observed=True)
            .size().rename("cantidad").reset_index()
        )
    result["porcentaje"] = (
        100 * result["cantidad"]
        / result.groupby("encuesta_year")["cantidad"].transform("sum")
    )
    return result


def weighted_activity_summary(
    data, activity, groups=("encuesta_year",), weight="factor_elevacion"
):
    groups = [groups] if isinstance(groups, str) else list(groups)

    def summarize(group):
        valid = group[[activity, weight]].dropna()
        valid = valid[valid[weight] > 0]
        participants = valid[activity] > 0
        return pd.Series({
            "n_muestra": len(valid),
            "n_efectivo": effective_sample_size(valid[weight]),
            "media_poblacion": np.average(valid[activity], weights=valid[weight]),
            "participacion_pct": 100 * np.average(participants, weights=valid[weight]),
            "media_participantes": (
                np.average(
                    valid.loc[participants, activity],
                    weights=valid.loc[participants, weight],
                ) if participants.any() else np.nan
            ),
        })

    return (
        data.groupby(groups, observed=True)
        .apply(summarize, include_groups=False)
        .reset_index()
    )


def temporal_change_table(
    summary, value, group_columns=None, year="encuesta_year",
    start_year=2003, end_year=2024,
):
    group_columns = [] if group_columns is None else list(group_columns)
    index_columns = group_columns or ["_total"]
    working = summary.copy()
    if not group_columns:
        working["_total"] = "Total"
    wide = working.pivot_table(
        index=index_columns, columns=year, values=value, observed=True
    ).reset_index()
    wide["cambio_absoluto"] = wide[end_year] - wide[start_year]
    wide["cambio_pct"] = np.where(
        wide[start_year].ne(0),
        100 * wide["cambio_absoluto"] / wide[start_year],
        np.nan,
    )
    return wide.drop(columns=["_total"], errors="ignore")

