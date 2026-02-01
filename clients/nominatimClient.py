"""
=============================================================================
CLIENTE HTTP PARA LA API DE NOMINATIM
=============================================================================

Este módulo contiene la clase NominatimClient que se encarga de realizar
las peticiones HTTP a la API externa de Nominatim.

La API de Nominatim proporciona acceso a:
- Búsqueda de direcciones y conversión a coordenadas (geocoding)
- Conversión de coordenadas a direcciones (reverse geocoding)
- Búsqueda de lugares por nombre o tipo

Documentación oficial de Nominatim:
- API Docs: https://nominatim.org/release-docs/latest/api/Overview/
- Base URL: https://nominatim.openstreetmap.org

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# httpx es una librería moderna para hacer peticiones HTTP asíncronas en Python
# Es similar a 'requests' pero soporta async/await de forma nativa
import httpx

# HTTPException nos permite lanzar errores HTTP con códigos de estado específicos
# FastAPI los convierte automáticamente en respuestas HTTP apropiadas
from fastapi import HTTPException

# Importamos la configuración centralizada de la aplicación
# Contiene las URLs de la API y otros parámetros
from appsettings import AppSettings


class NominatimClient:
    """
    Cliente HTTP para interactuar con la API de Nominatim.
    
    Esta clase encapsula toda la lógica de comunicación con la API externa,
    siguiendo el patrón de diseño "Client" o "Gateway". Esto permite:
    
    - Separar la lógica de HTTP de la lógica de negocio
    - Facilitar el testing mediante mocks
    - Centralizar el manejo de errores de la API externa
    - Reutilizar el cliente en diferentes servicios si es necesario
    
    Ejemplo de uso:
        async with httpx.AsyncClient() as http_client:
            nominatim_client = NominatimClient()
            results = await nominatim_client.search_address("1600 Amphitheatre Parkway, Mountain View", http_client)
    """

    def __init__(self):
        """
        Constructor de la clase.
        
        Actualmente no requiere inicialización especial, pero se mantiene
        por si en el futuro se necesita inyectar dependencias o configuración.
        """
        pass

    async def search_address(
        self, 
        query: str, 
        limit: int, 
        http_client: httpx.AsyncClient
    ) -> list:
        """
        Busca direcciones en la API de Nominatim y las convierte a coordenadas.
        
        Args:
            query (str): Dirección o nombre de lugar a buscar
            limit (int): Número máximo de resultados a retornar
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido.
        
        Returns:
            list: Lista de diccionarios con los resultados de la búsqueda.
                  Estructura:
                  [
                      {
                          "place_id": 123456,
                          "licence": "...",
                          "osm_type": "way",
                          "osm_id": 123456,
                          "boundingbox": [...],
                          "lat": "37.4224764",
                          "lon": "-122.0842499",
                          "display_name": "1600 Amphitheatre Parkway, Mountain View, CA, USA",
                          "class": "place",
                          "type": "house",
                          "importance": 0.5,
                          ...
                      }
                  ]
        
        Raises:
            HTTPException(status_code): Si hay un error en la API de Nominatim
        """
        # Realizamos la petición GET a la API de búsqueda de Nominatim
        # Nominatim requiere un User-Agent header para identificar la aplicación
        response = await http_client.get(
            f"{AppSettings.NOMINATIM_API_BASE_URL}/search",
            params={
                "q": query,  # Término de búsqueda (dirección)
                "format": "json",  # Formato de respuesta JSON
                "limit": limit,  # Número máximo de resultados
                "addressdetails": 1,  # Incluir detalles de dirección
                "extratags": 1,  # Incluir tags adicionales
                "namedetails": 1  # Incluir nombres alternativos
            },
            headers={
                "User-Agent": AppSettings.NOMINATIM_USER_AGENT
            },
            timeout=AppSettings.TIMEOUT_SECONDS
        )

        # Verificamos si la respuesta fue exitosa y manejamos diferentes códigos de error
        if response.status_code != 200:
            error_detail = self._get_error_message(response.status_code, "buscar dirección")
            raise HTTPException(
                status_code=response.status_code,
                detail=error_detail
            )

        # Convertimos la respuesta JSON a una lista de Python
        data = response.json()

        # Nominatim devuelve una lista vacía si no hay resultados
        if not isinstance(data, list):
            raise HTTPException(
                status_code=500,
                detail="Error 500 Internal Server Error: Respuesta inesperada de la API de Nominatim"
            )

        return data

    async def reverse_geocode(
        self, 
        lat: float, 
        lon: float, 
        http_client: httpx.AsyncClient
    ) -> dict:
        """
        Convierte coordenadas (latitud, longitud) a una dirección.
        
        Args:
            lat (float): Latitud
            lon (float): Longitud
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono compartido
        
        Returns:
            dict: Diccionario con información de la dirección.
                  Estructura:
                  {
                      "place_id": 123456,
                      "licence": "...",
                      "osm_type": "way",
                      "osm_id": 123456,
                      "lat": "37.4224764",
                      "lon": "-122.0842499",
                      "display_name": "1600 Amphitheatre Parkway, Mountain View, CA, USA",
                      "address": {
                          "house_number": "1600",
                          "road": "Amphitheatre Parkway",
                          "city": "Mountain View",
                          "state": "California",
                          "postcode": "94043",
                          "country": "United States",
                          ...
                      },
                      ...
                  }
        
        Raises:
            HTTPException(404): Si no se encontró una dirección para las coordenadas
            HTTPException(status_code): Si hay un error en la API de Nominatim
        """
        response = await http_client.get(
            f"{AppSettings.NOMINATIM_API_BASE_URL}/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "json",
                "addressdetails": 1,
                "extratags": 1,
                "namedetails": 1
            },
            headers={
                "User-Agent": AppSettings.NOMINATIM_USER_AGENT
            },
            timeout=AppSettings.TIMEOUT_SECONDS
        )

        # Verificamos si la respuesta fue exitosa y manejamos diferentes códigos de error
        if response.status_code != 200:
            error_detail = self._get_error_message(response.status_code, "realizar reverse geocoding")
            raise HTTPException(
                status_code=response.status_code,
                detail=error_detail
            )

        data = response.json()

        # Nominatim devuelve un error si no encuentra resultados
        if "error" in data:
            raise HTTPException(
                status_code=404,
                detail=f"Error 404 Not Found: No se encontró una dirección para las coordenadas ({lat}, {lon})"
            )

        return data

    def _get_error_message(self, status_code: int, operation: str) -> str:
        """
        Genera un mensaje de error descriptivo basado en el código HTTP.
        
        Args:
            status_code (int): Código HTTP de error
            operation (str): Operación que se estaba realizando
        
        Returns:
            str: Mensaje de error descriptivo en formato "Error {código} {nombre}: {razón}"
        """
        error_names = {
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
            429: "Too Many Requests",
            500: "Internal Server Error",
            503: "Service Unavailable"
        }
        
        error_reasons = {
            400: "Parámetros inválidos o faltantes",
            403: "User-Agent requerido o acceso denegado",
            404: "Recurso no encontrado",
            429: "Límite de peticiones excedido. Por favor, intenta más tarde",
            500: "Error interno del servidor",
            503: "Servicio temporalmente no disponible"
        }
        
        error_name = error_names.get(status_code, f"HTTP {status_code}")
        error_reason = error_reasons.get(status_code, f"Error HTTP {status_code}")
        
        return f"Error {status_code} {error_name}: {error_reason}"
