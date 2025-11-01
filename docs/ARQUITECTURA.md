# Arquitectura del Sistema

## 📐 Visión General

El **AICON Assistant API** es un microservicio de conversación inteligente basado en RAG (Retrieval Augmented Generation) que forma parte del ecosistema **ImmobAI**. Este servicio está diseñado para procesar consultas de usuarios utilizando documentación específica de la inmobiliaria, proporcionando respuestas contextuales y precisas mediante streaming.

## 🏗️ Arquitectura de Microservicios

### Contexto dentro de ImmobAI

Este servicio es parte de una arquitectura de microservicios que incluye:

- **Frontend Angular**: Interface web para usuarios e inmobiliarias
- **Backend Principal**: API de gestión inmobiliaria (propiedades, leads, asesores)
- **AICON Assistant API** (Este servicio): Motor de chat conversacional con RAG
- **WhatsApp Assistant**: Integración externa para atención de clientes
- **Servicios de Almacenamiento**: Google Cloud Storage y PostgreSQL

### Responsabilidades del Servicio

- ✅ Búsqueda semántica en documentos almacenados
- ✅ Generación de respuestas contextuales usando Gemini
- ✅ Streaming de respuestas en tiempo real
- ✅ Gestión de sesiones de conversación
- ✅ Persistencia de historial de chat
- ✅ Integración con Vertex AI Search (Discovery Engine)

## 🔧 Stack Tecnológico

### Backend
- **Framework**: Django 5.1.6 con Django REST Framework
- **Lenguaje**: Python 3.10
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)

### IA y Machine Learning
- **LLM**: Google Gemini 1.5 Pro-002
- **RAG Framework**: Langchain Google Community
- **Búsqueda**: Vertex AI Search (Discovery Engine)
- **Streaming**: Vertex AI Generative Models

### Infraestructura Cloud
- **Plataforma**: Google Cloud Platform
- **Contenedorización**: Docker
- **Despliegue**: Google Cloud Run (Knative)
- **CI/CD**: Google Cloud Build
- **Storage**: Google Cloud Storage
- **Sistema de Archivos**: GCS FUSE

### Librerías Principales
```python
langchain-google-community==1.0.7  # Conexión con Vertex AI Search
langchain-google-genai==1.0.8      # Gemini Models
langchain-google-vertexai==1.0.8   # Vertex AI Integration
google-cloud-discoveryengine==0.12.0  # Document Search
google-cloud-storage==2.18.0       # Cloud Storage
google-cloud-pubsub==2.15.0        # Pub/Sub messaging
```

## 📦 Estructura del Proyecto

```
aicon-assistant-api/
├── agent/                              # Módulo principal de conversación
│   ├── application/
│   │   └── service/
│   │       └── response_question.py    # Lógica de generación de respuestas
│   ├── domain/
│   │   ├── constants/
│   │   │   ├── domain_constants.py     # Constantes del dominio
│   │   │   └── prompts.py              # Templates de prompts
│   │   ├── entities/
│   │   │   ├── ChatDocumentoInfoRequest.py
│   │   │   └── GenerateSessionRequest.py
│   │   └── repository/
│   │       ├── ai_retriver.py          # Cliente RAG con Vertex AI Search
│   │       └── transformer_si.py       # Transformación de system instructions
│   ├── views/
│   │   ├── agent_conversation.py       # API de chat streaming
│   │   └── session.py                  # API de gestión de sesiones
│   ├── models.py                       # Models de BD (Session, Conversation)
│   └── urls.py                         # Rutas del módulo agent
│
├── commons/                            # Utilidades compartidas
│   └── domain/
│       ├── constants/
│       │   ├── env_variables.py        # Variables de entorno
│       │   ├── domain_constants.py     # Constantes globales
│       │   └── exceptions.py           # Excepciones personalizadas
│       └── repository/
│           ├── generative_model.py     # Wrapper de Gemini LLM
│           ├── data_store.py           # Operaciones de almacenamiento
│           └── gcloud_storage_client.py # Cliente GCS
│
├── documents/                          # Gestión de documentos
│   ├── application/
│   │   └── service.py                  # Servicios de documentos
│   └── domain/
│       └── models/
│           ├── document_info.py
│           └── data_store_info.py
│
├── backend_aicon_assistant/            # Configuración Django
│   ├── settings.py                     # Configuración principal
│   └── urls.py                         # URLs raíz
│
├── Dockerfile                          # Imagen Docker
├── requirements.txt                    # Dependencias Python
├── service.yaml                        # Config Knative Cloud Run
└── before-cloudbuild.yaml             # Pipeline CI/CD
```

## 🔄 Flujo de Datos

### 1. Generación de Sesión

```
Cliente → POST /aicon/chat/generate-session
         ↓
    SessionAPI.create()
         ↓
    Session.objects.create(email, uuid)
         ↓
    Response: { session_id: "uuid..." }
```

### 2. Chat con Streaming

```
Cliente → POST /aicon/chat/streaming-chat
         ↓
    AgentConversationAPI.generate_stream_response()
         ↓
    ┌─────────────────────────────────────┐
    │ 1. Recuperación RAG                │
    │    AiRetriver.get_few_examples()    │
    │    → Vertex AI Search               │
    │    → Documentos relevantes          │
    └─────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────┐
    │ 2. Construcción de Prompt          │
    │    TransformerSystemInstruction()    │
    │    → DEFAULT_PROMPT + few_examples  │
    └─────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────┐
    │ 3. Generación con LLM              │
    │    ResponseQuestion.generate()       │
    │    → Gemini 1.5 Pro                 │
    │    → Streaming response             │
    └─────────────────────────────────────┘
         ↓
    ┌─────────────────────────────────────┐
    │ 4. Persistencia                    │
    │    ConversationInfo.objects.create() │
    │    ConversationDetails.objects.create()│
    └─────────────────────────────────────┘
         ↓
    StreamingHttpResponse (SSE)
```

## 🎯 Componentes Principales

### AiRetriver
**Responsabilidad**: Búsqueda semántica en Vertex AI Search

```python
class AiRetriver:
    def __init__(self, max_documents: int)
    def invoke(query: str) -> List[Document]
    def get_few_examples(query: str) -> str
```

**Características**:
- Utiliza `VertexAISearchRetriever` de Langchain
- Busca documentos relevantes basados en similitud semántica
- Extrae ejemplos contextually relevant para few-shot learning
- Configurable `max_documents` para controlar contexto

### LlmGenerativeModel
**Responsabilidad**: Wrapper de Gemini LLM

```python
class LlmGenerativeModel:
    def __init__(system_instruction: str, type_model: str)
    def generate_content(query, config, safety_settings, stream)
    def get_text_from_iterator(iterator_response)
```

**Configuración**:
- Modelo: `gemini-1.5-pro-002` (robust) o `gemini-1.5-flash-002` (flash)
- Temperature: 1.0 (creatividad)
- Max tokens: 8192
- Safety settings: OFF (configurables)

### ResponseQuestion
**Responsabilidad**: Orquestación de generación de respuestas

```python
class ResponseQuestion:
    def generate_async_response_by_question(
        system_instruction: str,
        question: str
    ) -> Iterator[TextChunk]
```

**Características**:
- Integra retriever RAG con generación LLM
- Streaming en tiempo real
- Manejo de errores robusto

### Models de Base de Datos

#### Session
- Almacena sesiones por usuario (email)
- UUID único para tracking
- Timestamps de creación y actualización

#### ConversationInfo
- Agrupa conversaciones en una sesión
- Título de conversación
- Relación ForeignKey con Session

#### ConversationDetails
- Preguntas y respuestas individuales
- Contenido completo del LLM response
- Relación ForeignKey con ConversationInfo

## 🔐 Seguridad y Configuración

### Variables de Entorno Requeridas

```bash
PROJECT_ID=your-gcp-project-id
REGION=us-east4
DATA_STORE_ID=your-discovery-engine-datastore
DATA_STORE_LOCATION=global
GCLOUD_STORAGE_BUCKET=your-bucket-name
GCLOUD_STORAGE_FOLDER=your-folder-path
DOCUMENT_BUCKET=your-documents-bucket
TOPIC_DOCUMENT_PROCESSOR=your-pubsub-topic
```

### Autenticación

- **Desarrollo**: Sin autenticación (configurado para testing)
- **Producción**: Requiere Service Account de GCP
- **Headers**: Configurables via Django settings

### Rate Limiting

- Implementado via `AnonRateThrottle` de DRF
- Configurable por ruta

## 🚀 Deployment

### Cloud Run Configuration

```yaml
spec:
  containerConcurrency: 80
  timeoutSeconds: 30
  resources:
    limits:
      cpu: '1'
      memory: 1Gi
  containers:
    - image: us-east4-docker.pkg.dev/...
      env:
        - PROJECT_ID
        - REGION
        - DATA_STORE_ID
        # ... más variables
```

### Auto-Scaling

- Min Scale: 1 instancia
- Max Scale: 10 instancias
- Basado en concurrencia y latencia

## 📊 Consideraciones de Performance

- **Streaming**: Respuestas en tiempo real, no espera completitud
- **Retrieval**: Búsqueda optimizada con índices semánticos de Vertex AI
- **Caching**: Posible implementación futura de caché de documentos
- **Latency**: Típicamente 2-5 segundos para primera respuesta
- **Throughput**: 80 requests concurrentes por instancia

## 🔮 Mejoras Futuras

- [ ] Implementar caché Redis para documentos frecuentes
- [ ] Añadir métricas de observabilidad (Prometheus/Cloud Monitoring)
- [ ] Soporte multi-idioma
- [ ] Fine-tuning de prompts por institución
- [ ] Integración con más LLMs (configurable)
- [ ] WebSocket support para bidirectional streaming
- [ ] Rate limiting por usuario/sesión
- [ ] Implementar circuit breakers para resiliencia

## 📚 Referencias

- [Vertex AI Search Documentation](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Langchain Documentation](https://python.langchain.com/)
- [Google Cloud Run](https://cloud.google.com/run/docs)

