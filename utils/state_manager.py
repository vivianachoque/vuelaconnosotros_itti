"""
State Manager - Máquina de Estados Finitos para el Agente de Vuelos
Trackea el progreso del usuario a través del flujo de cancelación y rebooking.

FSM Simplificado: 4 estados que reflejan los 2 flujos principales del negocio.
"""

from enum import Enum
from datetime import datetime
from typing import List, Tuple


class ConversationState(Enum):
    """Estados posibles en el flujo de conversación (simplificado)"""
    NOTIFIED = "notified"      # Usuario fue notificado de la cancelación
    REBOOKING = "rebooking"    # Usuario está en proceso de rebooking (búsqueda + selección + reserva)
    REFUND = "refund"          # Usuario solicitó reembolso
    RESOLVED = "resolved"      # Problema resuelto (reserva confirmada o reembolso procesado)


class StateManager:
    """
    Gestiona el estado de la conversación de forma simplificada.

    Responsabilidades:
    - Trackear estado actual (4 estados principales)
    - Detectar interrupciones en el flujo
    - Mantener historial de transiciones
    - Proveer métricas del flujo

    Filosofía de diseño:
    Los micro-estados (buscando, seleccionando, confirmando) son detalles de
    implementación que el agente maneja internamente. El FSM solo trackea los
    estados que importan al negocio: ¿Está rebooking o pidiendo reembolso?
    """

    def __init__(self):
        """Inicializar el state manager"""
        self.current_state = ConversationState.NOTIFIED
        self.previous_state = None
        self.interruption_count = 0
        self.state_history: List[Tuple[ConversationState, str]] = []
        self._add_to_history(ConversationState.NOTIFIED)

    def _add_to_history(self, state: ConversationState):
        """Agregar transición al historial"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.state_history.append((state, timestamp))

    def transition_to(self, new_state: ConversationState):
        """Transición explícita a un nuevo estado"""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self._add_to_history(new_state)

    def update_state(self, user_message: str, agent_response: str):
        """
        Actualizar el estado basándose en el mensaje del usuario y la respuesta del agente.

        Lógica simplificada:
        - Detecta si el usuario pide REBOOKING (vuelos, alternativas, opciones)
        - Detecta si el usuario pide REEMBOLSO (reembolso, devolución, dinero)
        - Detecta cuando se RESUELVE (confirmación en respuesta del agente)
        - Detecta INTERRUPCIONES (cambio de flujo mid-conversation)

        Args:
            user_message: Lo que dijo el usuario
            agent_response: Lo que respondió el agente
        """
        user_lower = user_message.lower()
        agent_lower = agent_response.lower()

        # 1. Detectar si el problema se resolvió (estado final)
        resolution_keywords = [
            # Keywords para rebooking exitoso
            "reserva confirmada", "booking confirmado", "¡reserva confirmada!",
            "código de confirmación", "reserva exitosa",
            # Keywords para reembolso exitoso (más variaciones)
            "reembolso confirmado", "reembolso procesado", "devolución confirmada",
            "✅ reembolso", "reembolso exitoso", "hemos procesado su reembolso",
            "su reembolso ha sido", "reembolso aprobado"
        ]

        if any(keyword in agent_lower for keyword in resolution_keywords):
            if self.current_state != ConversationState.RESOLVED:
                self.transition_to(ConversationState.RESOLVED)
                return

        # 2. Detectar inicio de REBOOKING (Flujo A) - PRIMERO porque es más específico
        rebooking_keywords = [
            "vuelo", "vuelos", "alternativas", "opciones", "disponibles",
            "muéstr", "busca", "ver", "reserva", "reservar", "booking"
        ]

        if any(keyword in user_lower for keyword in rebooking_keywords):
            # Detectar interrupción: estaba en reembolso y ahora pide rebooking
            if self.current_state == ConversationState.REFUND:
                self.interruption_count += 1

            # También detectar si el agente muestra opciones
            if self.current_state == ConversationState.NOTIFIED:
                if any(kw in agent_lower for kw in ["opciones", "alternativas", "vuelos disponibles"]):
                    self.transition_to(ConversationState.REBOOKING)
                    return

            if self.current_state != ConversationState.REBOOKING:
                self.transition_to(ConversationState.REBOOKING)
                return

        # 3. Detectar solicitud de REEMBOLSO (Flujo B) - SEGUNDO
        refund_keywords = [
            "reembolso", "devol", "dinero", "plata",
            "refund", "money back", "me devuelvan"
        ]

        if any(keyword in user_lower for keyword in refund_keywords):
            # Detectar interrupción: estaba en rebooking y ahora pide reembolso
            if self.current_state == ConversationState.REBOOKING:
                self.interruption_count += 1

            if self.current_state != ConversationState.REFUND:
                self.transition_to(ConversationState.REFUND)
                return

    def get_current_state(self) -> ConversationState:
        """Obtener el estado actual"""
        return self.current_state

    def get_interruption_count(self) -> int:
        """Obtener el número de interrupciones (cambios de flujo)"""
        return self.interruption_count

    def get_state_history(self) -> List[Tuple[ConversationState, str]]:
        """Obtener el historial completo de estados"""
        return self.state_history

    def has_reached_state(self, state: ConversationState) -> bool:
        """Verificar si alguna vez se alcanzó un estado específico"""
        return any(s == state for s, _ in self.state_history)

    def get_progress_percentage(self) -> int:
        """
        Calcular el porcentaje de progreso en el flujo.

        Flujo A - Rebooking:
        NOTIFIED(25%) → REBOOKING(50%) → RESOLVED(100%)

        Flujo B - Reembolso:
        NOTIFIED(25%) → REFUND(50%) → RESOLVED(100%)
        """
        state_weights = {
            ConversationState.NOTIFIED: 25,
            ConversationState.REBOOKING: 50,
            ConversationState.REFUND: 50,
            ConversationState.RESOLVED: 100,
        }

        # Buscar el estado de mayor progreso alcanzado
        max_progress = 0
        for state, _ in self.state_history:
            progress = state_weights.get(state, 0)
            max_progress = max(max_progress, progress)

        return max_progress

    def get_state_emoji(self, state: ConversationState) -> str:
        """Obtener emoji representativo del estado"""
        emojis = {
            ConversationState.NOTIFIED: "📢",
            ConversationState.REBOOKING: "✈️",
            ConversationState.REFUND: "💰",
            ConversationState.RESOLVED: "✅",
        }
        return emojis.get(state, "❓")

    def get_state_label(self, state: ConversationState) -> str:
        """Obtener etiqueta legible del estado"""
        if state is None:
            return "Sin Estado"

        labels = {
            ConversationState.NOTIFIED: "Pasajero notificado",
            ConversationState.REBOOKING: "Procesando rebooking",
            ConversationState.REFUND: "Procesando reembolso",
            ConversationState.RESOLVED: "Problema resuelto",
        }
        return labels.get(state, "Desconocido")

    def is_final_state(self) -> bool:
        """
        Verificar si el flujo está completo (100%).
        Después de este punto, cambios requieren llamar al 0800.
        """
        return self.current_state == ConversationState.RESOLVED

    def needs_confirmation(self) -> bool:
        """
        Verificar si se necesita confirmación del usuario.

        Por ahora, esta funcionalidad está deshabilitada ya que el agente
        maneja las confirmaciones internamente a través de los prompts.

        Returns:
            False siempre (confirmaciones manejadas por el agente)
        """
        return False
