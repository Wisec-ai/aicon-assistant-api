# Documentación de API

## 📚 Visión General

El AICON Assistant API expone endpoints REST para:
- **Gestión de Sesiones**: Crear y administrar sesiones de conversación
- **Chat Streaming**: Interactuar con el agente conversacional usando RAG
- **Gestión de Documentos**: Subir e indexar documentos para el RAG

**Base URL**: `https://your-domain.run.app/aicon`

## 🔑 Autenticación

Actualmente, el servicio está configurado sin autenticación para desarrollo/testing. En producción, se recomienda implementar autenticación JWT o API Key.

### Headers Comunes

```http
Content-Type: application/json
Accept: application/json, text/event-stream
```

## 📡 Endpoints

---

## 1. Chat - Generar Sesión

Crea una nueva sesión de conversación para un usuario.

### Endpoint

```
POST /aicon/chat/generate-session
```

### Request Body

```json
{
  "email": "user@example.com"
}
```

### Response (200 OK)

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Ejemplo cURL

```bash
curl -X POST https://your-domain/aicon/chat/generate-session \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com"
  }'
```

### Respuesta de Error

```json
{
  "error": "Error uploading file to cloud storage",
  "details": "Error message details..."
}
```

---

## 2. Chat - Streaming Conversation

Inicia una conversación con el agente usando RAG. Las respuestas se entregan vía Server-Sent Events (SSE).

### Endpoint

```
POST /aicon/chat/streaming-chat
```

### Request Body

```json
{
  "question": "¿Cuáles son las características del departamento modelo Estudio?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "max_documents": 3,
  "conversation_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `question` | string | ✅ | Pregunta del usuario |
| `session_id` | string | ✅ | UUID de la sesión (del endpoint generate-session) |
| `max_documents` | integer | ❌ | Máximo de documentos a recuperar (default: 3) |
| `conversation_id` | string | ❌ | UUID de la conversación (generado automáticamente si no se proporciona) |

### Response (Streaming - SSE)

La respuesta es un stream de Server-Sent Events:

```http
Content-Type: text/event-stream
Cache-Control: no-cache
```

**Formato de cada evento:**

```json
{"raw_response": "fragmento de texto..."}
```

**Último evento:**

```json
{"conversation_id": "660e8400-e29b-41d4-a716-446655440000"}
```

### Ejemplo cURL

```bash
curl -X POST https://your-domain/aicon/chat/streaming-chat \
  -H "Content-Type: application/json" \
  -N \
  -d '{
    "question": "¿Cuáles son las características del departamento modelo Estudio?",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "max_documents": 3
  }'
```

### Ejemplo JavaScript (Fetch API)

```javascript
async function streamChat(question, sessionId) {
  const response = await fetch('https://your-domain/aicon/chat/streaming-chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
      session_id: sessionId,
      max_documents: 3
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split('\n');

    for (const line of lines) {
      if (line.trim()) {
        try {
          const data = JSON.parse(line);
          if (data.raw_response) {
            // Renderizar fragmento de respuesta
            console.log(data.raw_response);
          }
          if (data.conversation_id) {
            console.log('Conversation ID:', data.conversation_id);
          }
          if (data.error) {
            console.error('Error:', data.error);
          }
        } catch (e) {
          console.error('Parse error:', e);
        }
      }
    }
  }
}
```

### Respuesta de Error

```json
{"error": "Error message details...\n"}
```

---

## 3. Documentos - Generar URL de Carga

Genera una URL firmada (presigned URL) para subir un documento a Cloud Storage.

### Endpoint

```
POST /aicon/documents/upload
```

### Request Body

```json
{
  "company_id": "company-123",
  "file_name": "brochure-proyecto-xyz.pdf"
}
```

### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `company_id` | string | ✅ | Identificador de la inmobiliaria |
| `file_name` | string | ✅ | Nombre del archivo a subir |

### Response (200 OK)

```json
{
  "status": "successful",
  "url": "https://storage.googleapis.com/bucket/company-123/raw/brochure-proyecto-xyz.pdf?X-Goog-Signature=...",
  "details": ""
}
```

### Ejemplo cURL

```bash
# 1. Generar URL
curl -X POST https://your-domain/aicon/documents/upload \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "company-123",
    "file_name": "brochure.pdf"
  }'

# 2. Subir archivo usando la URL presignada
curl -X PUT "URL_PRESIGNADA_AQUI" \
  -H "Content-Type: application/pdf" \
  --data-binary @./brochure.pdf
```

### Respuesta de Error

```json
{
  "error": "Error uploading file to cloud storage",
  "url": "",
  "details": "Error message details..."
}
```

---

## 4. Documentos - Indexar en Data Store

Importa documentos desde Cloud Storage al Vertex AI Search Data Store para que estén disponibles en el RAG.

### Endpoint

```
POST /aicon/documents/upload-data-store
```

### Request Body

```json
{
  "company_id": "company-123"
}
```

### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `company_id` | string | ✅ | Identificador de la inmobiliaria |

### Response (200 OK)

```json
{
  "status": "successful"
}
```

### Ejemplo cURL

```bash
curl -X POST https://your-domain/aicon/documents/upload-data-store \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "company-123"
  }'
```

### Respuesta de Error

```json
{
  "error": "Error uploading file to cloud storage",
  "url": "",
  "details": "Error message details..."
}
```

---

## 🔄 Flujo Completo de Uso

### 1. Crear Sesión de Chat

```bash
SESSION_RESPONSE=$(curl -s -X POST https://your-domain/aicon/chat/generate-session \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}')

SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')
```

### 2. Hacer Pregunta con Streaming

```bash
curl -X POST https://your-domain/aicon/chat/streaming-chat \
  -H "Content-Type: application/json" \
  -N \
  -d "{
    \"question\": \"¿Qué propiedades hay disponibles en Lima?\",
    \"session_id\": \"$SESSION_ID\",
    \"max_documents\": 5
  }"
```

### 3. Subir Documento

```bash
# Generar URL
UPLOAD_RESPONSE=$(curl -s -X POST https://your-domain/aicon/documents/upload \
  -H "Content-Type: application/json" \
  -d '{"company_id": "company-123", "file_name": "brochure.pdf"}')

UPLOAD_URL=$(echo $UPLOAD_RESPONSE | jq -r '.url')

# Subir archivo
curl -X PUT "$UPLOAD_URL" \
  -H "Content-Type: application/pdf" \
  --data-binary @brochure.pdf

# Indexar en Data Store
curl -X POST https://your-domain/aicon/documents/upload-data-store \
  -H "Content-Type: application/json" \
  -d '{"company_id": "company-123"}'
```

---

## 📊 Modelos de Datos

### Session

```python
{
  "id": 1,
  "email": "user@example.com",
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00Z",
  "update_at": "2024-01-15T10:30:00Z"
}
```

### ConversationInfo

```python
{
  "id": 1,
  "uuid": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Sin titulo creado",
  "session_id": 1,
  "created_at": "2024-01-15T10:31:00Z"
}
```

### ConversationDetails

```python
{
  "id": 1,
  "question": "¿Cuáles son las características del departamento modelo Estudio?",
  "llm_response": "Según la documentación...",
  "conversation_info_id": 1,
  "created_at": "2024-01-15T10:31:05Z"
}
```

---

## ⚠️ Rate Limiting

El servicio implementa rate limiting usando `AnonRateThrottle` de Django REST Framework. Los límites actuales son:

- **Por defecto**: Configuración estándar de DRF
- **Recomendado para producción**: Configurar límites por usuario/sesión

Para verificar límites:
```bash
curl -I https://your-domain/aicon/chat/generate-session
```

Headers relevantes:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1640000000
```

---

## 🐛 Códigos de Error HTTP

| Código | Significado | Descripción |
|--------|-------------|-------------|
| 200 | OK | Solicitud exitosa |
| 400 | Bad Request | Datos de entrada inválidos |
| 404 | Not Found | Recurso no encontrado (ej: sesión inexistente) |
| 429 | Too Many Requests | Rate limit excedido |
| 500 | Internal Server Error | Error en el servidor |
| 503 | Service Unavailable | Servicio no disponible temporalmente |

---

## 🔍 Ejemplos de Integración

### React/Next.js

```typescript
// hooks/useChat.ts
import { useState } from 'react';

export function useChat() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const createSession = async (email: string) => {
    const response = await fetch('/aicon/chat/generate-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    });
    const data = await response.json();
    setSessionId(data.session_id);
    return data.session_id;
  };

  const sendMessage = async (question: string) => {
    if (!sessionId) throw new Error('No session created');
    setIsLoading(true);

    const response = await fetch('/aicon/chat/streaming-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        session_id: sessionId,
        max_documents: 3,
      }),
    });

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let fullResponse = '';

    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.trim()) {
          try {
            const data = JSON.parse(line);
            if (data.raw_response) {
              fullResponse += data.raw_response;
              setMessages((prev) => [
                ...prev.slice(0, -1),
                { role: 'assistant', content: fullResponse },
              ]);
            }
          } catch (e) {
            console.error('Parse error:', e);
          }
        }
      }
    }

    setIsLoading(false);
  };

  return { createSession, sendMessage, messages, isLoading };
}
```

### Python

```python
import requests
import json

class AICONChatClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session_id = None

    def create_session(self, email: str) -> str:
        response = requests.post(
            f"{self.base_url}/aicon/chat/generate-session",
            json={"email": email}
        )
        data = response.json()
        self.session_id = data["session_id"]
        return self.session_id

    def chat_stream(self, question: str, max_documents: int = 3):
        if not self.session_id:
            raise ValueError("Session not created")

        response = requests.post(
            f"{self.base_url}/aicon/chat/streaming-chat",
            json={
                "question": question,
                "session_id": self.session_id,
                "max_documents": max_documents
            },
            stream=True
        )

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    if 'raw_response' in data:
                        yield data['raw_response']
                    elif 'error' in data:
                        raise Exception(data['error'])
                except json.JSONDecodeError:
                    pass

# Uso
client = AICONChatClient("https://your-domain")
session_id = client.create_session("user@example.com")

for chunk in client.chat_stream("¿Qué propiedades hay disponibles?"):
    print(chunk, end='', flush=True)
```

---

## 📝 Notas Importantes

1. **Streaming**: El endpoint de chat usa Server-Sent Events para streaming. No cierre la conexión prematuramente.
2. **Session ID**: Mantenga el session_id para mantener contexto entre conversaciones.
3. **Documentos**: Los documentos deben ser indexados en el Data Store antes de estar disponibles para búsqueda RAG.
4. **Formato de archivos**: Formatos soportados: PDF, DOCX, TXT, MD, HTML.
5. **Límites**: Máximo de 3-10 documentos recuperados por defecto (configurable).
6. **Timeout**: Timeout de Cloud Run configurado a 30 segundos para requests.

---

## 🔗 Referencias

- [Server-Sent Events (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vertex AI Search API](https://cloud.google.com/generative-ai-app-builder/docs)

