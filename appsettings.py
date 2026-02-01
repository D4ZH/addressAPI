"""
=============================================================================
CONFIGURACIÓN CENTRALIZADA DE LA APLICACIÓN
=============================================================================

Este módulo contiene la configuración global de la aplicación, cargando
las variables de entorno desde el archivo .env y exponiendo constantes
de configuración.

¿Por qué usar un archivo de configuración centralizado?
-------------------------------------------------------
1. SEGURIDAD: Las API keys y secretos no se guardan en el código fuente
2. FLEXIBILIDAD: Puedes cambiar configuraciones sin modificar código
3. AMBIENTES: Fácil de tener diferentes configuraciones (dev, staging, prod)
4. MANTENIBILIDAD: Un solo lugar para todas las configuraciones

Contenido del archivo .env (ejemplo):
-------------------------------------
NOMINATIM_API_BASE_URL=https://nominatim.openstreetmap.org
NOMINATIM_USER_AGENT=MyGeocodingApp/1.0

IMPORTANTE: El archivo .env NUNCA debe subirse a Git
Agrégalo a tu .gitignore para proteger tus credenciales

Autor: [Tu nombre]
Fecha: Enero 2026
=============================================================================
"""

# os proporciona funciones para interactuar con el sistema operativo
# Usamos os.getenv() para leer variables de entorno
import os

# python-dotenv permite cargar variables de entorno desde un archivo .env
# Esto es muy útil en desarrollo para no tener que configurar variables
# de entorno del sistema manualmente
from dotenv import load_dotenv


# =============================================================================
# CARGAR VARIABLES DE ENTORNO
# =============================================================================
# load_dotenv() busca un archivo llamado .env en el directorio actual
# y carga todas las variables definidas en él como variables de entorno
# 
# Ejemplo de contenido de .env:
# OPENWEATHER_API_KEY=abc123
# 
# Después de load_dotenv(), puedes acceder con os.getenv("OPENWEATHER_API_KEY")
load_dotenv()


class AppSettings:
    """
    Clase de configuración que contiene todas las constantes de la aplicación.
    
    Usamos una clase en lugar de variables sueltas por las siguientes razones:
    - Agrupa todas las configuraciones en un solo lugar
    - Permite validación y transformación de valores
    - Facilita el autocompletado en el IDE
    - Es más fácil de mockear en tests
    
    Uso:
        from appsettings import AppSettings
        
        api_key = AppSettings.OPENWEATHER_API_KEY
        timeout = AppSettings.TIMEOUT_SECONDS
    
    Nota: Todos los atributos son de clase (class attributes), no de instancia.
    Esto significa que no necesitas crear una instancia para usarlos:
        AppSettings.OPENWEATHER_API_KEY  # ✓ Correcto
        AppSettings().OPENWEATHER_API_KEY  # También funciona, pero innecesario
    """

    # =========================================================================
    # CONFIGURACIÓN DE LA API DE NOMINATIM
    # =========================================================================
    
    # URL base de la API de Nominatim
    # Documentación: https://nominatim.org/release-docs/latest/api/Overview/
    # Nominatim es un servicio gratuito de geocoding basado en OpenStreetMap
    # Ejemplo: https://nominatim.openstreetmap.org/search?q=1600+Amphitheatre+Parkway
    NOMINATIM_API_BASE_URL = os.getenv("NOMINATIM_API_BASE_URL", "https://nominatim.openstreetmap.org")
    
    # User-Agent requerido por Nominatim para identificar la aplicación
    # Es importante usar un User-Agent descriptivo para ayudar a Nominatim
    # a identificar y contactar a los usuarios en caso de uso excesivo
    NOMINATIM_USER_AGENT = os.getenv("NOMINATIM_USER_AGENT", "GeocodingApp/1.0")

    # =========================================================================
    # CONFIGURACIÓN DE LLAMADAS HTTP
    # =========================================================================
    
    # Tiempo máximo de espera para las peticiones HTTP (en segundos)
    # Si la API de Nominatim no responde en este tiempo, se lanza un error
    # Un valor muy bajo puede causar errores en redes lentas
    # Un valor muy alto puede hacer que la aplicación parezca "colgada"
    TIMEOUT_SECONDS = 10
    
    # Límite de resultados por defecto en búsquedas
    # Nominatim permite hasta 50 resultados por búsqueda
    DEFAULT_LIMIT = 10