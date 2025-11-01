# AICON Assistant API

**Microservicio de agente conversacional inteligente basado en RAG para ImmobAI**

## 📋 Descripción

El **AICON Assistant API** es un servicio core de conversación que forma parte de la arquitectura de microservicios de **ImmobAI** (plataforma inmobiliaria inteligente). Este servicio implementa un sistema de chat avanzado utilizando **RAG** (Retrieval Augmented Generation) para responder preguntas de usuarios basándose en documentación específica de inmobiliarias.

### Contexto en ImmobAI

Este servicio se integra con la funcionalidad **"Chatea con tu data"** de la plataforma ImmobAI, permitiendo a inmobiliarias:

- 📄 Consultar documentación interna mediante chat inteligente
- 🔍 Obtener respuestas precisas basadas en brochures, características de proyectos y documentación técnica
- 💬 Mantener historial de conversaciones contextuales
- 🎯 Personalizar respuestas según el catálogo de cada inmobiliaria

### Flujo de Operación

```
Usuario → Pregunta → AICON Assistant API
                         ↓
         [1] Búsqueda RAG (Vertex AI Search)
                         ↓
         [2] Generación con Gemini 1.5 Pro
                         ↓
         [3] Streaming de respuesta
                         ↓
              Usuario recibe respuesta
```

## ✨ Características Principales

### 🧠 Inteligencia Artificial

- **RAG Algorithm**: Búsqueda semántica en documentos almacenados
- **LLM**: Google Gemini 1.5 Pro-002 para generación de respuestas
- **Streaming**: Respuestas en tiempo real vía Server-Sent Events
- **Contextual**: Utiliza historial de conversación y documentos relevantes

### 📚 Gestión de Documentos

- Subida de documentos vía presigned URLs
- Indexación automática en Vertex AI Search (Discovery Engine)
- Búsqueda semántica en brochures, PDFs, y documentación técnica
- Soporte multi-formato: PDF, DOCX, TXT, MD, HTML

### 🔄 Gestión de Sesiones

- Sesiones persistentes por usuario
- Historial completo de conversaciones
- Tracking de preguntas y respuestas
- Identificación por email

### ⚡ Performance

- Streaming en tiempo real
- Búsqueda optimizada con índices semánticos
- Deployed en Google Cloud Run
- Auto-scaling (1-10 instancias)
- Concurrencia de hasta 80 requests por instancia

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.10+
- Google Cloud Project con Vertex AI habilitado
- Vertex AI Search (Discovery Engine) Data Store configurado
- Service Account con permisos necesarios

### Instalación Local

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd aicon-assistant-api

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 5. Ejecutar migraciones
python manage.py migrate

# 6. Iniciar servidor
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

### Docker

```bash
# Build
docker build -t aicon-assistant-api:latest .

# Run
docker run -d \
  -p 8080:8080 \
  -e PROJECT_ID=your-project-id \
  -e REGION=us-east4 \
  -e DATA_STORE_ID=your-datastore-id \
  aicon-assistant-api:latest
```

## 📚 Documentación

Documentación completa disponible en la carpeta `/docs`:

📖 **[Índice de Documentación](docs/README.md)** - Guía de navegación

- **[Arquitectura](docs/ARQUITECTURA.md)** - Diseño del sistema, componentes y flujos de datos
- **[Configuración](docs/CONFIGURACION.md)** - Setup, deployment y configuración avanzada
- **[API](docs/API.md)** - Documentación completa de endpoints REST

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Django 5.1.6 + Django REST Framework
- **Lenguaje**: Python 3.10
- **ORM**: Django ORM
- **Base de Datos**: SQLite (dev) / PostgreSQL (prod)

### IA & Machine Learning
- **LLM**: Google Gemini 1.5 Pro-002
- **RAG**: Langchain + Vertex AI Search
- **Search**: Google Discovery Engine
- **Streaming**: Vertex AI Generative Models

### Cloud & DevOps
- **Plataforma**: Google Cloud Platform
- **Compute**: Cloud Run (Knative)
- **CI/CD**: Cloud Build
- **Storage**: Cloud Storage
- **Container**: Docker

### Principales Librerías
```
langchain-google-community==1.0.7   # Vertex AI Search
langchain-google-genai==1.0.8       # Gemini Models
langchain-google-vertexai==1.0.8    # Vertex AI Integration
google-cloud-discoveryengine==0.12.0 # Document Search
google-cloud-storage==2.18.0        # Cloud Storage
djangorestframework==3.15.2         # REST API
```

## 📁 Estructura del Proyecto

```
aicon-assistant-api/
├── agent/                          # Módulo principal de conversación
│   ├── application/service/        # Servicios de negocio
│   ├── domain/
│   │   ├── constants/              # Prompts y constantes
│   │   ├── entities/               # DTOs y entidades
│   │   └── repository/             # Clientes RAG y AI
│   ├── views/                      # API endpoints
│   └── models.py                   # Models de BD
├── commons/                        # Utilidades compartidas
│   └── domain/
│       ├── constants/              # Variables de entorno
│       ├── repository/             # Clientes Cloud
│       └── utils/                  # Utilidades generales
├── documents/                      # Gestión de documentos
│   ├── application/
│   ├── domain/models/
│   └── views.py
├── backend_aicon_assistant/        # Config Django
│   ├── settings.py
│   └── urls.py
├── docs/                           # Documentación
│   ├── ARQUITECTURA.md
│   ├── CONFIGURACION.md
│   └── API.md
├── Dockerfile                      # Imagen Docker
├── requirements.txt                # Dependencias
└── service.yaml                    # Config Cloud Run
```

## 🎯 Uso Básico de la API

### 1. Crear Sesión

```bash
curl -X POST https://your-domain/aicon/chat/generate-session \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
```

Respuesta:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Hacer Pregunta (Streaming)

```bash
curl -X POST https://your-domain/aicon/chat/streaming-chat \
  -H "Content-Type: application/json" \
  -N \
  -d '{
    "question": "¿Cuáles son las características del modelo Estudio?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

Respuesta (streaming):
```json
{"raw_response": "Según la documentación disponible..."}
{"raw_response": "el modelo Estudio cuenta con..."}
...
{"conversation_id": "660e8400-e29b-41d4-a716-446655440000"}
```

Ver [documentación completa de API](docs/API.md) para más ejemplos.

## 🔐 Configuración

### Variables de Entorno Requeridas

```bash
PROJECT_ID=your-gcp-project
REGION=us-east4
DATA_STORE_ID=your-datastore-id
DATA_STORE_LOCATION=global
GCLOUD_STORAGE_BUCKET=your-bucket
GCLOUD_STORAGE_FOLDER=/documents
DOCUMENT_BUCKET=your-docs-bucket
```

Ver [guía de configuración](docs/CONFIGURACION.md) para setup detallado.

## 🚢 Deployment

### Google Cloud Run

El servicio está configurado para deploy automático en Cloud Run:

```bash
# Trigger Cloud Build
gcloud builds submit --config=cloudbuild.yaml

# O push a rama main para CI/CD automático
git push origin main
```

**Especificaciones de producción**:
- CPU: 1 vCPU
- Memoria: 1GB
- Max instancias: 10
- Timeout: 30s
- Concurrencia: 80 requests/instancia

Ver [configuración de deployment](docs/CONFIGURACION.md) para más detalles.

## 🧪 Testing

```bash
# Tests unitarios
python manage.py test

# Tests con cobertura
coverage run --source='.' manage.py test
coverage report
```

## 📊 Monitoring

El servicio envía logs automáticamente a Cloud Logging:

```bash
# Ver logs en tiempo real
gcloud logging tail "resource.type=cloud_run_revision"
```

## 🔄 Arquitectura de Microservicios

Este servicio es parte del ecosistema ImmobAI:

```
Frontend Angular
    ↓
Backend Principal ←→ AICON Assistant API ←→ Vertex AI Search
    ↓                        ↓
WhatsApp Assistant      Cloud Storage
```

Ver [documentación de arquitectura](docs/ARQUITECTURA.md) para detalles completos.

## 👥 Equipo

**AICON** - Startup de Inteligencia Artificial

- **Cristian Gomez** - cgluni16@gmail.com
- **Johann Gonzales** - jgonzalesinca15@gmail.com

## 📞 Contacto

**Equipo**: AICON  
**Email**: cgluni16@gmail.com, jgonzalesinca15@gmail.com

## 🙏 Agradecimientos

- Google Cloud Platform
- Langchain Team
- Django Community
- Vertex AI Team

## 📝 Licencia

Proprietary - Todos los derechos reservados

---

**Nota**: Este es un microservicio core para ImmobAI. Para más información sobre la plataforma completa, consultar los repositorios relacionados.

