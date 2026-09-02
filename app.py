"""Interfaz principal del agente académico desarrollado con Streamlit.

Este módulo configura y ejecuta la interfaz web del asistente académico.
Gestiona la visualización del estado del estudiante, el historial de
conversación y la interacción entre el usuario y el agente basado en Gemini.

El flujo principal de la aplicación incluye:

- Validación de la configuración requerida.
- Inicialización del estado de sesión.
- Visualización de la información académica del estudiante.
- Renderizado del historial de conversación.
- Captura de nuevos mensajes del usuario.
- Actualización del estado y la memoria conversacional.
- Generación de respuestas mediante el agente académico.
- Reinicio de la conversación cuando el usuario lo solicita.
"""

import streamlit as st

from config.settings import validar_configuracion
from core.agent import responder
from core.state import (
    agregar_mensaje,
    actualizar_estado_estudiante,
    inicializar_estado,
    obtener_memoria,
    reiniciar_estado,
)


st.set_page_config(
    page_title="Agente Académico",
    page_icon="🤖",
)


# Valida que las variables necesarias para utilizar Gemini estén configuradas.
try:
    validar_configuracion()
except ValueError as error:
    st.error(str(error))
    st.stop()


# Inicializa el estado persistente de la sesión de Streamlit.
inicializar_estado()


# Encabezado principal de la aplicación.
st.title("Agente Académico")
st.caption("Universidad Católica Luis Amigó")
st.write("MVP con Gemini, contexto, memoria, estado y una herramienta.")


# Panel lateral con la información académica conocida del estudiante.
with st.sidebar:
    st.subheader("Estado del estudiante")

    estudiante = st.session_state.estudiante

    st.write("Nombre:", estudiante["nombre"])
    st.write("Programa:", estudiante["programa"])
    st.write("Semestre:", estudiante["semestre"])

    st.divider()

    if st.button("Reiniciar conversación"):
        reiniciar_estado()
        st.rerun()


# Renderiza el historial de mensajes almacenados en la sesión.
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])


# Captura una nueva consulta del estudiante.
prompt = st.chat_input("Escribe tu pregunta académica...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    actualizar_estado_estudiante(prompt)
    agregar_mensaje("user", prompt)

    try:
        respuesta = responder(
            mensaje_usuario=prompt,
            estudiante=st.session_state.estudiante,
            memoria=obtener_memoria(),
        )
    except Exception as error:
        respuesta = f"Ocurrió un error al consultar Gemini: {error}"

    with st.chat_message("assistant"):
        st.markdown(respuesta)

    agregar_mensaje("assistant", respuesta)

    st.rerun()