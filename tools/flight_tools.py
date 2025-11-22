"""
Herramientas del agente de VuelaConNosotros
Estas herramientas permiten al agente interactuar con el sistema de vuelos
"""

from langchain.tools import tool
from data.flights import get_flight_status, find_alternatives, create_booking


@tool
def check_flight_status(flight_number: str) -> str:
    """
    Verifica el estado actual de un vuelo específico.
    
    Usa esta herramienta cuando el usuario pregunte por el estado de un vuelo
    o cuando necesites confirmar información de un vuelo antes de proceder.
    
    Args:
        flight_number: El número de vuelo a consultar (ej: ITTI-FLY-001)
    
    Returns:
        Información detallada del estado del vuelo
    """
    result = get_flight_status(flight_number)
    
    if not result["found"]:
        return f"❌ {result['error']}"
    
    flight = result["flight"]
    status_emoji = {
        "CANCELLED": "❌",
        "AVAILABLE": "✅",
        "DELAYED": "⏰"
    }
    
    emoji = status_emoji.get(flight["status"], "ℹ️")
    
    response = f"""
{emoji} **Estado del Vuelo {flight['number']}**

Ruta: {flight['origin']} → {flight['destination']}
Horario programado: {flight['scheduled_time']}
Estado: {flight['status']}
"""
    
    if flight["status"] == "CANCELLED":
        response += f"Motivo: {flight.get('reason', 'No especificado')}\n"
    elif flight.get("available_seats"):
        response += f"Asientos disponibles: {flight['available_seats']}\n"
        if flight.get("departure_day"):
            departure_day_label = "Hoy" if flight["departure_day"] == "today" else "Mañana"
            response += f"Fecha de salida: {departure_day_label}\n"
    
    return response.strip()


@tool
def find_alternative_flights(cancelled_flight_number: str) -> str:
    """
    Busca vuelos alternativos disponibles para un vuelo cancelado.
    
    Usa esta herramienta cuando el usuario acepte ver opciones alternativas
    o cuando necesites mostrar las alternativas disponibles.
    
    Args:
        cancelled_flight_number: El número del vuelo cancelado (ej: ITTI-FLY-001)
    
    Returns:
        Lista de vuelos alternativos disponibles con todos los detalles
    """
    result = find_alternatives(cancelled_flight_number)
    
    if not result["found"]:
        return f"❌ {result['error']}"
    
    original = result["original_flight"]
    alternatives = result["alternatives"]
    
    response = f"""✈️ **Vuelos alternativos disponibles**

Vuelo original cancelado: {original['number']}
Ruta: {original['origin']} → {original['destination']}
Horario original: {original['scheduled_time']}

**Alternativas disponibles ({result['count']} opciones):**

"""
    
    for idx, flight in enumerate(alternatives, 1):
        departure_day_label = "Hoy" if flight["departure_day"] == "today" else "Mañana"

        response += f"""
**Opción {idx}: {flight['number']}**
• Destino: {flight['destination']}
• {departure_day_label} - Salida: {flight['scheduled_time']}
• Asientos disponibles: {flight['available_seats']}
• Clase: {flight['class']}
• Estado: {flight['status']}

"""
    
    response += "\n💡 **Recomendación:** Le sugiero la Opción 1 por su horario conveniente y buena disponibilidad.\n\n¿Cuál opción de vuelo prefiere? (Puede indicar 1, 2, 3 o el número de vuelo)"

    return response.strip()


@tool
def make_booking(passenger_name: str, flight_number: str) -> str:
    """
    Realiza una nueva reserva para un pasajero en un vuelo específico.

    Usa esta herramienta solo cuando el usuario confirme explícitamente
    que desea reservar un vuelo específico.

    Args:
        passenger_name: Nombre completo del pasajero
        flight_number: Número del vuelo a reservar (ej: ITTI-FLY-021)

    Returns:
        Confirmación de la reserva con código de referencia
    """
    result = create_booking(passenger_name, flight_number)

    if not result["success"]:
        error_msg = result['error']

        # Mensaje empático y profesional cuando no hay asientos
        if "no hay asientos disponibles" in error_msg.lower():
            return f"""😔 **Lamentamos informarle que el vuelo {flight_number} ya no tiene asientos disponibles.**

Esto puede ocurrir cuando varios pasajeros reservan simultáneamente. Entendemos que esto es frustrante.

✈️ **¿Qué podemos hacer ahora?**

Permítame mostrarle las otras opciones disponibles que tenemos para su destino. Todas son igualmente convenientes y le garantizarán llegar a su destino.

¿Desea que le muestre las alternativas disponibles?"""

        # Otros errores (vuelo no disponible, etc.)
        return f"❌ {error_msg}\n\nPermítame ayudarle a encontrar otra opción. ¿Desea ver los vuelos alternativos disponibles?"
    
    booking = result["booking"]
    flight = booking["flight_details"]
    
    departure_day_label = "Hoy" if flight["departure_day"] == "today" else "Mañana"
    
    response = f"""
✅ **¡Reserva Confirmada!**

Código de Confirmación: **{booking['confirmation_code']}**
Pasajero: {booking['passenger_name']}
Vuelo: {flight['number']}
Ruta: {flight['origin']} → {flight['destination']}
Horario: {flight['scheduled_time']} ({departure_day_label})
Clase: {flight['class']}

📧 Le hemos enviado los detalles de su reserva por email.
📱 Puede hacer check-in online 24 horas antes del vuelo.

⚠️ **Importante:**
• Llegue al aeropuerto con 2 horas de anticipación
• Recuerde llevar su documento de identidad
• Su código de confirmación es: {booking['confirmation_code']}

¿Necesita ayuda con algo más?
"""
    
    return response.strip()


def get_flight_tools():
    """
    Retorna la lista de herramientas disponibles para el agente.
    """
    return [
        check_flight_status,
        find_alternative_flights,
        make_booking
    ]
