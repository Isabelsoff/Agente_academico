# Guía Paso a Paso para Desplegar el Agente Académico en Render

Esta guía detalla el proceso completo para desplegar la aplicación **Agente Académico** en la plataforma en la nube **[Render](https://render.com)**.

---

## 1. Resumen de la Estructura del Proyecto

El proyecto está estructurado como una aplicación web interactiva desarrollada con **Streamlit** y potenciada por el SDK oficial de **Google GenAI (Gemini)**.

```text
agente_academico_v01/
│
├── app.py                  # Punto de entrada de la interfaz Streamlit
├── requirements.txt        # Dependencias de Python (streamlit, google-genai, python-dotenv)
├── .env                    # Variables de entorno locales (NO se sube a Git)
├── .gitignore              # Archivos y carpetas excluidos del control de versiones
│
├── config/
│   ├── __init__.py
│   └── settings.py         # Carga y validación de GEMINI_API_KEY y modelo
│
├── core/
│   ├── __init__.py
│   ├── agent.py            # Lógica del agente y orquestación con Gemini
│   └── state.py            # Gestión del estado de sesión y memoria conversacional
│
├── data/
│   └── horarios.json       # Datos estáticos de asignaturas y horarios
│
└── tools/
    ├── __init__.py
    └── horario_tool.py     # Tool de consulta de horarios académicos
```

### Componentes Clave para el Despliegue:
1. **Punto de Entrada**: `app.py`.
2. **Dependencias** (`requirements.txt`):
   - `streamlit`
   - `google-genai`
   - `python-dotenv`
3. **Variables de Entorno Requeridas**:
   - `GEMINI_API_KEY`: API Key generada en [Google AI Studio](https://aistudio.google.com/).

---

## 2. Requisitos Previos

Antes de comenzar, asegúrate de contar con:
1. Una cuenta activa en **[GitHub](https://github.com/)** (o GitLab).
2. Una cuenta en **[Render](https://render.com/)** (puedes registrarte con tu cuenta de GitHub).
3. Tu **API Key de Gemini** activa.
4. **Git** instalado en tu computadora.

---

## 3. Paso 1: Subir el Proyecto a GitHub

Render desplegará tu aplicación directamente desde un repositorio de Git.

### 3.1. Validar el archivo `.gitignore`
Asegúrate de que el archivo `.gitignore` en la raíz del proyecto contenga al menos:
```gitignore
venv/
.venv/
__pycache__/
*.pyc
.env
```
> ⚠️ **Importante**: El archivo `.env` nunca debe subirse al repositorio público para proteger tu clave de API.

### 3.2. Inicializar el repositorio y hacer commit
Abre una terminal en la carpeta del proyecto (`agente_academico_v01`) y ejecuta:

```bash
# Inicializar repositorio git si aún no está inicializado
git init

# Agregar los archivos al control de versiones
git add .

# Crear el primer commit
git commit -m "feat: versión inicial del agente académico"
```

### 3.3. Crear repositorio en GitHub y subir el código
1. Ve a [GitHub](https://github.com/new) y crea un nuevo repositorio (por ejemplo, `agente-academico`).
2. Vincula tu repositorio local con GitHub y sube los cambios:

```bash
git branch -M main
git remote add origin https://github.com/TU_USUARIO/agente-academico.git
git push -u origin main
```

---

## 4. Paso 2: Crear el Servicio Web en Render

1. Inicia sesión en el [Panel de Control de Render](https://dashboard.render.com/).
2. Haz clic en el botón **New +** (arriba a la derecha) y selecciona **Web Service**.
3. Selecciona **Build and deploy from a Git repository** y haz clic en **Next**.
4. Conecta tu cuenta de GitHub si aún no lo has hecho y busca el repositorio `agente-academico`. Haz clic en **Connect**.

---

## 5. Paso 3: Configurar los Parámetros del Servicio

En el formulario de configuración del Web Service, completa los campos con los siguientes valores:

| Campo | Valor Recomendado | Explicación |
| :--- | :--- | :--- |
| **Name** | `agente-academico` | Nombre que identificará tu servicio en Render. |
| **Region** | `Ohio (US East)` o `Oregon (US West)` | Elige la región más cercana a ti. |
| **Branch** | `main` | Rama principal del repositorio a desplegar. |
| **Runtime** | `Python 3` | Entorno de ejecución. |
| **Build Command** | `pip install -r requirements.txt` | Comando para instalar las dependencias. |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` | Comando de arranque para Streamlit. |
| **Instance Type** | `Free` | Plan gratuito de Render. |

> 📌 **¿Por qué este Start Command?**
> Render asigna dinámicamente un puerto a través de la variable `$PORT`. Con los argumentos `--server.port $PORT` y `--server.address 0.0.0.0`, Streamlit escucha en la interfaz y puerto correctos exigidos por el proxy de Render.

---

## 6. Paso 4: Configurar Variables de Entorno (Environment Variables)

Desplázate hacia abajo hasta la sección **Environment Variables** y agrega las siguientes variables:

1. **Clave requerida:**
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `TU_API_KEY_REAL_DE_GEMINI` (pega aquí la clave obtenida de Google AI Studio).

2. **Versión de Python recomendada (Opcional pero aconsejada):**
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.11.8`

---

## 7. Paso 5: Desplegar y Verificar

1. Haz clic en el botón **Create Web Service** al final de la página.
2. Render iniciará automáticamente el proceso de construcción (*Build*):
   - Clonará el repositorio.
   - Instalará las dependencias de `requirements.txt`.
   - Ejecutará el comando de inicio de Streamlit.
3. Observa los logs en tiempo real. Cuando veas mensajes similares a:
   ```text
   ==> Uploading build...
   ==> Build successful 🎉
   ==> Deploying...
   ==> Starting service with 'streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true'
   You can now view your Streamlit app in your browser.
   ==> Your service is live 🚀
   ```
4. Haz clic en el enlace público proporcionado en la parte superior izquierda (por ejemplo, `https://agente-academico-xxxx.onrender.com`).
5. **Prueba tu agente**:
   - Envía un mensaje con tu nombre y programa (ej. *"Hola, soy Juan de Ingeniería de Sistemas"*).
   - Consulta un horario (ej. *"¿En qué horario se dicta Algoritmos y Estructura de Datos?"*).
   - Verifica que el panel lateral (*Estado del estudiante*) se actualice y que la herramienta de consulta de horarios devuelva los datos correctos.

---

## 8. Opción Avanzada: Despliegue Automático mediante `render.yaml` (Blueprint)

Si prefieres configurar la infraestructura como código (Infrastructure as Code), puedes crear un archivo `render.yaml` en la raíz del proyecto con la siguiente estructura:

```yaml
services:
  - type: web
    name: agente-academico
    runtime: python
    plan: free
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.8
      - key: GEMINI_API_KEY
        sync: false # Deberás ingresar el valor secretamente desde el dashboard de Render
```

Luego, en Render seleccionas **New +** > **Blueprint** y conectas el repositorio.

---

## 9. Preguntas Frecuentes y Solución de Problemas (Troubleshooting)

### 🔴 Error: `ValueError: Configura una API Key válida en el archivo .env usando GEMINI_API_KEY`
- **Causa**: No se configuró la variable de entorno `GEMINI_API_KEY` en Render o conserva el texto de ejemplo.
- **Solución**: Ve a la pestaña **Environment** en el panel de tu servicio en Render, agrega o edita `GEMINI_API_KEY` con tu clave válida y haz clic en **Save Changes** (esto disparará un re-despliegue automático).

### 🔴 Error: `Port scan timeout` o `Bad Gateway (502)`
- **Causa**: Streamlit se está ejecutando en el puerto por defecto `8501` o en `localhost` en lugar del puerto dinámico de Render.
- **Solución**: Asegúrate de que el **Start Command** tenga exactamente:
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

### ⏱️ La primera consulta tarda unos segundos en cargar (Cold Start)
- **Causa**: En el plan gratuito de Render (*Free Tier*), los servicios web entran en reposo si no reciben tráfico durante 15 minutos.
- **Comportamiento**: Al recibir una nueva petición, Render reactiva la instancia, lo cual puede tardar entre 30 y 50 segundos en el primer acceso. Las siguientes consultas responderán de inmediato.
