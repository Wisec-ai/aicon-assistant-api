# Documentación AICON Assistant API

Bienvenido a la documentación del **AICON Assistant API**, el microservicio de conversación inteligente basado en RAG para ImmobAI.

## 📚 Índice de Documentación

### 🏗️ [Arquitectura](ARQUITECTURA.md)

Descripción completa del diseño del sistema, incluyendo:
- Visión general de la arquitectura de microservicios
- Stack tecnológico y librerías utilizadas
- Estructura del proyecto y componentes principales
- Flujos de datos detallados
- Configuración de seguridad y performance
- Mejoras futuras planificadas

**Audiencia**: Desarrolladores, arquitectos, tech leads

---

### 🔧 [Configuración](CONFIGURACION.md)

Guía paso a paso para configurar y desplegar el servicio:
- Requisitos previos y software necesario
- Instalación local y desarrollo
- Configuración con Docker
- Deployment en Google Cloud Run
- Configuración de base de datos (PostgreSQL/Cloud SQL)
- Setup de Vertex AI Search (Discovery Engine)
- Variables de entorno y secretos
- Monitoreo y logging
- Troubleshooting común

**Audiencia**: DevOps, desarrolladores, system administrators

---

### 📡 [API](API.md)

Documentación completa de los endpoints REST:
- Visión general de la API
- Autenticación y headers
- Detalles de cada endpoint:
  - Generar sesión
  - Chat streaming
  - Gestión de documentos
- Modelos de datos
- Ejemplos de código (JavaScript, Python, cURL)
- Códigos de error HTTP
- Rate limiting
- Flujos de uso completos

**Audiencia**: Desarrolladores frontend, integrators, QA

---

## 🎯 Guía Rápida

### ¿Qué es AICON Assistant API?

Es un microservicio que proporciona capacidades de chat inteligente usando RAG (Retrieval Augmented Generation). Permite a los usuarios hacer preguntas en lenguaje natural y recibir respuestas contextualizadas basadas en documentación específica de inmobiliarias.

### ¿Cuál documento debo leer?

- **Solo integrar la API**: → [API.md](API.md)
- **Desplegar en producción**: → [Configuración.md](CONFIGURACION.md)
- **Entender cómo funciona**: → [Arquitectura.md](ARQUITECTURA.md)
- **Setup completo desde cero**: → Lee todos los documentos en orden

---

## 🚀 Inicio Rápido

Para empezar rápido:

1. Clona el repositorio
2. Configura variables de entorno (ver [Configuración](CONFIGURACION.md))
3. Instala dependencias: `pip install -r requirements.txt`
4. Ejecuta migraciones: `python manage.py migrate`
5. Inicia servidor: `python manage.py runserver`

Luego consulta [API.md](API.md) para ver cómo usar los endpoints.

---

## 📞 Soporte

Para preguntas o problemas:
- **Email**: cgluni16@gmail.com, jgonzalesinca15@gmail.com
- **Equipo**: AICON

---

**Nota**: Esta documentación es específica para el microservicio AICON Assistant API. Para información sobre la plataforma ImmobAI completa, consultar la documentación del proyecto principal.

