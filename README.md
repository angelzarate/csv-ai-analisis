# Analizador Inteligente de Solicitudes 🚀🤖

Este es un servicio backend desarrollado en **FastAPI** que actúa como un **Analizador Inteligente de Solicitudes**. Su propósito es procesar archivos CSV con solicitudes de clientes (las cuales suelen contener errores, duplicados o información incompleta) y, mediante un Modelo de Lenguaje Grande (LLM) con salidas estructuradas estrictas, normalizar, categorizar y priorizar cada registro para el equipo de operaciones.

---

## 🛠️ Stack Tecnológico

El proyecto está construido utilizando herramientas modernas, eficientes y preparadas para producción:

*   **Python 3.14:** Lenguaje base por su madurez en el ecosistema de IA y datos.
*   **FastAPI:** Framework web asíncrono de alto rendimiento para la construcción de la API.
*   **Pydantic v2:** Validación de datos y definición de esquemas robustos (*Structured Outputs*).
*   **SQLITE:** Base de datos sencilla para almacenar en "cache" las solicitudes.
*   **SQLAlchemy y Alembic:** Interacción con la base de datos.
*   **Pandas:** Manipulación, limpieza preliminar y parseo eficiente de archivos CSV.
*   **OpenAI SDK :** Integración con modelos de lenguaje (`gpt-4o-mini` o superiores) garantizando respuestas JSON en un 100% conformes al esquema de la aplicación.
*   **Docker:** Contenedor para asegurar la portabilidad
*   **Uvicorn:** Servidor ASGI rápido para ejecutar la aplicación de FastAPI.

---

## 📥 Estructura de Datos (CSV de Entrada)

El servicio espera recibir un archivo `.csv` con las siguientes columnas ( basarse en los ejemplos de 📁examples/*.csv):

| Columna | Descripción |
| :--- | :--- |
| `id_solicitud` | Identificador único del registro (ej. `SOL-001`). |
| `cliente` | Nombre completo del usuario. |
| `canal` | Medio por el que ingresó (WhatsApp, Correo, Web, Llamada). |
| `fecha` | Fecha de captura del caso (`YYYY-MM-DD`). |
| `descripcion` | Texto libre redactado por el cliente o agente (campo crítico). |
| `producto` | Bien o servicio afectado. |
| `ciudad` | Ubicación del usuario o sucursal. |
| `prioridad_manual` | Prioridad inicial asignada en ventanilla (puede estar vacía). |
| `comentarios_adicionales` | Notas internas del sistema o del operador. |

---

## 📤 Estructura de Salida (JSON Generado)

Por cada registro del CSV, el analizador devuelve un objeto JSON:

*   `id_solicitud` *(string)*: El ID original recibido.
*   `categoria_sugerida` *(string)*: Clasificación operativa óptima (Soporte Técnico, Facturación, Queja, etc.).
*   `prioridad_sugerida` *(enum: Alta, Media, Baja)*: Prioridad corregida basada en el impacto crítico del texto.
*   `sentimiento` *(enum: Positivo, Neutral, Negativo)*: Estado de ánimo detectado en el cliente.
*   `resumen` *(string)*: Síntesis de la problemática en un máximo de 15 palabras.
*   `datos_faltantes` *(array de strings)*: Lista de variables necesarias que el cliente omitió mencionar.
*   `requiere_revision_humana` *(boolean)*: Bandera activada (`true`) si el texto es contradictorio, inteligible o corrupto.
*   `justificacion` *(string)*: Explicación racional de las decisiones tomadas por el LLM.
*   `tokens_estimados` *(integer)*: Consumo de tokens reflejado en la transacción.
*   `modelo_utilizado` *(string)*: Identificador del LLM que procesó la fila (ej. `gpt-4o-mini`).

---

## 🐳 Ejecución del Proyecto con Docker

Este proyecto está completamente dockerizado para evitar problemas de dependencias locales.

### Prerrequisitos
*   Tener instalado **Docker** y **Docker Compose**.
*   Contar con una clave de API de OpenAI (`OPENAI_API_KEY`).

### Pasos para levantar el servicio

1. **Clonar el repositorio o situarse en la carpeta del proyecto:**
   ```bash
   cd csv-ai-analisis
   ```

2. **Configurar las variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto y agrega tu API Key de OpenAI (basate del 📄.env.example):
   *Nota:* las variables en .env no usar ""
   ```env
   OPENAI_API_KEY=tu_sk_openai_aqui
   DB_CONNECTION=

   ```

3. **Construir y levantar el contenedor:**
   Ejecuta el siguiente comando en tu terminal para compilar la imagen y levantar el servidor backend:
   ```bash
   docker build -t csv-ai-analisis .
   docker run --name csv-ai-analisis-api --env-file .env -p 8000:8000 csv-ai-analisis
   ```

4. **Verificar el estado del servicio:**
   Una vez que los logs muestren que Uvicorn está corriendo, puedes acceder a la documentación interactiva en tu navegador:
   *   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   *   **Redoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---



## 🚀 Pruebas de la API

Puedes probar los endpoint directamente desde Swagger en `http://localhost:8000/docs` subiendo cualquiera de los archivos CSV generados (como `./examples/solicitudes.csv`), o ejecutando un comando `curl` desde tu terminal:

```bash
curl -X 'POST'   'http://localhost:8000/upload-reqs/'   -H 'accept: application/json'   -H 'Content-Type: multipart/form-data'   -F 'file=@solicitudes.csv;type=text/csv'
```


---

## ❓ Preguntas Frecuentes (FAQ)

### 1. ¿Cómo funciona conceptualmente el Analizador Inteligente?
El servicio actúa como un pipeline de datos semi-estructurados. 
1. **Ingesta:** El usuario carga un archivo CSV a través de la API.
2. **Sanitización:** Pandas procesa el archivo en memoria, limpia los valores nulos (`NaN`) convirtiéndolos en cadenas vacías para que no alteren las plantillas del LLM, ademas de eliminar los duplicados.
3. **Enriquecimiento por IA:** Cada registro se envía a los modelos de OpenAI utilizando la característica de **Structured Outputs**. El backend valida la respuesta contra un esquema estricto de Pydantic antes de compilar el resultado JSON final.

### 2. ¿Cómo evitamos el reprocesamiento innecesario de datos?
Para optimizar costos de API y cómputo local, el backend implementa una estrategia de **Deduplicación en la Ingesta**:
* **Filtro de Duplicados Exactos:** Antes de iterar sobre los registros, Pandas ejecuta una validación rápida con `df.drop_duplicates()`. Si una fila es exactamente idéntica a otra en todas sus columnas, se descarta del procesamiento del LLM y se clona el resultado analizado previamente.
* **Caché de IDs:** Se agrega una capa en base de datos, para almacenar las solicitudes ya procesadas mediante `id_solicitud`. Si el sistema detecta que este registro exacto ya fue procesado con anterioridad, retorna el JSON almacenado directamente desde la BD sin invocar de nuevo al LLM.
Esta capa puede manejada por un Cache en Redis.

### 3. ¿Cómo procesamos las solicitudes en paralelo?
El backend está diseñado de manera nativa sobre un paradigma **asíncrono (`async/await`)** utilizando `asyncio`.
* En lugar de procesar los registros secuencialmente (Fila 1 -> Esperar API -> Fila 2), el sistema genera corrutinas concurrentes utilizando `asyncio.gather()`.
* Esto permite disparar cientos de peticiones HTTP simultáneas hacia la infraestructura de OpenAI, reduciendo el tiempo total de procesamiento de un lote completo de minutos a unos pocos segundos, limitado únicamente por los límites de tasa (*Rate Limits* o RPM) de tu cuenta de OpenAI.

### 4. Selcción del modelo
Para este MVP se opta por utilizar `gpt-4o-mini` ya que ofrece un excelente costo / beneficio, el modelo puede ser cambiado desde `.env`

``` .env
OPENAI_MODEL

```


### 5. ¿Porqué decidí NO utilizar la Batch API de OpenAI?
Aunque la *Batch API* de OpenAI ofrece un 50% de descuento en el costo de los tokens, fue descartada para este microservicio debido a los siguientes requerimientos arquitectónicos:
* **Necesidad de Tiempo Real (Sincronicidad):** La Batch API está diseñada para trabajos en lote asíncronos que pueden demorar **hasta 24 horas** en devolver los resultados. El *Analizador Inteligente de Solicitudes* está pensado para equipos operativos que necesitan clasificar y priorizar el archivo recibido por la mañana de manera **inmediata** para empezar a trabajar al instante.
* **Experiencia de Usuario (UX):** El endpoint de FastAPI está diseñado para responder de forma síncrona (petición-respuesta rápida). Usar Batch API obligaría a implementar una arquitectura compleja con Webhooks, bases de datos de estado intermedio y mecanismos de notificación para avisarle al usuario horas después que su archivo está listo.
* **Estrategia Costo-Beneficio:** Al utilizar el modelo `gpt-4o-mini`, los costos por token ya son extremadamente bajos (fracciones de centavo por registro). El beneficio de velocidad e inmediatez que aporta el procesamiento paralelo asíncrono supera con creces el ahorro marginal de esperar 24 horas por los resultados.