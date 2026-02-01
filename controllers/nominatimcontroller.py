"""
=============================================================================
CONTROLADOR DE NOMINATIM (CAPA DE PRESENTACIÓN)
=============================================================================

Este módulo contiene los endpoints de la API relacionados con Nominatim.
Los controladores son responsables de:
- Recibir las peticiones HTTP
- Validar los parámetros de entrada
- Llamar a los servicios correspondientes
- Devolver las respuestas estructuradas

Endpoints disponibles:
- GET /api/nominatim/search - Buscar direcciones y convertir a coordenadas
- GET /api/nominatim/reverse - Convertir coordenadas a dirección

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

import httpx
from fastapi import APIRouter, Query
from services.nominatimservices import NominatimService
from DTOs.nominatimDtos import (
    GeocodeSearchResponseDTO,
    ReverseGeocodeResponseDTO
)
from appsettings import AppSettings

# Creamos el router con el prefijo /api/nominatim
# Esto significa que todas las rutas aquí definidas comenzarán con /api/nominatim
router = APIRouter(prefix="/api/nominatim", tags=["Nominatim"])


@router.get(
    "/search",
    response_model=GeocodeSearchResponseDTO,
    summary="Buscar direcciones y convertir a coordenadas",
    description="Busca direcciones en Nominatim y las convierte a coordenadas (latitud, longitud)"
)
async def search_address(
    q: str = Query(..., description="Dirección o nombre de lugar a buscar", example="1600 Amphitheatre Parkway, Mountain View"),
    limit: int = Query(default=10, ge=1, le=50, description="Número máximo de resultados (máximo 50)")
):
    """
    Busca direcciones en la API de Nominatim y las convierte a coordenadas.
    
    Este endpoint permite buscar direcciones por nombre, dirección completa,
    o cualquier término relacionado con ubicaciones geográficas.
    
    Args:
        q: Dirección o nombre de lugar a buscar
        limit: Número máximo de resultados (entre 1 y 50)
    
    Returns:
        GeocodeSearchResponseDTO: Lista de ubicaciones encontradas con sus coordenadas
    
    Ejemplo:
        GET /api/nominatim/search?q=1600 Amphitheatre Parkway, Mountain View&limit=5
    """
    async with httpx.AsyncClient() as http_client:
        nominatim_service = NominatimService()
        search_response = await nominatim_service.search_address(q, limit, http_client)
        return search_response


@router.get(
    "/reverse",
    response_model=ReverseGeocodeResponseDTO,
    summary="Convertir coordenadas a dirección",
    description="Convierte coordenadas (latitud, longitud) a una dirección usando Nominatim"
)
async def reverse_geocode(
    lat: float = Query(..., description="Latitud (-90 a 90)", example=37.4224764, ge=-90, le=90),
    lon: float = Query(..., description="Longitud (-180 a 180)", example=-122.0842499, ge=-180, le=180)
):
    """
    Convierte coordenadas (latitud, longitud) a una dirección.
    
    Este endpoint realiza reverse geocoding, encontrando la dirección más cercana
    para las coordenadas proporcionadas.
    
    Args:
        lat: Latitud (debe estar entre -90 y 90)
        lon: Longitud (debe estar entre -180 y 180)
    
    Returns:
        ReverseGeocodeResponseDTO: Información de la dirección correspondiente a las coordenadas
    
    Ejemplo:
        GET /api/nominatim/reverse?lat=37.4224764&lon=-122.0842499
    """
    async with httpx.AsyncClient() as http_client:
        nominatim_service = NominatimService()
        reverse_response = await nominatim_service.reverse_geocode(lat, lon, http_client)
        return reverse_response
