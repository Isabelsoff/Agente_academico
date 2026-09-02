# Agente Académico — MVP con Python, Streamlit y Gemini

Este proyecto implementa un **prototipo sencillo de agente académico** para la Universidad Católica Luis Amigó.

El objetivo es demostrar de forma práctica el flujo:

```text
Usuario
   ↓
Streamlit
   ↓
Contexto + Memoria + Estado
   ↓
Gemini
   ↓
Decisión
   ├── Responder directamente
   └── Usar herramienta
           ↓
    consultar_horario()
           ↓
      horarios.json
           ↓
         Gemini
           ↓
        Respuesta
```

El proyecto utiliza una estructura modular básica para separar responsabilidades sin introducir arquitecturas complejas.

---

# 1. Requisitos previos

Antes de iniciar, verificar que el equipo tenga instalado:

- Python 3.10 o superior.
- `pip`.
- Un editor de código como Visual Studio Code.
- Acceso a Internet.
- Una API Key de Gemini.

Para verificar Python:

```bash
python --version
```

En algunos sistemas puede ser necesario usar:

```bash
python3 --version
```

Para verificar `pip`:

```bash
pip --version
```

---

# 2. Estructura del proyecto

Crear una carpeta principal llamada:

```text
agente_academico
```

La estructura final debe ser:

```text
agente_academico/
│
├── app.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── core/
│   ├── __init__.py
│   ├── agent.py
│   └── state.py
│
├── tools/
│   ├── __init__.py
│   └── horario_tool.py
│
├── data/
│   └── horarios.json
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

Cada carpeta tiene una responsabilidad específica:

| Elemento | Responsabilidad |
|---|---|
| `app.py` | Interfaz Streamlit y flujo principal |
| `config/` | Configuración del proyecto |
| `core/` | Lógica del agente, memoria y estado |
| `tools/` | Herramientas que puede usar el agente |
| `data/` | Datos utilizados por las herramientas |
| `.env` | Variables sensibles como API Key |
| `requirements.txt` | Dependencias del proyecto |

---

# 3. Crear la carpeta del proyecto

Desde una terminal:

```bash
mkdir agente_academico
cd agente_academico
```

---

# 4. Crear el entorno virtual

Es recomendable ejecutar cada proyecto Python dentro de un entorno virtual.

Crearlo con:

```bash
python -m venv venv
```

La estructura quedará temporalmente así:

```text
agente_academico/
├── venv/
└── ...
```

La carpeta `venv` no debe compartirse ni subirse a Git.

---

# 5. Activar el entorno virtual

## Windows — CMD

```bash
venv\Scripts\activate
```

## Windows — PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

## Linux o macOS

```bash
source venv/bin/activate
```

Cuando esté correctamente activado, la terminal mostrará algo similar a:

```text
(venv) C:\proyectos\agente_academico>
```

---

# 6. Crear `requirements.txt`

Crear el archivo:

```text
requirements.txt
```

Agregar:

```text
streamlit
google-genai
python-dotenv
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Las dependencias cumplen estas funciones:

| Librería | Función |
|---|---|
| `streamlit` | Construye la interfaz web |
| `google-genai` | Permite utilizar Gemini |
| `python-dotenv` | Permite leer variables del archivo `.env` |

---

# 7. Crear el archivo `.env`

En la raíz del proyecto crear:

```text
.env
```

Agregar:

```text
GEMINI_API_KEY=TU_API_KEY_AQUI
```

Posteriormente reemplazar:

```text
TU_API_KEY_AQUI
```

por la API Key real de Gemini.

Ejemplo:

```text
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXX
```

La API Key no debe escribirse directamente dentro del código Python.

---

# 8. Crear `.gitignore`

Crear:

```text
.gitignore
```

Agregar:

```text
venv/
.venv/
__pycache__/
*.pyc
.env
```

Esto evita subir al repositorio:

- el entorno virtual;
- archivos temporales de Python;
- la API Key.

---

# 9. Crear la carpeta `config`

Crear:

```text
config/
```

Dentro crear:

```text
__init__.py
settings.py
```

`__init__.py` puede quedar vacío.

El archivo:

```text
config/settings.py
```

debe contener:

```python
import os
from dotenv import load_dotenv


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = "gemini-2.5-flash"


def validar_configuracion() -> None:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "TU_API_KEY_AQUI":
        raise ValueError(
            "Configura una API Key válida en el archivo .env "
            "usando GEMINI_API_KEY."
        )
```

Este módulo centraliza la configuración de Gemini.

De esta forma, si posteriormente se cambia el modelo, no es necesario modificar diferentes archivos.

---

# 10. Crear la carpeta `data`

Crear:

```text
data/
```

Dentro crear:

```text
horarios.json
```

Agregar datos ficticios:

```json
[
  {
    "dia": "lunes",
    "asignatura": "Bases de Datos",
    "hora": "8:00 a. m. - 10:00 a. m.",
    "aula": "Aula 301"
  },
  {
    "dia": "lunes",
    "asignatura": "Programación",
    "hora": "10:00 a. m. - 12:00 m.",
    "aula": "Laboratorio 2"
  },
  {
    "dia": "martes",
    "asignatura": "Ingeniería de Software",
    "hora": "6:00 p. m. - 8:00 p. m.",
    "aula": "Aula 405"
  },
  {
    "dia": "miércoles",
    "asignatura": "Matemáticas Discretas",
    "hora": "8:00 a. m. - 10:00 a. m.",
    "aula": "Aula 203"
  },
  {
    "dia": "jueves",
    "asignatura": "Bases de Datos",
    "hora": "6:00 p. m. - 8:00 p. m.",
    "aula": "Laboratorio 1"
  },
  {
    "dia": "viernes",
    "asignatura": "Programación",
    "hora": "2:00 p. m. - 4:00 p. m.",
    "aula": "Laboratorio 3"
  }
]
```

En este MVP el archivo JSON simula una fuente institucional de información.

---

# 11. Crear la herramienta del agente

Crear la carpeta:

```text
tools/
```

Dentro crear:

```text
__init__.py
horario_tool.py
```

`__init__.py` puede quedar vacío.

En:

```text
tools/horario_tool.py
```

agregar:

```python
import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "horarios.json"
)


def consultar_horario(consulta: str) -> list[dict]:
    """
    Consulta el horario académico ficticio.

    Args:
        consulta: Día de la semana o nombre de la asignatura.

    Returns:
        Lista de clases que coinciden con la consulta.
    """

    with DATA_FILE.open(
        "r",
        encoding="utf-8"
    ) as archivo:

        horarios = json.load(archivo)

    criterio = consulta.lower().strip()

    return [
        clase
        for clase in horarios
        if criterio in clase["dia"].lower()
        or criterio in clase["asignatura"].lower()
    ]
```

Esta función representa una **herramienta del agente**.

Gemini podrá utilizarla cuando determine que necesita consultar información de horarios.

---

# 12. Crear la gestión de estado y memoria

Crear:

```text
core/
```

Dentro crear:

```text
__init__.py
state.py
agent.py
```

`__init__.py` puede quedar vacío.

En:

```text
core/state.py
```

agregar:

```python
import re

import streamlit as st


ESTUDIANTE_INICIAL = {
    "nombre": "No registrado",
    "programa": "No registrado",
    "semestre": "No registrado",
}


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

}


def inicializar_estado() -> None:

    if "estudiante" not in st.session_state:

        st.session_state.estudiante = (
            ESTUDIANTE_INICIAL.copy()
        )

    if "mensajes" not in st.session_state:

        st.session_state.mensajes = []


def actualizar_estado_estudiante(
    texto: str
) -> None:

    texto_lower = texto.lower()

    patron_nombre = (
        r"(?:soy|me llamo)\s+"
        r"([A-Za-zÁÉÍÓÚáéíóúÑñ]+)"
    )

    coincidencia = re.search(
        patron_nombre,
        texto,
        re.IGNORECASE
    )

    if coincidencia:

        st.session_state.estudiante[
            "nombre"
        ] = coincidencia.group(1).capitalize()

    if (
        "ingeniería de sistemas" in texto_lower
        or "ingenieria de sistemas" in texto_lower
    ):

        st.session_state.estudiante[
            "programa"
        ] = "Ingeniería de Sistemas"

    for descripcion, numero in SEMESTRES.items():

        if descripcion in texto_lower:

            st.session_state.estudiante[
                "semestre"
            ] = numero

            break


def agregar_mensaje(
    role: str,
    content: str
) -> None:

    st.session_state.mensajes.append(
        {
            "role": role,
            "content": content
        }
    )


def obtener_memoria(
    limite: int = 6
) -> str:

    mensajes = (
        st.session_state.mensajes[-limite:]
    )

    return "\n".join(
        f"{mensaje['role']}: "
        f"{mensaje['content']}"
        for mensaje in mensajes
    )


def reiniciar_estado() -> None:

    st.session_state.mensajes = []

    st.session_state.estudiante = (
        ESTUDIANTE_INICIAL.copy()
    )
```

Este archivo administra dos conceptos diferentes.

## Estado

Representa información estructurada del estudiante:

```python
{
    "nombre": "Carlos",
    "programa": "Ingeniería de Sistemas",
    "semestre": "3"
}
```

## Memoria

Representa los mensajes recientes de la conversación.

Ejemplo:

```text
user: Hola, soy Carlos.
assistant: Hola Carlos...
user: Estoy en tercer semestre.
assistant: Perfecto...
```

Para mantener el prototipo sencillo se conservan únicamente los últimos:

```python
6
```

mensajes.

---

# 13. Crear la lógica del agente

Abrir:

```text
core/agent.py
```

Agregar:

```python
from google import genai
from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

from tools.horario_tool import (
    consultar_horario
)


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def construir_contexto(
    estudiante: dict,
    memoria: str
) -> str:

    return f"""
Eres un asistente académico de la
Universidad Católica Luis Amigó.

Ayudas al estudiante con preguntas
académicas sencillas.

ESTADO ACTUAL DEL ESTUDIANTE:

Nombre: {estudiante["nombre"]}
Programa: {estudiante["programa"]}
Semestre: {estudiante["semestre"]}

MEMORIA RECIENTE:

{memoria}

Dispones de una herramienta llamada
consultar_horario.

Usa consultar_horario cuando el estudiante
pregunte por:

- horarios;
- clases;
- días;
- horas;
- asignaturas;
- aulas.

Si puedes responder utilizando el estado
o la memoria, responde directamente.

No inventes información de horarios.

Sé breve, claro y cordial.
""".strip()


def responder(
    mensaje_usuario: str,
    estudiante: dict,
    memoria: str
) -> str:

    contexto = construir_contexto(
        estudiante,
        memoria
    )

    response = client.models.generate_content(

        model=GEMINI_MODEL,

        contents=mensaje_usuario,

        config=types.GenerateContentConfig(

            system_instruction=contexto,

            tools=[
                consultar_horario
            ]

        )
    )

    return (
        response.text
        or "No fue posible generar una respuesta."
    )
```

Este módulo contiene el núcleo del agente.

Aquí se conectan:

```text
Contexto
   +
Estado
   +
Memoria
   +
Gemini
   +
Herramientas
```

---

# 14. Crear `app.py`

Finalmente crear:

```text
app.py
```

Agregar:

```python
import streamlit as st

from config.settings import (
    validar_configuracion
)

from core.agent import responder

from core.state import (
    agregar_mensaje,
    actualizar_estado_estudiante,
    inicializar_estado,
    obtener_memoria,
    reiniciar_estado,
)


# ----------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------

st.set_page_config(
    page_title="Agente Académico",
    page_icon="🎓",
)


try:

    validar_configuracion()

except ValueError as error:

    st.error(str(error))

    st.stop()


inicializar_estado()


# ----------------------------------------------
# INTERFAZ
# ----------------------------------------------

st.title(
    "🎓 Agente Académico"
)

st.caption(
    "Universidad Católica Luis Amigó"
)

st.write(
    "MVP con Gemini, contexto, memoria, "
    "estado y una herramienta."
)


# ----------------------------------------------
# ESTADO DEL ESTUDIANTE
# ----------------------------------------------

with st.sidebar:

    st.subheader(
        "Estado del estudiante"
    )

    estudiante = (
        st.session_state.estudiante
    )

    st.write(
        "Nombre:",
        estudiante["nombre"]
    )

    st.write(
        "Programa:",
        estudiante["programa"]
    )

    st.write(
        "Semestre:",
        estudiante["semestre"]
    )

    st.divider()

    if st.button(
        "Reiniciar conversación"
    ):

        reiniciar_estado()

        st.rerun()


# ----------------------------------------------
# HISTORIAL
# ----------------------------------------------

for mensaje in (
    st.session_state.mensajes
):

    with st.chat_message(
        mensaje["role"]
    ):

        st.markdown(
            mensaje["content"]
        )


# ----------------------------------------------
# MENSAJE DEL USUARIO
# ----------------------------------------------

prompt = st.chat_input(
    "Escribe tu pregunta académica..."
)


if prompt:

    with st.chat_message("user"):

        st.markdown(prompt)


    actualizar_estado_estudiante(
        prompt
    )


    agregar_mensaje(
        "user",
        prompt
    )


    try:

        respuesta = responder(

            mensaje_usuario=prompt,

            estudiante=(
                st.session_state.estudiante
            ),

            memoria=obtener_memoria(),

        )

    except Exception as error:

        respuesta = (
            "Ocurrió un error al consultar "
            f"Gemini: {error}"
        )


    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            respuesta
        )


    agregar_mensaje(
        "assistant",
        respuesta
    )
```

---

# 15. Verificar la estructura

Antes de ejecutar, revisar que el proyecto tenga exactamente una estructura similar a:

```text
agente_academico/
│
├── app.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── core/
│   ├── __init__.py
│   ├── agent.py
│   └── state.py
│
├── tools/
│   ├── __init__.py
│   └── horario_tool.py
│
├── data/
│   └── horarios.json
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 16. Configurar la API Key

Verificar nuevamente:

```text
.env
```

Debe contener:

```text
GEMINI_API_KEY=TU_API_KEY_REAL
```

No utilizar comillas.

Ejemplo correcto:

```text
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXX
```

---

# 17. Ejecutar la aplicación

Verificar primero que el entorno virtual esté activo.

Ejemplo:

```text
(venv)
```

Después ejecutar:

```bash
streamlit run app.py
```

Streamlit iniciará un servidor local.

Normalmente mostrará:

```text
Local URL: http://localhost:8501
```

Abrir esa dirección en el navegador.

---

# 18. Pruebas funcionales

Realizar las pruebas en el siguiente orden.

## Prueba 1 — Nombre y programa

Escribir:

```text
Hola, soy Carlos y estudio Ingeniería de Sistemas.
```

En el panel lateral debería aparecer:

```text
Nombre: Carlos
Programa: Ingeniería de Sistemas
Semestre: No registrado
```

---

# 19. Prueba 2 — Estado del estudiante

Escribir:

```text
Estoy en tercer semestre.
```

El estado debería actualizarse a:

```text
Nombre: Carlos
Programa: Ingeniería de Sistemas
Semestre: 3
```

---

# 20. Prueba 3 — Uso de herramienta

Escribir:

```text
¿Qué clases tengo el lunes?
```

El agente deberá utilizar:

```python
consultar_horario("lunes")
```

La herramienta encontrará:

```text
Bases de Datos
8:00 a. m. - 10:00 a. m.

Programación
10:00 a. m. - 12:00 m.
```

Gemini construirá la respuesta final.

---

# 21. Prueba 4 — Consulta por asignatura

Escribir:

```text
¿A qué hora tengo Bases de Datos?
```

La herramienta podrá consultar:

```python
consultar_horario(
    "Bases de Datos"
)
```

y devolver las coincidencias encontradas en `horarios.json`.

---

# 22. Prueba 5 — Memoria y estado

Escribir:

```text
¿Recuerdas qué carrera estudio?
```

El agente debería responder:

```text
Ingeniería de Sistemas.
```

En este caso no necesita consultar el archivo de horarios.

Puede utilizar directamente el estado del estudiante.

---

# 23. Flujo interno del prototipo

Cuando el estudiante escribe:

```text
¿Qué clases tengo el lunes?
```

ocurre el siguiente proceso:

```text
1. Usuario escribe en Streamlit
              ↓
2. app.py recibe el mensaje
              ↓
3. state.py actualiza estado/memoria
              ↓
4. agent.py construye el contexto
              ↓
5. Gemini interpreta la solicitud
              ↓
6. Gemini determina que necesita
   consultar información externa
              ↓
7. Ejecuta consultar_horario()
              ↓
8. horario_tool.py lee horarios.json
              ↓
9. La herramienta devuelve los datos
              ↓
10. Gemini genera la respuesta
              ↓
11. Streamlit muestra el resultado
```

---

# 24. Responsabilidad de cada archivo

## `app.py`

Controla:

- interfaz;
- entrada del usuario;
- visualización del historial;
- visualización del estado;
- coordinación del flujo.

No debe contener la lógica principal del agente.

---

## `config/settings.py`

Controla:

- variables de entorno;
- API Key;
- nombre del modelo;
- validación de configuración.

---

## `core/agent.py`

Controla:

- contexto del agente;
- conexión con Gemini;
- herramientas disponibles;
- generación de respuestas.

---

## `core/state.py`

Controla:

- estado del estudiante;
- memoria conversacional;
- actualización de datos;
- reinicio de conversación.

---

## `tools/horario_tool.py`

Controla:

```python
consultar_horario()
```

Esta función representa una capacidad externa del agente.

---

## `data/horarios.json`

Contiene los datos ficticios utilizados por la herramienta.

---

# 25. Problemas comunes

## Error: `python no se reconoce como un comando`

Python no está instalado o no está agregado al `PATH`.

Verificar:

```bash
python --version
```

---

## Error al activar PowerShell

Si aparece una restricción de ejecución, abrir PowerShell como usuario y ejecutar:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Después:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Error: `No module named streamlit`

El entorno virtual probablemente no está activo o las dependencias no fueron instaladas.

Ejecutar:

```bash
pip install -r requirements.txt
```

---

## Error: API Key no encontrada

Verificar que exista:

```text
.env
```

en la raíz del proyecto.

Debe contener:

```text
GEMINI_API_KEY=TU_API_KEY_REAL
```

---

## Error relacionado con Gemini

Comprobar:

1. que la API Key sea válida;
2. que exista conexión a Internet;
3. que el modelo configurado esté disponible;
4. que `google-genai` esté instalado.

Actualizar la librería si es necesario:

```bash
pip install --upgrade google-genai
```

---

## Streamlit no abre automáticamente

Copiar en el navegador la dirección mostrada por la terminal:

```text
http://localhost:8501
```

---

# 26. Detener la aplicación

En la terminal donde Streamlit está ejecutándose presionar:

```text
Ctrl + C
```

---

# 27. Desactivar el entorno virtual

Cuando termine el trabajo:

```bash
deactivate
```

---

# 28. Resultado esperado

Al finalizar debe existir un agente académico capaz de:

- conversar con el estudiante;
- recordar algunos mensajes recientes;
- conservar nombre, programa y semestre;
- consultar información externa;
- decidir cuándo utilizar una herramienta;
- responder utilizando Gemini.

El prototipo permite demostrar de manera directa los componentes fundamentales:

```text
Usuario
   ↓
Interfaz
   ↓
Contexto
   +
Memoria
   +
Estado
   ↓
LLM
   ↓
Herramientas
   ↓
Datos externos
   ↓
Respuesta
```

---

# 29. Alcance del MVP

Este proyecto es intencionalmente sencillo.

No incluye:

- bases de datos;
- autenticación;
- RAG;
- bases vectoriales;
- LangChain;
- múltiples agentes;
- FastAPI;
- Docker;
- microservicios;
- despliegue en producción.

La finalidad es comprender primero el funcionamiento de un agente antes de incorporar arquitecturas y capacidades adicionales.