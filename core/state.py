"""Gestión del estado de sesión y memoria del estudiante en Streamlit.

Este módulo administra la información básica del estudiante y el historial
de mensajes almacenados en ``st.session_state``.

También incluye utilidades para identificar datos del estudiante a partir
de texto libre, construir una memoria reciente de la conversación y
reiniciar el estado de la sesión.
"""

import re

import streamlit as st


# Estado inicial utilizado cuando aún no se ha identificado al estudiante.
ESTUDIANTE_INICIAL = {
    "nombre": "No registrado",
    "programa": "No registrado",
    "semestre": "No registrado",
}


# Equivalencias utilizadas para identificar el semestre mencionado
# por el estudiante, tanto en formato textual como numérico.
SEMESTRES = {
    "primer semestre": "1",
    "segundo semestre": "2",
    "tercer semestre": "3",
    "cuarto semestre": "4",
    "quinto semestre": "5",
    "sexto semestre": "6",
    "séptimo semestre": "7",
    "septimo semestre": "7",
    "octavo semestre": "8",
    "noveno semestre": "9",
    "décimo semestre": "10",
    "decimo semestre": "10",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "10": "10",
}


def inicializar_estado() -> None:
    """Inicializa las variables necesarias en el estado de sesión.

    Crea la información inicial del estudiante y el historial de mensajes
    únicamente cuando dichas variables aún no existen en
    ``st.session_state``.

    Esto permite conservar la información entre las distintas ejecuciones
    de la aplicación Streamlit dentro de una misma sesión.
    """
    if "estudiante" not in st.session_state:
        st.session_state.estudiante = ESTUDIANTE_INICIAL.copy()

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_estado_estudiante(texto: str) -> None:
    """Actualiza los datos del estudiante identificados en un texto.

    Analiza el contenido recibido para detectar el nombre del estudiante,
    su programa académico y el semestre que cursa. Los valores encontrados
    se almacenan directamente en ``st.session_state.estudiante``.

    La búsqueda del programa y del semestre no distingue entre mayúsculas
    y minúsculas. También se contemplan variantes con y sin tildes para
    algunos valores.

    Args:
        texto: Mensaje escrito por el estudiante del cual se intentará
            extraer información personal y académica.
    """
    texto_lower = texto.lower()

    patron_nombre = r"(?:soy|me llamo)\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+)"
    coincidencia = re.search(patron_nombre, texto, re.IGNORECASE)

    if coincidencia:
        st.session_state.estudiante["nombre"] = coincidencia.group(1).capitalize()

    if (
        "ingeniería de sistemas" in texto_lower
        or "ingenieria de sistemas" in texto_lower
    ):
        st.session_state.estudiante["programa"] = "Ingeniería de Sistemas"

    for descripcion, numero in SEMESTRES.items():
        if descripcion in texto_lower:
            st.session_state.estudiante["semestre"] = numero
            break


def agregar_mensaje(role: str, content: str) -> None:
    """Agrega un mensaje al historial de conversación de la sesión.

    Args:
        role: Rol asociado al mensaje, por ejemplo ``"user"`` o
            ``"assistant"``.
        content: Contenido textual del mensaje que se desea almacenar.
    """
    st.session_state.mensajes.append(
        {
            "role": role,
            "content": content,
        }
    )


def obtener_memoria(limite: int = 6) -> str:
    """Construye una representación textual de los mensajes recientes.

    Recupera los últimos mensajes almacenados en la sesión y los convierte
    en una cadena de texto que puede utilizarse como contexto o memoria
    conversacional.

    Args:
        limite: Número máximo de mensajes recientes que se incluirán.
            Por defecto se utilizan los últimos 6 mensajes.

    Returns:
        Cadena con los mensajes recientes en formato ``"role: content"``,
        separados por saltos de línea. Devuelve una cadena vacía si no
        existen mensajes almacenados.
    """
    mensajes = st.session_state.mensajes[-limite:]

    return "\n".join(
        f"{mensaje['role']}: {mensaje['content']}"
        for mensaje in mensajes
    )


def reiniciar_estado() -> None:
    """Restablece la información de la sesión a sus valores iniciales.

    Elimina el historial de conversación y reemplaza la información del
    estudiante por una nueva copia de ``ESTUDIANTE_INICIAL``.
    """
    st.session_state.mensajes = []
    st.session_state.estudiante = ESTUDIANTE_INICIAL.copy()