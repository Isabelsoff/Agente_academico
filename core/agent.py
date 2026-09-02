"""Integración del asistente académico con la API de Gemini.

Este módulo configura el cliente de Gemini y proporciona las funciones
necesarias para construir el contexto del asistente y generar respuestas
a partir de los mensajes del estudiante.

El asistente utiliza información del estudiante, memoria reciente de la
conversación y herramientas externas para responder consultas académicas.
"""

from typing import TypedDict

from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from tools.horario_tool import consultar_horario


class Estudiante(TypedDict):
    """Representa la información académica básica de un estudiante."""

    nombre: str
    programa: str
    semestre: str


# Cliente utilizado para realizar solicitudes a la API de Gemini.
client = genai.Client(api_key=GEMINI_API_KEY)


def construir_contexto(estudiante: Estudiante, memoria: str) -> str:
    """Construye las instrucciones de contexto para el asistente académico.

    Combina la información actual del estudiante con la memoria reciente
    de la conversación y las instrucciones que determinan el comportamiento
    del modelo.

    El contexto también indica cuándo debe utilizarse la herramienta
    ``consultar_horario`` y establece restricciones para evitar respuestas
    con información de horarios no disponible.

    Args:
        estudiante: Información académica actual del estudiante.
        memoria: Representación textual de los mensajes recientes de la
            conversación.

    Returns:
        Instrucción de sistema que se enviará al modelo Gemini como contexto.
    """
    return f"""
Eres un asistente académico de la Universidad Católica Luis Amigó.

Ayudas al estudiante con preguntas académicas sencillas.

ESTADO ACTUAL DEL ESTUDIANTE:
Nombre: {estudiante["nombre"]}
Programa: {estudiante["programa"]}
Semestre: {estudiante["semestre"]}

MEMORIA RECIENTE:
{memoria}

Dispones de una herramienta llamada consultar_horario.

Usa consultar_horario cuando el estudiante pregunte por horarios,
clases, días, horas, asignaturas o aulas.

Si puedes responder usando el estado o la memoria, responde directamente.
No inventes información de horarios.
Sé breve, claro y cordial.
""".strip()


def responder(
    mensaje_usuario: str,
    estudiante: Estudiante,
    memoria: str,
) -> str:
    """Genera una respuesta del asistente académico mediante Gemini.

    Construye el contexto de la conversación y envía el mensaje del
    estudiante al modelo configurado de Gemini. El modelo puede utilizar
    la herramienta ``consultar_horario`` cuando la consulta requiere
    información relacionada con el horario académico.

    Args:
        mensaje_usuario: Mensaje enviado por el estudiante.
        estudiante: Información académica actual del estudiante.
        memoria: Representación textual de los mensajes recientes de la
            conversación.

    Returns:
        Respuesta textual generada por Gemini. Si el modelo no devuelve
        contenido textual, se retorna un mensaje predeterminado.
    """
    contexto = construir_contexto(estudiante, memoria)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=mensaje_usuario,
        config=types.GenerateContentConfig(
            system_instruction=contexto,
            tools=[consultar_horario],
        ),
    )

    return response.text or "No fue posible generar una respuesta."