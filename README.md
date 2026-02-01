# 🗺️ Nominatim Geocoding API - Documentación Completa

> **API REST para convertir direcciones a coordenadas y viceversa**  
> Basada en Nominatim y OpenStreetMap - ¡100% Gratuita! 🎉

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Endpoints de la API Externa](#-endpoints-de-la-api-externa)
- [Manejo de Errores](#-manejo-de-errores)
- [Endpoints Locales](#-endpoints-locales)
- [Configuración](#-configuración)
- [Instalación y Ejecución](#-instalación-y-ejecución)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Política de Uso](#-política-de-uso)

---

## 🎯 Descripción General

### ¿Qué hace la API? 🤔

Esta aplicación consume la **API de Nominatim** para realizar **geocoding** (conversión de direcciones a coordenadas) y **reverse geocoding** (conversión de coordenadas a direcciones) en tiempo real. La aplicación actúa como un intermediario que simplifica el acceso a los servicios de geocoding de Nominatim, que está basado en datos de **OpenStreetMap**.

### ¿Qué información devuelve? 📦

- 🔍 **Búsqueda de direcciones**: Lista de ubicaciones que coinciden con una dirección o nombre de lugar, incluyendo coordenadas (latitud, longitud)
- 🔄 **Reverse geocoding**: Dirección completa correspondiente a unas coordenadas específicas
- 📊 **Información detallada**: Datos completos de ubicaciones (dirección estructurada, tipo de lugar, importancia, etc.)

### ¿Para qué sirve? 💡

- ✅ Convertir direcciones a coordenadas geográficas (latitud, longitud)
- ✅ Convertir coordenadas a direcciones legibles
- ✅ Integrar funcionalidad de geocoding en aplicaciones web o móviles
- ✅ Buscar lugares por nombre o dirección
- ✅ Obtener información detallada de ubicaciones geográficas

---

## 🌐 Endpoints de la API Externa

La aplicación utiliza varios endpoints de la API de Nominatim:

---

### 1️⃣ Search API (Búsqueda de Direcciones - Geocoding) 🔍

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `https://nominatim.openstreetmap.org/search` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [Nominatim Search API](https://nominatim.org/release-docs/latest/api/Search/) |

#### 📝 Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `q` | string | ✅ Sí | Dirección o nombre de lugar a buscar |
| `format` | string | ❌ No | Formato de respuesta (json, xml, geojson) - por defecto json |
| `limit` | int | ❌ No | Número máximo de resultados (máximo 50, por defecto 10) |
| `addressdetails` | int | ❌ No | Incluir detalles de dirección (0 o 1, por defecto 1) |
| `extratags` | int | ❌ No | Incluir tags adicionales (0 o 1, por defecto 1) |
| `namedetails` | int | ❌ No | Incluir nombres alternativos (0 o 1, por defecto 1) |

> ⚠️ **Nota importante:** Nominatim requiere un header `User-Agent` para identificar la aplicación. Sin este header, las peticiones pueden ser rechazadas.

#### 📤 Ejemplo de Petición

```http
GET /api/nominatim/search?q=1600+Amphitheatre+Parkway,+Mountain+View&limit=5
```

#### ✅ Ejemplo de Respuesta Exitosa (JSON)

```json
[
  {
    "place_id": 123456,
    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
    "osm_type": "way",
    "osm_id": 123456,
    "boundingbox": ["37.4224764", "37.4224764", "-122.0842499", "-122.0842499"],
    "lat": "37.4224764",
    "lon": "-122.0842499",
    "display_name": "1600 Amphitheatre Parkway, Mountain View, CA 94043, United States",
    "class": "place",
    "type": "house",
    "importance": 0.5,
    "address": {
      "house_number": "1600",
      "road": "Amphitheatre Parkway",
      "city": "Mountain View",
      "state": "California",
      "postcode": "94043",
      "country": "United States",
      "country_code": "us"
    }
  }
]
```

#### 📋 Descripción de Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `place_id` | int | ID único del lugar en Nominatim |
| `lat` | string | Latitud del lugar |
| `lon` | string | Longitud del lugar |
| `display_name` | string | Nombre completo del lugar para mostrar |
| `class` | string | Clase del lugar (place, amenity, etc.) |
| `type` | string | Tipo específico del lugar (house, building, etc.) |
| `importance` | float | Importancia del lugar (0-1) |
| `address` | object | Detalles estructurados de la dirección |
| `address.house_number` | string | Número de casa |
| `address.road` | string | Nombre de la calle |
| `address.city` | string | Ciudad |
| `address.country` | string | País |

---

### 2️⃣ Reverse API (Coordenadas a Dirección - Reverse Geocoding) 🔄

| Campo | Descripción |
|-------|-------------|
| **URL del endpoint** | `https://nominatim.openstreetmap.org/reverse` |
| **Método HTTP** | `GET` |
| **Documentación oficial** | [Nominatim Reverse API](https://nominatim.org/release-docs/latest/api/Reverse/) |

#### 📝 Parámetros Requeridos

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `lat` | float | ✅ Sí | Latitud (-90 a 90) |
| `lon` | float | ✅ Sí | Longitud (-180 a 180) |
| `format` | string | ❌ No | Formato de respuesta (json, xml, geojson) - por defecto json |
| `addressdetails` | int | ❌ No | Incluir detalles de dirección (0 o 1, por defecto 1) |
| `extratags` | int | ❌ No | Incluir tags adicionales (0 o 1, por defecto 1) |
| `namedetails` | int | ❌ No | Incluir nombres alternativos (0 o 1, por defecto 1) |

#### 📤 Ejemplo de Petición

```http
GET /api/nominatim/reverse?lat=37.4224764&lon=-122.0842499
```

#### ✅ Ejemplo de Respuesta Exitosa (JSON)

```json
{
  "place_id": 123456,
  "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
  "osm_type": "way",
  "osm_id": 123456,
  "lat": "37.4224764",
  "lon": "-122.0842499",
  "display_name": "1600 Amphitheatre Parkway, Mountain View, CA 94043, United States",
  "class": "place",
  "type": "house",
  "address": {
    "house_number": "1600",
    "road": "Amphitheatre Parkway",
    "city": "Mountain View",
    "state": "California",
    "postcode": "94043",
    "country": "United States",
    "country_code": "us"
  }
}
```

#### 📋 Descripción de los Campos Más Importantes

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `place_id` | int | ID único del lugar |
| `lat` | string | Latitud del lugar |
| `lon` | string | Longitud del lugar |
| `display_name` | string | Nombre completo del lugar |
| `address` | object | Detalles estructurados de la dirección |
| `address.house_number` | string | Número de casa |
| `address.road` | string | Nombre de la calle |
| `address.city` | string | Ciudad |
| `address.country` | string | País |

---

## ⚠️ Manejo de Errores

### 📊 Códigos HTTP Estándar

Nominatim utiliza códigos HTTP estándar para indicar el estado de las peticiones:

| Código HTTP | Significado | Causa Común |
|-------------|-------------|-------------|
| `200` ✅ | OK | Petición exitosa |
| `400` ❌ | Bad Request | Parámetros inválidos o faltantes |
| `403` 🚫 | Forbidden | User-Agent no proporcionado o bloqueado |
| `404` 🔍 | Not Found | No se encontró una ubicación para las coordenadas (reverse geocoding) |
| `422` 📝 | Unprocessable Content | Parámetros con formato inválido (ej: string donde se espera número) |
| `429` ⏱️ | Too Many Requests | Límite de peticiones excedido (rate limiting) |
| `500` 🔥 | Internal Server Error | Error interno del servidor de Nominatim |
| `503` 🔧 | Service Unavailable | Servicio temporalmente no disponible |

---

### 🔍 Ejemplo de Respuesta de Error (Recurso No Encontrado - 404)

**Petición (Reverse Geocoding):**
```http
GET /api/nominatim/reverse?lat=0&lon=0
```

**Respuesta:**
```http
HTTP/1.1 404 Not Found
```

```json
{
  "detail": "Error 404 Not Found: No se encontró una dirección para las coordenadas (0.0, 0.0)"
}
```

**Explicación:** No se encontró una dirección válida para las coordenadas proporcionadas (0, 0 está en el océano). Nuestra aplicación lo detecta y responde con código HTTP 404.

---

### 🚫 Ejemplo de Error de User-Agent Faltante (403)

**Petición:**
```http
GET /api/nominatim/search?q=New+York
```

**Respuesta:**
```http
HTTP/1.1 403 Forbidden
```

```json
{
  "detail": "Error 403 Forbidden: User-Agent requerido o acceso denegado"
}
```

**Explicación:** Nominatim requiere un header `User-Agent` para identificar la aplicación. Si Nominatim rechaza la petición por falta de User-Agent, nuestra aplicación lo detecta y responde con código HTTP 403.

---

### 🔍 Ejemplo de Error de Búsqueda Sin Resultados (404)

**Petición:**
```http
GET /api/nominatim/search?q=xyzabc123nonexistentplace
```

**Respuesta:**
```http
HTTP/1.1 404 Not Found
```

```json
{
  "detail": "Error 404 Not Found: No se encontraron ubicaciones para 'xyzabc123nonexistentplace'"
}
```

**Explicación:** No se encontraron ubicaciones que coincidan con el término de búsqueda. Nominatim devuelve un array vacío, y nuestra aplicación lo detecta y responde con código HTTP 404.

---

### ⏱️ Ejemplo de Error de Rate Limiting (429)

**Petición:**
```http
GET /api/nominatim/search?q=New+York
```

**Respuesta:**
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

```json
{
  "detail": "Error 429 Too Many Requests: Límite de peticiones excedido. Por favor, intenta más tarde"
}
```

**Explicación:** Se ha excedido el límite de peticiones permitidas. Nominatim tiene límites de rate limiting para proteger el servicio. Nuestra aplicación detecta el código HTTP 429 y responde con un mensaje descriptivo.

> 💡 **Nota:** Nominatim recomienda no hacer más de 1 petición por segundo. Para uso intensivo, se recomienda instalar una instancia propia de Nominatim.

---

### ❌ Ejemplo de Error de Parámetros Inválidos (400)

**Petición:**
```http
GET /api/nominatim/reverse?lat=100&lon=-200
```

**Respuesta:**
```http
HTTP/1.1 400 Bad Request
```

```json
{
  "detail": "Error 400 Bad Request: La latitud debe estar entre -90 y 90"
}
```

**Explicación:** Las coordenadas están fuera del rango válido (latitud debe estar entre -90 y 90, longitud entre -180 y 180). Nuestra aplicación valida esto antes de hacer la petición y responde con código HTTP 400.

---

### 📝 Ejemplo de Error de Formato Inválido (422)

**Petición:**
```http
GET /api/nominatim/reverse?lat=37.4224764&lon=a
```

**Respuesta:**
```http
HTTP/1.1 422 Unprocessable Content
```

```json
{
  "detail": "Error 422 Unprocessable Content: query -> lon: value is not a valid float"
}
```

**Explicación:** El parámetro `lon` tiene un formato inválido (se espera un número pero se recibió "a"). FastAPI valida automáticamente los tipos de parámetros y responde con código HTTP 422 cuando el formato no es válido.

---

### 🔥 Ejemplo de Error de Servidor Interno (500)

**Petición:**
```http
GET /api/nominatim/search?q=New+York
```

**Respuesta:**
```http
HTTP/1.1 500 Internal Server Error
```

```json
{
  "detail": "Error 500 Internal Server Error: Error interno del servidor"
}
```

**Explicación:** Ocurrió un error interno en el servidor de Nominatim. Nuestra aplicación detecta el código HTTP 500 y responde con un mensaje descriptivo.

---

### 🔧 Ejemplo de Error de Servicio No Disponible (503)

**Petición:**
```http
GET /api/nominatim/search?q=New+York
```

**Respuesta:**
```http
HTTP/1.1 503 Service Unavailable
```

```json
{
  "detail": "Error 503 Service Unavailable: Servicio temporalmente no disponible"
}
```

**Explicación:** El servicio de Nominatim está temporalmente no disponible (mantenimiento, sobrecarga, etc.). Nuestra aplicación detecta el código HTTP 503 y responde con un mensaje descriptivo.

---

## 🚀 Endpoints de la Aplicación Local

### 1️⃣ Buscar Direcciones (Geocoding) 🔍

| Campo | Descripción |
|-------|-------------|
| **URL** | `/api/nominatim/search` |
| **Método HTTP** | `GET` |

#### 📝 Parámetros

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `q` | string | ✅ Sí | Dirección o nombre de lugar a buscar |
| `limit` | int | ❌ No | Número máximo de resultados (1-50, por defecto 10) |

#### 📤 Ejemplo de Petición

```http
GET /api/nominatim/search?q=1600+Amphitheatre+Parkway,+Mountain+View&limit=5
```

#### ✅ Ejemplo de Respuesta Exitosa

```json
{
  "results": [
    {
      "place_id": 123456,
      "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
      "osm_type": "way",
      "osm_id": 123456,
      "lat": "37.4224764",
      "lon": "-122.0842499",
      "display_name": "1600 Amphitheatre Parkway, Mountain View, CA 94043, United States",
      "class": "place",
      "type": "house",
      "importance": 0.5,
      "address": {
        "house_number": "1600",
        "road": "Amphitheatre Parkway",
        "city": "Mountain View",
        "state": "California",
        "postcode": "94043",
        "country": "United States",
        "country_code": "us"
      }
    }
  ],
  "total": 1,
  "query": "1600 Amphitheatre Parkway, Mountain View"
}
```

---

### 2️⃣ Convertir Coordenadas a Dirección (Reverse Geocoding) 🔄

| Campo | Descripción |
|-------|-------------|
| **URL** | `/api/nominatim/reverse` |
| **Método HTTP** | `GET` |

#### 📝 Parámetros

| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `lat` | float | ✅ Sí | Latitud (-90 a 90) |
| `lon` | float | ✅ Sí | Longitud (-180 a 180) |

#### 📤 Ejemplo de Petición

```http
GET /api/nominatim/reverse?lat=37.4224764&lon=-122.0842499
```

#### ✅ Ejemplo de Respuesta Exitosa

```json
{
  "place_id": 123456,
  "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
  "osm_type": "way",
  "osm_id": 123456,
  "lat": "37.4224764",
  "lon": "-122.0842499",
  "display_name": "1600 Amphitheatre Parkway, Mountain View, CA 94043, United States",
  "class": "place",
  "type": "house",
  "address": {
    "house_number": "1600",
    "road": "Amphitheatre Parkway",
    "city": "Mountain View",
    "state": "California",
    "postcode": "94043",
    "country": "United States",
    "country_code": "us"
  },
  "lat_input": 37.4224764,
  "lon_input": -122.0842499
}
```

---

## ⚙️ Configuración

### 🔐 Variables de Entorno (.env)

```env
NOMINATIM_API_BASE_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=GeocodingApp/1.0
```

**Notas importantes:**
- ✅ La API de Nominatim es **gratuita** y no requiere autenticación
- ⚠️ **Es obligatorio** proporcionar un `User-Agent` descriptivo para identificar tu aplicación
- ⏱️ Nominatim tiene límites de rate limiting (recomendado: máximo 1 petición por segundo)
- 🚀 Para uso intensivo, considera instalar tu propia instancia de Nominatim

### 📚 Obtener Acceso a la API

1. 🌐 Visitar [Nominatim.org](https://nominatim.org/)
2. 📖 Revisar la [documentación oficial de la API](https://nominatim.org/release-docs/latest/api/Overview/)
3. ✅ La API pública está disponible sin necesidad de registro
4. 🔧 Para uso intensivo, consulta la [guía de instalación](https://nominatim.org/release-docs/latest/admin/Installation/) para instalar tu propia instancia

---

## 📁 Estructura del Proyecto

```
API/
├── clients/
│   └── nominatimClient.py      # Cliente HTTP para la API de Nominatim
├── controllers/
│   └── nominatimcontroller.py  # Endpoints de la API
├── DTOs/
│   └── nominatimDtos.py        # Modelos de datos (DTOs)
├── services/
│   └── nominatimservices.py    # Lógica de negocio
├── appsettings.py              # Configuración centralizada
├── main.py                     # Punto de entrada de la aplicación
└── README.md                   # Este archivo
```

---

## 🛠️ Instalación y Ejecución

### 📋 Requisitos

- 🐍 Python 3.7+
- 📦 pip (gestor de paquetes de Python)

### 📥 Instalación de Dependencias

```bash
pip install fastapi uvicorn httpx python-dotenv pydantic
```

### ▶️ Ejecutar la Aplicación

```bash
# Modo desarrollo (con recarga automática)
uvicorn main:app --reload

# Modo producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en:
- 🌐 **API**: `http://localhost:8000`
- 📚 **Documentación interactiva (Swagger)**: `http://localhost:8000/docs`
- 📖 **Documentación alternativa (ReDoc)**: `http://localhost:8000/redoc`

---

## 📜 Política de Uso de Nominatim

Nominatim es un servicio **gratuito** basado en OpenStreetMap. Para mantener el servicio disponible para todos, es importante seguir estas políticas:

1. ⏱️ **Rate Limiting**: No hacer más de 1 petición por segundo
2. 🏷️ **User-Agent**: Siempre incluir un User-Agent descriptivo
4. 📝 **Atribución**: Los datos deben atribuirse a OpenStreetMap contributors

Para más información, consulta: [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)

---

## 🔗 Recursos Adicionales

- 📚 [Documentación oficial de Nominatim API](https://nominatim.org/release-docs/latest/api/Overview/)
- 🌐 [Nominatim.org](https://nominatim.org/)
- 🗺️ [OpenStreetMap](https://www.openstreetmap.org/)
- ⚡ [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🔧 [Pydantic Documentation](https://docs.pydantic.dev/)

---
