"""Utilidades para la consulta de horarios académicos.

Este módulo proporciona funciones para cargar y consultar la información
de horarios almacenada en el archivo JSON de datos de la aplicación.
"""

import json
from pathlib import Path
from typing import TypedDict


class Clase(TypedDict):
    """Representa una clase dentro del horario académico."""

    dia: str
    asignatura: str
    hora: str
    aula: str


# Ruta al archivo que contiene la información de los horarios académicos.
DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "horarios.json"


def consultar_horario(consulta: str):
    """Busca clases en el horario académico según un criterio de consulta.

    La búsqueda no distingue entre mayúsculas y minúsculas y permite
    coincidencias parciales por día de la semana o nombre de asignatura.

    Args:
        consulta: Día de la semana, nombre de la asignatura o fragmento
            de texto utilizado como criterio de búsqueda.

    Returns:
        Lista de clases que coinciden con el criterio de búsqueda.
        Devuelve una lista vacía si no se encuentran coincidencias.

    Raises:
        FileNotFoundError: Si el archivo de horarios no existe.
        json.JSONDecodeError: Si el archivo contiene un JSON inválido.
    """
    with DATA_FILE.open("r", encoding="utf-8") as archivo:
        horarios: list[Clase] = json.load(archivo)

    criterio = consulta.lower().strip()

    resultados = [
        clase
        for clase in horarios
        if criterio in clase["dia"].lower()
        or criterio in clase["asignatura"].lower()
    ]

    return {
        "consulta": consulta,
        "resultados": resultados,
        "cantidad": len(resultados),
    }