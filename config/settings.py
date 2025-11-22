"""
Configuración centralizada de la aplicación.
"""

from data.flights import CANCELLED_FLIGHTS

# Configuración del modelo
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TEMPERATURE = 0.3

# Función helper para obtener datos de un vuelo cancelado
def get_cancelled_flight_data(flight_number: str) -> dict:
    """
    Obtiene los datos completos de un vuelo cancelado.

    Args:
        flight_number: Número del vuelo (ej: ITTI-FLY-001)

    Returns:
        Diccionario con los datos del vuelo o valores por defecto si no existe
    """
    return CANCELLED_FLIGHTS.get(flight_number, {
        "origin": "Buenos Aires (EZE)",
        "destination": "Lima (LIM)",
        "reason": "Condiciones meteorológicas adversas"
    })

# Datos por defecto del escenario
DEFAULT_PASSENGER_NAME = "Carlos Gonzalez"
DEFAULT_FLIGHT_NUMBER = "ITTI-FLY-001"
DEFAULT_ORIGIN = "Buenos Aires (EZE)"
DEFAULT_DESTINATION = "Lima (LIM)"
DEFAULT_CANCELLATION_REASONS = [
    "Condiciones meteorológicas adversas",
    "Problema técnico en la aeronave",
    "Falta de tripulación"
]

# Lista de vuelos cancelados disponibles
# Los datos completos (origen, destino, horario, razón) se obtienen automáticamente de data/flights.py
AVAILABLE_CANCELLED_FLIGHTS = [
    "ITTI-FLY-001",  # Buenos Aires → Lima (14:30)
    "ITTI-FLY-002",  # Buenos Aires → Santiago (09:15)
    "ITTI-FLY-003",  # Buenos Aires → Bogotá (11:00)
    "ITTI-FLY-004",  # Buenos Aires → Ciudad de México (16:45)
    "ITTI-FLY-005",  # Buenos Aires → São Paulo (08:30)
    "ITTI-FLY-006",  # Buenos Aires → Montevideo (19:00)
    "ITTI-FLY-007",  # Buenos Aires → Asunción (13:20)
    "ITTI-FLY-008"   # Buenos Aires → Río de Janeiro (15:30)
]

# Configuración de Streamlit
PAGE_TITLE = "VuelaConNosotros - Asistente"
PAGE_ICON = "✈️"
LAYOUT = "centered"

# Configuración de UI
ASSISTANT_AVATAR = "✈️"
USER_AVATAR = "👤"

# Estilos personalizados
CUSTOM_CSS = """
<style>
    .proactive-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        border-left: 5px solid #ffd700;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
"""
