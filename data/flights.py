"""
Base de datos mockeada de vuelos
Este módulo simula las respuestas de una API real de aerolínea.
En producción, estas funciones harían llamadas HTTP a la API real.
"""

from datetime import datetime
import random

# Base de datos de vuelos cancelados (ITTI-FLY-001 a 008)
CANCELLED_FLIGHTS = {
    "ITTI-FLY-001": {
        "number": "ITTI-FLY-001",
        "origin": "Buenos Aires (EZE)",
        "destination": "Lima (LIM)",
        "scheduled_time": "14:30",
        "status": "CANCELLED",
        "reason": "Condiciones meteorológicas adversas"
    },
    "ITTI-FLY-002": {
        "number": "ITTI-FLY-002",
        "origin": "Buenos Aires (EZE)",
        "destination": "Santiago (SCL)",
        "scheduled_time": "09:15",
        "status": "CANCELLED",
        "reason": "Problema técnico en la aeronave"
    },
    "ITTI-FLY-003": {
        "number": "ITTI-FLY-003",
        "origin": "Buenos Aires (EZE)",
        "destination": "Bogotá (BOG)",
        "scheduled_time": "11:00",
        "status": "CANCELLED",
        "reason": "Falta de tripulación"
    },
    "ITTI-FLY-004": {
        "number": "ITTI-FLY-004",
        "origin": "Buenos Aires (EZE)",
        "destination": "Ciudad de México (MEX)",
        "scheduled_time": "16:45",
        "status": "CANCELLED",
        "reason": "Condiciones meteorológicas adversas"
    },
    "ITTI-FLY-005": {
        "number": "ITTI-FLY-005",
        "origin": "Buenos Aires (EZE)",
        "destination": "São Paulo (GRU)",
        "scheduled_time": "08:30",
        "status": "CANCELLED",
        "reason": "Problema técnico en la aeronave"
    },
    "ITTI-FLY-006": {
        "number": "ITTI-FLY-006",
        "origin": "Buenos Aires (EZE)",
        "destination": "Montevideo (MVD)",
        "scheduled_time": "19:00",
        "status": "CANCELLED",
        "reason": "Condiciones meteorológicas adversas"
    },
    "ITTI-FLY-007": {
        "number": "ITTI-FLY-007",
        "origin": "Buenos Aires (EZE)",
        "destination": "Asunción (ASU)",
        "scheduled_time": "13:20",
        "status": "CANCELLED",
        "reason": "Falta de tripulación"
    },
    "ITTI-FLY-008": {
        "number": "ITTI-FLY-008",
        "origin": "Buenos Aires (EZE)",
        "destination": "Río de Janeiro (GIG)",
        "scheduled_time": "15:30",
        "status": "CANCELLED",
        "reason": "Problema técnico en la aeronave"
    }
}

# Base de datos de vuelos alternativos disponibles
ALTERNATIVE_FLIGHTS = {
    # Alternativas para ITTI-FLY-001 (Lima)
    "ITTI-FLY-021": {
        "number": "ITTI-FLY-021",
        "origin": "Buenos Aires (EZE)",
        "destination": "Lima (LIM)",
        "scheduled_time": "18:45",
        "status": "AVAILABLE",
        "available_seats": 15,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-022": {
        "number": "ITTI-FLY-022",
        "origin": "Buenos Aires (EZE)",
        "destination": "Lima (LIM)",
        "scheduled_time": "22:30",
        "status": "AVAILABLE",
        "available_seats": 8,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-023": {
        "number": "ITTI-FLY-023",
        "origin": "Buenos Aires (EZE)",
        "destination": "Lima (LIM)",
        "scheduled_time": "10:00",
        "status": "AVAILABLE",
        "available_seats": 22,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-002 (Santiago)
    "ITTI-FLY-024": {
        "number": "ITTI-FLY-024",
        "origin": "Buenos Aires (EZE)",
        "destination": "Santiago (SCL)",
        "scheduled_time": "13:30",
        "status": "AVAILABLE",
        "available_seats": 18,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-025": {
        "number": "ITTI-FLY-025",
        "origin": "Buenos Aires (EZE)",
        "destination": "Santiago (SCL)",
        "scheduled_time": "17:15",
        "status": "AVAILABLE",
        "available_seats": 10,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-026": {
        "number": "ITTI-FLY-026",
        "origin": "Buenos Aires (EZE)",
        "destination": "Santiago (SCL)",
        "scheduled_time": "09:45",
        "status": "AVAILABLE",
        "available_seats": 25,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-003 (Bogotá)
    "ITTI-FLY-027": {
        "number": "ITTI-FLY-027",
        "origin": "Buenos Aires (EZE)",
        "destination": "Bogotá (BOG)",
        "scheduled_time": "15:20",
        "status": "AVAILABLE",
        "available_seats": 12,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-028": {
        "number": "ITTI-FLY-028",
        "origin": "Buenos Aires (EZE)",
        "destination": "Bogotá (BOG)",
        "scheduled_time": "20:00",
        "status": "AVAILABLE",
        "available_seats": 6,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-029": {
        "number": "ITTI-FLY-029",
        "origin": "Buenos Aires (EZE)",
        "destination": "Bogotá (BOG)",
        "scheduled_time": "11:30",
        "status": "AVAILABLE",
        "available_seats": 20,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-004 (Ciudad de México)
    "ITTI-FLY-030": {
        "number": "ITTI-FLY-030",
        "origin": "Buenos Aires (EZE)",
        "destination": "Ciudad de México (MEX)",
        "scheduled_time": "19:30",
        "status": "AVAILABLE",
        "available_seats": 14,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-031": {
        "number": "ITTI-FLY-031",
        "origin": "Buenos Aires (EZE)",
        "destination": "Ciudad de México (MEX)",
        "scheduled_time": "23:45",
        "status": "AVAILABLE",
        "available_seats": 9,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-032": {
        "number": "ITTI-FLY-032",
        "origin": "Buenos Aires (EZE)",
        "destination": "Ciudad de México (MEX)",
        "scheduled_time": "12:15",
        "status": "AVAILABLE",
        "available_seats": 19,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-005 (São Paulo)
    "ITTI-FLY-033": {
        "number": "ITTI-FLY-033",
        "origin": "Buenos Aires (EZE)",
        "destination": "São Paulo (GRU)",
        "scheduled_time": "12:00",
        "status": "AVAILABLE",
        "available_seats": 16,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-034": {
        "number": "ITTI-FLY-034",
        "origin": "Buenos Aires (EZE)",
        "destination": "São Paulo (GRU)",
        "scheduled_time": "16:30",
        "status": "AVAILABLE",
        "available_seats": 11,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-035": {
        "number": "ITTI-FLY-035",
        "origin": "Buenos Aires (EZE)",
        "destination": "São Paulo (GRU)",
        "scheduled_time": "08:45",
        "status": "AVAILABLE",
        "available_seats": 24,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-006 (Montevideo)
    "ITTI-FLY-036": {
        "number": "ITTI-FLY-036",
        "origin": "Buenos Aires (EZE)",
        "destination": "Montevideo (MVD)",
        "scheduled_time": "21:15",
        "status": "AVAILABLE",
        "available_seats": 13,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-037": {
        "number": "ITTI-FLY-037",
        "origin": "Buenos Aires (EZE)",
        "destination": "Montevideo (MVD)",
        "scheduled_time": "07:30",
        "status": "AVAILABLE",
        "available_seats": 17,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    "ITTI-FLY-038": {
        "number": "ITTI-FLY-038",
        "origin": "Buenos Aires (EZE)",
        "destination": "Montevideo (MVD)",
        "scheduled_time": "14:00",
        "status": "AVAILABLE",
        "available_seats": 21,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-007 (Asunción)
    "ITTI-FLY-039": {
        "number": "ITTI-FLY-039",
        "origin": "Buenos Aires (EZE)",
        "destination": "Asunción (ASU)",
        "scheduled_time": "17:45",
        "status": "AVAILABLE",
        "available_seats": 10,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-040": {
        "number": "ITTI-FLY-040",
        "origin": "Buenos Aires (EZE)",
        "destination": "Asunción (ASU)",
        "scheduled_time": "21:30",
        "status": "AVAILABLE",
        "available_seats": 7,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-041": {
        "number": "ITTI-FLY-041",
        "origin": "Buenos Aires (EZE)",
        "destination": "Asunción (ASU)",
        "scheduled_time": "10:30",
        "status": "AVAILABLE",
        "available_seats": 18,
        "departure_day": "tomorrow",
        "class": "Economy"
    },
    
    # Alternativas para ITTI-FLY-008 (Río de Janeiro)
    "ITTI-FLY-042": {
        "number": "ITTI-FLY-042",
        "origin": "Buenos Aires (EZE)",
        "destination": "Río de Janeiro (GIG)",
        "scheduled_time": "18:00",
        "status": "AVAILABLE",
        "available_seats": 15,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-043": {
        "number": "ITTI-FLY-043",
        "origin": "Buenos Aires (EZE)",
        "destination": "Río de Janeiro (GIG)",
        "scheduled_time": "22:15",
        "status": "AVAILABLE",
        "available_seats": 9,
        "departure_day": "today",
        "class": "Economy"
    },
    "ITTI-FLY-044": {
        "number": "ITTI-FLY-044",
        "origin": "Buenos Aires (EZE)",
        "destination": "Río de Janeiro (GIG)",
        "scheduled_time": "11:00",
        "status": "AVAILABLE",
        "available_seats": 23,
        "departure_day": "tomorrow",
        "class": "Economy"
    }
}

# Mapeo de vuelos cancelados a sus alternativas
FLIGHT_ALTERNATIVES_MAP = {
    "ITTI-FLY-001": ["ITTI-FLY-021", "ITTI-FLY-022", "ITTI-FLY-023"],
    "ITTI-FLY-002": ["ITTI-FLY-024", "ITTI-FLY-025", "ITTI-FLY-026"],
    "ITTI-FLY-003": ["ITTI-FLY-027", "ITTI-FLY-028", "ITTI-FLY-029"],
    "ITTI-FLY-004": ["ITTI-FLY-030", "ITTI-FLY-031", "ITTI-FLY-032"],
    "ITTI-FLY-005": ["ITTI-FLY-033", "ITTI-FLY-034", "ITTI-FLY-035"],
    "ITTI-FLY-006": ["ITTI-FLY-036", "ITTI-FLY-037", "ITTI-FLY-038"],
    "ITTI-FLY-007": ["ITTI-FLY-039", "ITTI-FLY-040", "ITTI-FLY-041"],
    "ITTI-FLY-008": ["ITTI-FLY-042", "ITTI-FLY-043", "ITTI-FLY-044"]
}

# Base de datos de reservas (se va llenando)
BOOKINGS_DATABASE = {}


# ============================================================================
# FUNCIONES QUE SIMULAN API CALLS
# En producción, estas harían requests.get() / requests.post() en caso de que querramos escalar al producto.
# ============================================================================

def get_flight_status(flight_number: str) -> dict:
    """
    Simula: GET /api/flights/{flight_number}/status
    
    Retorna información del estado de un vuelo.
    """
    flight_number = flight_number.upper().strip()
    
    # Buscar en vuelos cancelados
    if flight_number in CANCELLED_FLIGHTS:
        return {
            "found": True,
            "flight": CANCELLED_FLIGHTS[flight_number]
        }
    
    # Buscar en vuelos alternativos
    if flight_number in ALTERNATIVE_FLIGHTS:
        return {
            "found": True,
            "flight": ALTERNATIVE_FLIGHTS[flight_number]
        }
    
    # No encontrado
    return {
        "found": False,
        "error": f"Vuelo {flight_number} no encontrado en el sistema"
    }


def find_alternatives(cancelled_flight_number: str) -> dict:
    """
    Simula: GET /api/flights/alternatives?cancelled={flight_number}
    
    Busca vuelos alternativos para un vuelo cancelado.
    """
    cancelled_flight_number = cancelled_flight_number.upper().strip()
    
    # Verificar que el vuelo esté en la lista de cancelados
    if cancelled_flight_number not in CANCELLED_FLIGHTS:
        return {
            "found": False,
            "error": f"El vuelo {cancelled_flight_number} no está en la lista de cancelados"
        }
    
    # Obtener las alternativas
    alternative_numbers = FLIGHT_ALTERNATIVES_MAP.get(cancelled_flight_number, [])
    alternatives = [ALTERNATIVE_FLIGHTS[num] for num in alternative_numbers]
    
    original_flight = CANCELLED_FLIGHTS[cancelled_flight_number]
    
    return {
        "found": True,
        "original_flight": original_flight,
        "alternatives": alternatives,
        "count": len(alternatives)
    }


def create_booking(passenger_name: str, flight_number: str) -> dict:
    """
    Simula: POST /api/bookings

    Crea una nueva reserva para un pasajero en un vuelo específico.
    """
    flight_number = flight_number.upper().strip()
    
    # Verificar que el vuelo existe y está disponible
    if flight_number not in ALTERNATIVE_FLIGHTS:
        return {
            "success": False,
            "error": f"El vuelo {flight_number} no está disponible para reservar"
        }
    
    flight = ALTERNATIVE_FLIGHTS[flight_number]
    
    # Verificar disponibilidad de asientos
    if flight["available_seats"] <= 0:
        return {
            "success": False,
            "error": f"No hay asientos disponibles en el vuelo {flight_number}"
        }
    
    # Generar código de confirmación
    confirmation_code = f"ITTI-{random.randint(100000, 999999)}"
    
    # Crear reserva
    booking = {
        "confirmation_code": confirmation_code,
        "passenger_name": passenger_name,
        "flight_number": flight_number,
        "flight_details": flight,
        "booking_date": datetime.now().isoformat(),
        "status": "CONFIRMED"
    }
    
    # Guardar en base de datos
    BOOKINGS_DATABASE[confirmation_code] = booking
    
    # Reducir asientos disponibles
    ALTERNATIVE_FLIGHTS[flight_number]["available_seats"] -= 1
    
    return {
        "success": True,
        "booking": booking
    }


def get_booking(confirmation_code: str) -> dict:
    """
    Simula: GET /api/bookings/{confirmation_code}
    
    Obtiene información de una reserva por su código de confirmación.
    """
    if confirmation_code in BOOKINGS_DATABASE:
        return {
            "found": True,
            "booking": BOOKINGS_DATABASE[confirmation_code]
        }
    
    return {
        "found": False,
        "error": f"No se encontró reserva con código {confirmation_code}"
    }
