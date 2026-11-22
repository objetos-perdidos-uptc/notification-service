# Seeker UPTC - Matching & Notification Microservices

Este repositorio contiene la implementación de los microservicios de **Matching** y **Notificaciones** para la plataforma de Objetos Perdidos de la UPTC, desarrollados bajo **Arquitectura Hexagonal**, **DDD** y **EDA**.

## 🏗️ Arquitectura

- **Dominio:** Lógica pura (Patrón Strategy para el cálculo de similitud).
- **Aplicación:** Casos de uso (inyección de dependencias).
- **Infraestructura:** Redis (Rankings), RabbitMQ (Eventos) y Brevo (Emails).

## 🚀 Cómo ejecutar el proyecto (Local)

### Prerrequisitos

- Python 3.12+
- Docker y Docker Compose
- Una cuenta en Brevo (para el envío de correos).

### 1. Variables de Entorno

En el microservicio `notification-service`, crea un archivo `.env`:

```env
BREVO_API_KEY=tu_api_key_aqui
EMAIL_USER=tu_correo_verificado@gmail.com
```
