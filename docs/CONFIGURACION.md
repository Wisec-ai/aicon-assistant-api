# Configuración del Sistema

## 📋 Requisitos Previos

### Software Requerido

- **Python**: 3.10.16 o superior
- **Docker**: 20.10+ (para containerización)
- **Google Cloud SDK**: Última versión
- **Git**: Para clonar el repositorio

### Cuentas y Recursos Cloud

- **Google Cloud Project** con facturación habilitada
- **Vertex AI Search** (Discovery Engine) Data Store configurado
- **Cloud Storage Bucket** para almacenar documentos
- **Service Account** con permisos necesarios

## 🔧 Instalación Local

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd aicon-assistant-api
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# Google Cloud Configuration
PROJECT_ID=your-project-id
REGION=us-east4

# Vertex AI Search (Discovery Engine)
DATA_STORE_ID=your-datastore-id
DATA_STORE_LOCATION=global

# Cloud Storage
GCLOUD_STORAGE_BUCKET=your-storage-bucket
GCLOUD_STORAGE_FOLDER=/documents

# Document Processing
DOCUMENT_BUCKET=your-documents-bucket
TOPIC_DOCUMENT_PROCESSOR=projects/your-project/topics/document-processor

# Database (opcional para producción)
DB_ENGINE=django.db.backends.postgresql
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Configurar Autenticación GCP

```bash
# Opción 1: Application Default Credentials
gcloud auth application-default login

# Opción 2: Service Account (producción)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

### 6. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Iniciar Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 🐳 Configuración con Docker

### Build de Imagen

```bash
docker build -t aicon-assistant-api:latest .
```

### Ejecutar Contenedor

```bash
docker run -d \
  --name aicon-assistant \
  -p 8080:8080 \
  -e PROJECT_ID=your-project-id \
  -e REGION=us-east4 \
  -e DATA_STORE_ID=your-datastore-id \
  -e DATA_STORE_LOCATION=global \
  -e GCLOUD_STORAGE_BUCKET=your-bucket \
  -e GCLOUD_STORAGE_FOLDER=/documents \
  -v /path/to/service-account.json:/app/service-account.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json \
  aicon-assistant-api:latest
```

### Usando Docker Compose (recomendado)

Crear `docker-compose.yml`:

```yaml
version: '3.8'

services:
  aicon-assistant-api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - PROJECT_ID=${PROJECT_ID}
      - REGION=${REGION}
      - DATA_STORE_ID=${DATA_STORE_ID}
      - DATA_STORE_LOCATION=${DATA_STORE_LOCATION}
      - GCLOUD_STORAGE_BUCKET=${GCLOUD_STORAGE_BUCKET}
      - GCLOUD_STORAGE_FOLDER=${GCLOUD_STORAGE_FOLDER}
    volumes:
      - ./service-account.json:/app/service-account.json:ro
      - ./media:/app/media
    env_file:
      - .env
```

Ejecutar:
```bash
docker-compose up -d
```

## ☁️ Configuración para Producción

### Cloud Run Deployment

#### 1. Configurar Service Account

```bash
# Crear service account
gcloud iam service-accounts create aicon-assistant-sa \
  --display-name="AICON Assistant Service Account"

# Asignar permisos necesarios
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:aicon-assistant-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/discoveryengine.editor"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:aicon-assistant-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# Crear y descargar key
gcloud iam service-accounts keys create service-account.json \
  --iam-account=aicon-assistant-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

#### 2. Configurar Artifact Registry

```bash
# Crear repositorio Docker
gcloud artifacts repositories create aicon-api-agents \
  --repository-format=docker \
  --location=us-east4 \
  --description="AICON Assistant API Docker repository"
```

#### 3. Configurar Cloud Build

Crear `cloudbuild.yaml`:

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    entrypoint: bash
    args:
      - '-c'
      - |
        docker build -t us-east4-docker.pkg.dev/$PROJECT_ID/${_REPOSITORY}/${_CLOUD_RUN_NAME}:latest .
        && docker push us-east4-docker.pkg.dev/$PROJECT_ID/${_REPOSITORY}/${_CLOUD_RUN_NAME}:latest
    secretEnv: []

  - name: 'us-east4-docker.pkg.dev/$PROJECT_ID/envsubst/envsubst:latest'
    entrypoint: 'sh'
    args:
      - '-c'
      - |
        envsubst < ./service.yaml | sponge ./service.yaml
        cat ./service.yaml
  
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud run services replace ./service.yaml

options:
  env:
    - 'CLOUD_RUN_NAME=$_CLOUD_RUN_NAME'
    - 'REGION=$_REGION'
    - 'PROJECT_ID=$PROJECT_ID'
    - 'BUILD_ID=$BUILD_ID'
    - 'STAGE=$_STAGE'
    - 'REPOSITORY=$_REPOSITORY'

substitutions:
  _CLOUD_RUN_NAME: aicon-api-crm-v1
  _REGION: us-east4
  _REPOSITORY: aicon-api-agents
```

#### 4. Desplegar

```bash
# Trigger Cloud Build
gcloud builds submit --config=cloudbuild.yaml

# O hacer push a rama que tiene trigger automático
git push origin main
```

### Variables de Entorno en Cloud Run

Configurar en `service.yaml`:

```yaml
env:
  - name: PROJECT_ID
    value: '${PROJECT_ID}'
  - name: REGION
    value: '${REGION}'
  - name: DATA_STORE_ID
    value: '${DATA_STORE_ID}'
  - name: DATA_STORE_LOCATION
    value: '${DATA_STORE_LOCATION}'
  - name: GCLOUD_STORAGE_BUCKET
    value: '${GCLOUD_STORAGE_BUCKET}'
  - name: GCLOUD_STORAGE_FOLDER
    value: '${GCLOUD_STORAGE_FOLDER}'
  - name: DOCUMENT_BUCKET
    value: '${DOCUMENT_BUCKET}'
  - name: GOOGLE_APPLICATION_CREDENTIALS
    value: '${GOOGLE_APPLICATION_CREDENTIALS}'
```

## 🗄️ Configuración de Base de Datos

### SQLite (Desarrollo)

Por defecto, Django usa SQLite. No requiere configuración adicional.

### PostgreSQL (Producción)

#### 1. Crear Instancia Cloud SQL

```bash
gcloud sql instances create aicon-postgres \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-east4
```

#### 2. Crear Base de Datos

```bash
gcloud sql databases create aicon_db --instance=aicon-postgres
```

#### 3. Crear Usuario

```bash
gcloud sql users create aicon_user \
  --instance=aicon-postgres \
  --password=YOUR_SECURE_PASSWORD
```

#### 4. Configurar Django Settings

En `backend_aicon_assistant/settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "aicon_db",
        "USER": "aicon_user",
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": "/cloudsql/PROJECT_ID:us-east4:aicon-postgres",
        "PORT": "5432",
    }
}
```

#### 5. Ejecutar Migraciones

```bash
python manage.py migrate
```

## 🔍 Configurar Vertex AI Search (Discovery Engine)

### 1. Habilitar APIs Necesarias

```bash
gcloud services enable \
  discoveryengine.googleapis.com \
  storage.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com
```

### 2. Crear Data Store

```bash
# Via Console o API
# URL: https://console.cloud.google.com/gen-app-builder/data-stores
```

O via API:

```bash
curl -X POST \
  "https://discoveryengine.googleapis.com/v1alpha/projects/PROJECT_ID/locations/global/collections/default_collection/dataStores?dataStoreId=DATASTORE_ID" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "AICON Documents",
    "solution_types": ["SOLUTION_TYPE_SEARCH"]
  }'
```

### 3. Configurar Importación de Documentos

```bash
# Importar documentos desde Cloud Storage
gcloud discovery-engine import \
  --data-store=DATASTORE_ID \
  --location=global \
  --project=PROJECT_ID \
  --gcs-source=gs://YOUR_BUCKET/documents
```

## 📊 Monitoreo y Logging

### Cloud Monitoring

El servicio automáticamente envía logs a Cloud Logging. Para ver logs:

```bash
# Logs en tiempo real
gcloud logging tail "resource.type=cloud_run_revision"

# Logs específicos
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=aicon-api-crm-v1" --limit 50
```

### Métricas Personalizadas

Configurar en Cloud Monitoring para:
- Latencia de respuesta
- Tasa de errores
- Throughput
- Uso de recursos

## 🔒 Seguridad

### CORS Configuration

En `backend_aicon_assistant/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "http://localhost:4200",  # Desarrollo
]
```

### Rate Limiting

Configurar en cada vista según necesidades:

```python
from rest_framework.throttling import AnonRateThrottle

class MyAPIView(APIView):
    throttle_classes = [AnonRateThrottle]
```

### Headers de Seguridad

Configurar en Cloud Run:
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test agent.tests

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

### Testing de Integración

```bash
# Requiere servicios en ejecución
pytest tests/integration/
```

## 🚨 Troubleshooting

### Error: "Project not found"

```bash
# Verificar proyecto activo
gcloud config get-value project

# Cambiar proyecto
gcloud config set project YOUR_PROJECT_ID
```

### Error: "Permission denied"

```bash
# Verificar permisos del service account
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

### Error: "DataStore not found"

```bash
# Listar datastores existentes
gcloud discovery-engine data-stores list \
  --location=global \
  --project=YOUR_PROJECT_ID
```

### Error: "Connection refused" en Cloud Run

Verificar:
1. Puertos correctos (8080)
2. Variables de entorno configuradas
3. Service account con permisos
4. VPC Connector si es necesario

## 📝 Checklist de Deployment

- [ ] Variables de entorno configuradas
- [ ] Service Account creado y con permisos
- [ ] Vertex AI Search Data Store configurado
- [ ] Cloud Storage bucket accesible
- [ ] Base de datos migrada
- [ ] Dockerfile probado localmente
- [ ] Cloud Build configurado
- [ ] Cloud Run service creado
- [ ] Domain mapping configurado (opcional)
- [ ] Monitoring y alertas configuradas
- [ ] Backup de base de datos configurado

## 🔗 Referencias

- [Vertex AI Search Setup](https://cloud.google.com/generative-ai-app-builder/docs/create-engine-search)
- [Cloud Run Deployment](https://cloud.google.com/run/docs/deploying)
- [Django Deployment Best Practices](https://docs.djangoproject.com/en/5.1/howto/deployment/)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)

