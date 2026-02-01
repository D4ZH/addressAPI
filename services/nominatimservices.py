"""
=============================================================================
SERVICIO DE NOMINATIM (CAPA DE LÓGICA DE NEGOCIO)
=============================================================================

Este módulo contiene la clase NominatimService que implementa la lógica de
negocio para obtener información de geocoding de Nominatim.

En una arquitectura de capas (Layered Architecture), este servicio actúa
como intermediario entre:
- Controladores (reciben las peticiones HTTP)
- Clientes (se comunican con APIs externas)
- DTOs (definen la estructura de los datos de respuesta)

Responsabilidades de este servicio:
1. Validar la entrada del usuario
2. Coordinar las llamadas al cliente de Nominatim
3. Transformar los datos crudos de la API en DTOs estructurados
4. Manejar errores de configuración

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# httpx es la librería para peticiones HTTP asíncronas
# La usamos para tipar el parámetro http_client
import httpx

# HTTPException permite lanzar errores HTTP que FastAPI convierte en respuestas
from fastapi import HTTPException

# Importamos el cliente que se comunica con la API de Nominatim
# Este cliente encapsula toda la lógica de HTTP
from clients.nominatimClient import NominatimClient

# Importamos los DTOs (Data Transfer Objects) que definen la estructura de respuesta
# Usar DTOs garantiza que siempre devolvamos datos con el formato correcto
from DTOs.nominatimDtos import (
    GeocodeSearchResponseDTO,
    ReverseGeocodeResponseDTO,
    LocationDTO,
    AddressDTO
)

# Importamos la configuración centralizada de la aplicación
from appsettings import AppSettings


class NominatimService:
    """
    Servicio principal para obtener información de geocoding de Nominatim.
    
    Esta clase implementa el patrón de diseño "Service Layer", que separa
    la lógica de negocio de los controladores y los clientes HTTP.
    
    Ventajas de usar un servicio:
    - Los controladores quedan simples (solo reciben y responden)
    - La lógica de negocio es reutilizable
    - Facilita el testing unitario
    - Permite agregar validaciones, caché, logging, etc.
    
    Atributos:
        client (NominatimClient): Instancia del cliente HTTP para Nominatim
    
    Ejemplo de uso:
        async with httpx.AsyncClient() as http_client:
            service = NominatimService()
            results = await service.search_address("1600 Amphitheatre Parkway, Mountain View", 10, http_client)
            print(results.results[0].lat, results.results[0].lon)
    """

    def __init__(self):
        """
        Constructor del servicio.
        
        Inicializa el servicio creando una instancia del cliente de Nominatim.
        """
        # Creamos una instancia del cliente de Nominatim
        # Este cliente se reutilizará en todas las llamadas del servicio
        self.client = NominatimClient()

    async def search_address(
        self, 
        query: str, 
        limit: int, 
        http_client: httpx.AsyncClient
    ) -> GeocodeSearchResponseDTO:
        """
        Busca direcciones en Nominatim y devuelve los resultados en formato estructurado.
        
        Args:
            query (str): Dirección o nombre de lugar a buscar
            limit (int): Número máximo de resultados a retornar
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono.
        
        Returns:
            GeocodeSearchResponseDTO: Objeto estructurado con las ubicaciones encontradas
        
        Raises:
            HTTPException(400): Si el término de búsqueda está vacío
            HTTPException(404): Si no se encontraron resultados
            HTTPException(500): Si hay un error con la API de Nominatim
        """
        # Limpiamos el término de búsqueda
        query = query.strip()
        
        if not query:
            raise HTTPException(
                status_code=400,
                detail="Error 400 Bad Request: El término de búsqueda no puede estar vacío"
            )

        # Obtenemos los datos de la API de Nominatim
        search_data = await self.client.search_address(query, limit, http_client)

        # Verificamos si hay resultados
        if not search_data:
            raise HTTPException(
                status_code=404,
                detail=f"Error 404 Not Found: No se encontraron ubicaciones para '{query}'"
            )

        # Transformamos los datos crudos en DTOs estructurados
        locations = []
        for location_data in search_data:
            location = self._build_location_dto(location_data)
            locations.append(location)

        return GeocodeSearchResponseDTO(
            results=locations,
            total=len(locations),
            query=query
        )

    async def reverse_geocode(
        self, 
        lat: float, 
        lon: float, 
        http_client: httpx.AsyncClient
    ) -> ReverseGeocodeResponseDTO:
        """
        Convierte coordenadas a una dirección usando Nominatim.
        
        Args:
            lat (float): Latitud
            lon (float): Longitud
            http_client (httpx.AsyncClient): Cliente HTTP asíncrono
        
        Returns:
            ReverseGeocodeResponseDTO: Objeto estructurado con información de la dirección
        
        Raises:
            HTTPException(400): Si las coordenadas están fuera de rango
            HTTPException(404): Si no se encontró una dirección para las coordenadas
            HTTPException(500): Si hay un error con la API de Nominatim
        """
        # Validamos las coordenadas
        if not (-90 <= lat <= 90):
            raise HTTPException(
                status_code=400,
                detail="Error 400 Bad Request: La latitud debe estar entre -90 y 90"
            )
        
        if not (-180 <= lon <= 180):
            raise HTTPException(
                status_code=400,
                detail="Error 400 Bad Request: La longitud debe estar entre -180 y 180"
            )

        # Obtenemos los datos de la API de Nominatim
        reverse_data = await self.client.reverse_geocode(lat, lon, http_client)

        # Construimos el DTO con información detallada
        address = None
        if reverse_data.get("address"):
            address = self._build_address_dto(reverse_data["address"])

        return ReverseGeocodeResponseDTO(
            place_id=reverse_data["place_id"],
            licence=reverse_data.get("licence", ""),
            osm_type=reverse_data.get("osm_type"),
            osm_id=reverse_data.get("osm_id"),
            lat=reverse_data["lat"],
            lon=reverse_data["lon"],
            display_name=reverse_data["display_name"],
            class_type=reverse_data.get("class"),
            type=reverse_data.get("type"),
            address=address,
            lat_input=lat,
            lon_input=lon
        )

    def _build_location_dto(self, location_data: dict) -> LocationDTO:
        """
        Construye un LocationDTO a partir de los datos crudos de la API.
        
        Args:
            location_data (dict): Datos crudos de la ubicación desde la API
        
        Returns:
            LocationDTO: Objeto DTO estructurado
        """
        address = None
        if location_data.get("address"):
            address = self._build_address_dto(location_data["address"])

        return LocationDTO(
            place_id=location_data["place_id"],
            licence=location_data.get("licence", ""),
            osm_type=location_data.get("osm_type"),
            osm_id=location_data.get("osm_id"),
            lat=location_data["lat"],
            lon=location_data["lon"],
            display_name=location_data["display_name"],
            class_type=location_data.get("class"),
            type=location_data.get("type"),
            importance=location_data.get("importance"),
            address=address
        )

    def _build_address_dto(self, address_data: dict) -> AddressDTO:
        """
        Construye un AddressDTO a partir de los datos crudos de la API.
        
        Args:
            address_data (dict): Datos crudos de la dirección desde la API
        
        Returns:
            AddressDTO: Objeto DTO estructurado
        """
        return AddressDTO(
            house_number=address_data.get("house_number"),
            road=address_data.get("road"),
            neighbourhood=address_data.get("neighbourhood"),
            city=address_data.get("city"),
            state=address_data.get("state"),
            postcode=address_data.get("postcode"),
            country=address_data.get("country"),
            country_code=address_data.get("country_code")
        )
