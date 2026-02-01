"""
=============================================================================
DTOs (DATA TRANSFER OBJECTS) - MODELOS DE DATOS
=============================================================================

Este módulo contiene los DTOs (Data Transfer Objects) utilizados para
estructurar los datos de respuesta de la API de Nominatim.

¿Qué es un DTO?
---------------
Un DTO es un objeto que define la estructura de los datos que se transfieren
entre capas de la aplicación o hacia/desde clientes externos.

¿Por qué usar DTOs en FastAPI?
------------------------------
1. VALIDACIÓN AUTOMÁTICA: Pydantic valida que los datos cumplan el esquema
2. DOCUMENTACIÓN: FastAPI genera docs automáticos (Swagger) basados en los DTOs
3. SERIALIZACIÓN: Convierte automáticamente objetos Python a JSON
4. TYPE HINTS: Mejora el autocompletado y detección de errores en el IDE
5. CONSISTENCIA: Garantiza que todas las respuestas tengan el mismo formato

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# BaseModel es la clase base de Pydantic para definir modelos de datos
# Proporciona validación automática, serialización y documentación
from pydantic import BaseModel, Field
from typing import Optional, List


class AddressDTO(BaseModel):
    """DTO para información de dirección."""
    house_number: Optional[str] = Field(None, description="Número de casa")
    road: Optional[str] = Field(None, description="Nombre de la calle")
    neighbourhood: Optional[str] = Field(None, description="Barrio")
    city: Optional[str] = Field(None, description="Ciudad")
    state: Optional[str] = Field(None, description="Estado/Provincia")
    postcode: Optional[str] = Field(None, description="Código postal")
    country: Optional[str] = Field(None, description="País")
    country_code: Optional[str] = Field(None, description="Código de país (ISO)")

    class Config:
        json_schema_extra = {
            "example": {
                "house_number": "1600",
                "road": "Amphitheatre Parkway",
                "city": "Mountain View",
                "state": "California",
                "postcode": "94043",
                "country": "United States",
                "country_code": "us"
            }
        }


class LocationDTO(BaseModel):
    """DTO para información de una ubicación."""
    place_id: int = Field(..., description="ID único del lugar en Nominatim")
    licence: str = Field(..., description="Licencia de los datos")
    osm_type: Optional[str] = Field(None, description="Tipo de objeto OSM (node, way, relation)")
    osm_id: Optional[int] = Field(None, description="ID del objeto OSM")
    lat: str = Field(..., description="Latitud")
    lon: str = Field(..., description="Longitud")
    display_name: str = Field(..., description="Nombre completo para mostrar")
    class_type: Optional[str] = Field(None, alias="class", description="Clase del lugar")
    type: Optional[str] = Field(None, description="Tipo del lugar")
    importance: Optional[float] = Field(None, description="Importancia del lugar (0-1)")
    address: Optional[AddressDTO] = Field(None, description="Detalles de la dirección")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
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
        }


class GeocodeSearchResponseDTO(BaseModel):
    """DTO para la respuesta de búsqueda de direcciones (geocoding)."""
    results: List[LocationDTO] = Field(..., description="Lista de ubicaciones encontradas")
    total: int = Field(..., description="Número total de resultados")
    query: str = Field(..., description="Término de búsqueda utilizado")

    class Config:
        json_schema_extra = {
            "example": {
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
        }


class ReverseGeocodeResponseDTO(BaseModel):
    """DTO para la respuesta de reverse geocoding (coordenadas a dirección)."""
    place_id: int = Field(..., description="ID único del lugar en Nominatim")
    licence: str = Field(..., description="Licencia de los datos")
    osm_type: Optional[str] = Field(None, description="Tipo de objeto OSM")
    osm_id: Optional[int] = Field(None, description="ID del objeto OSM")
    lat: str = Field(..., description="Latitud")
    lon: str = Field(..., description="Longitud")
    display_name: str = Field(..., description="Nombre completo para mostrar")
    class_type: Optional[str] = Field(None, alias="class", description="Clase del lugar")
    type: Optional[str] = Field(None, description="Tipo del lugar")
    address: Optional[AddressDTO] = Field(None, description="Detalles de la dirección")
    lat_input: float = Field(..., description="Latitud de entrada")
    lon_input: float = Field(..., description="Longitud de entrada")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
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
        }
