import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from utils.state_manager import StateManager, ConversationState
from dotenv import load_dotenv
import os

# Importar configuración, prompts y tools
from config.settings import *
from prompts.system_prompt import get_cancellation_notification, get_system_message
from tools.flight_tools import get_flight_tools

# Cargar variables de entorno
load_dotenv()

# Configuración de página
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

st.title("✈️ VuelaConNosotros - Asistente de Vuelos")
st.markdown("*Gestión inteligente de vuelos con IA*")

# Estilos personalizados
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sidebar con configuración del escenario
with st.sidebar:
    st.header("Configuración del Escenario")
    st.info("Personalizá los datos de la simulación")

    passenger_name = st.text_input("Nombre del Pasajero", DEFAULT_PASSENGER_NAME)

    # Selector de vuelo cancelado
    flight_number = st.selectbox(
        "Vuelo Cancelado",
        AVAILABLE_CANCELLED_FLIGHTS,
        index=0
    )

    # Obtener datos del vuelo seleccionado automáticamente
    from config.settings import get_cancelled_flight_data
    flight_data = get_cancelled_flight_data(flight_number)

    # Campos auto-completados basados en el vuelo seleccionado (solo lectura)
    origin = st.text_input(
        "Origen",
        flight_data["origin"],
        disabled=True,
        help="Se actualiza automáticamente según el vuelo seleccionado"
    )
    destination = st.text_input(
        "Destino",
        flight_data["destination"],
        disabled=True,
        help="Se actualiza automáticamente según el vuelo seleccionado"
    )

    # El motivo de cancelación se puede cambiar manualmente
    cancellation_reason = st.selectbox(
        "Motivo de Cancelación",
        DEFAULT_CANCELLATION_REASONS,
        index=DEFAULT_CANCELLATION_REASONS.index(flight_data.get("reason", DEFAULT_CANCELLATION_REASONS[0]))
            if flight_data.get("reason") in DEFAULT_CANCELLATION_REASONS
            else 0
    )

    # Botón de reinicio/inicio de simulación
    if st.button("🚀 Iniciar simulación", use_container_width=True):
        print("\n\n" + "🔄"*40)
        print("NUEVA CONVERSACIÓN INICIADA")
        print("🔄"*40 + "\n\n")
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.divider()
    
    # VISUALIZACIÓN DEL ESTADO DEL FSM 
    st.header("📊 Estado de la Conversación")

    # Inicializar state manager si no existe
    if "state_manager" not in st.session_state:
        st.session_state.state_manager = StateManager()

    # Obtener state manager
    state_mgr = st.session_state.state_manager
    current_state = state_mgr.get_current_state()

    # Mostrar estado actual con emoji
    emoji = state_mgr.get_state_emoji(current_state)
    label = state_mgr.get_state_label(current_state)
    st.info(f"**Estado Actual:** {emoji} {label}")

    # Mostrar interrupciones (cambios de flujo)
    interruptions = state_mgr.get_interruption_count()
    if interruptions > 0:
        st.warning(f"**Cambios de decisión:** {interruptions}")

    # Progreso del flujo
    st.markdown("**Progreso del flujo:**")

    # Determinar qué flujo mostrar basándose en el estado actual
    if state_mgr.has_reached_state(ConversationState.REFUND):
        # Flujo B: Reembolso 
        refund_states = [
            ConversationState.NOTIFIED,
            ConversationState.REFUND,
            ConversationState.RESOLVED
        ]

        for state in refund_states:
            reached = state_mgr.has_reached_state(state)
            emoji_check = "✅" if reached else "⏳"
            label_state = state_mgr.get_state_label(state)
            st.markdown(f"{emoji_check} {label_state}")
    else:
        # Flujo A: Rebooking 
        rebooking_states = [
            ConversationState.NOTIFIED,
            ConversationState.REBOOKING,
            ConversationState.RESOLVED
        ]

        for state in rebooking_states:
            reached = state_mgr.has_reached_state(state)
            emoji_check = "✅" if reached else "⏳"
            label_state = state_mgr.get_state_label(state)
            st.markdown(f"{emoji_check} {label_state}")

    # Barra de progreso
    progress = state_mgr.get_progress_percentage()
    st.progress(progress / 100)
    st.caption(f"Completado: {progress}%")
    
    st.divider()
    
    # Información del modelo (solo lectura)
    with st.expander("Información del Modelo"):
        st.write(f"**Modelo:** {DEFAULT_MODEL}")
        st.write(f"**Temperatura:** {DEFAULT_TEMPERATURE}")
        st.caption("Configuración optimizada para atención al cliente")
    
    st.divider()

    # Debug opcional
    if st.checkbox("Modo Debug"):
        st.write("**Estado actual:**")
        st.write(f"Mensajes: {len(st.session_state.get('messages', []))}")
        st.write(f"Proactivo enviado: {st.session_state.get('initial_message_sent', False)}")
        
        #  Debug del state manager
        if "state_manager" in st.session_state:
            st.write("**Historial de Estados:**")
            for state, time in st.session_state.state_manager.get_state_history():
                st.write(f"- {time}: {st.session_state.state_manager.get_state_label(state)}")
    
    # Footer en el sidebar
    st.divider()
    st.caption("Challenge para Itti - Viviana Choque")

# Cachear el modelo LLM
@st.cache_resource
def get_chat_model(model: str, temp: float):
    """Crear modelo LLM con caché para evitar recreaciones"""
    return ChatOpenAI(model=model, temperature=temp, streaming=True)

chat_model = get_chat_model(DEFAULT_MODEL, DEFAULT_TEMPERATURE)

# Obtener herramientas
tools = get_flight_tools()

# Inicializar estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

if "initial_message_sent" not in st.session_state:
    st.session_state.initial_message_sent = False

#  Inicializar state manager
if "state_manager" not in st.session_state:
    st.session_state.state_manager = StateManager()

# ===== LOGGING ESCENARIO =====
if "scenario_logged" not in st.session_state:
    print("\n" + "🎬"*40)
    print("ESCENARIO CONFIGURADO:")
    print("🎬"*40)
    print(f"📝 Pasajero: {passenger_name}")
    print(f"✈️  Vuelo cancelado: {flight_number}")
    print(f"🗺️  Ruta: {origin} → {destination}")
    print(f"⚠️  Motivo: {cancellation_reason}")
    print("🎬"*40 + "\n")
    st.session_state.scenario_logged = True

# Crear mensaje del sistema con el contexto
system_message_content = get_system_message(
    passenger_name,
    flight_number,
    origin,
    destination,
    cancellation_reason
)

# AGREGAR INSTRUCCIONES DINÁMICAS BASADAS EN EL ESTADO
if "state_manager" in st.session_state:
    state_mgr = st.session_state.state_manager
    
    # Si necesita confirmación, agregar instrucciones
    if state_mgr.needs_confirmation():
        confirmation_instructions = """

## 🔒 ACCIÓN REQUERIDA: SOLICITAR CONFIRMACIÓN

El usuario acaba de tomar una decisión importante. DEBES pedir confirmación explícita ANTES de proceder.

### Formato de Confirmación Obligatorio:

"Perfecto, ha elegido [la opción]. 

⚠️ **¿Está completamente seguro de esta decisión?** 

Una vez confirmado, procesaremos inmediatamente y NO podrá hacer cambios sin comunicarse al **0800-ITTI**.

Por favor confirme con 'Sí, confirmo' o si desea reconsiderar, puede decirme 'No, quiero cambiar'."

**CRÍTICO:** NO PROCESES NADA hasta recibir confirmación explícita del usuario.
"""
        system_message_content += confirmation_instructions
    
    # Si está en estado final (100%), no permitir cambios
    if state_mgr.is_final_state():
        final_state_instructions = """

## 🚫 ESTADO FINAL ALCANZADO - NO MÁS CAMBIOS

El proceso ya fue completado al 100%. NO PUEDES realizar más cambios directamente.

Si el usuario intenta cambiar algo, responde exactamente así:

"Su [reserva/reembolso] ya ha sido procesado y confirmado exitosamente. ✅

Para realizar cualquier modificación, necesitará comunicarse con nuestro centro de atención al cliente al **0800-ITTI**.

Nuestro equipo estará encantado de ayudarle con cualquier cambio que necesite. ¿Hay algo más en lo que pueda asistirle?"

**NO ofrezcas hacer cambios tú mismo. SIEMPRE redirige al 0800-ITTI.**
"""
        system_message_content += final_state_instructions

# Actualizar o agregar mensaje del sistema al inicio
if len(st.session_state.messages) == 0:
    st.session_state.messages.insert(0, SystemMessage(content=system_message_content))
elif isinstance(st.session_state.messages[0], SystemMessage):
    # Actualizar el mensaje del sistema si los parámetros cambiaron
    st.session_state.messages[0] = SystemMessage(content=system_message_content)
else:
    st.session_state.messages.insert(0, SystemMessage(content=system_message_content))

# Crear agente con herramientas usando la nueva API de LangGraph
agent_executor = create_react_agent(
    chat_model,
    tools
)

# Mostrar mensaje proactivo inicial
if not st.session_state.initial_message_sent:
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        cancellation_notification = get_cancellation_notification(
            passenger_name,
            flight_number,
            destination,
            cancellation_reason
        )

        st.markdown(f"""
        <div class="proactive-message">
            {cancellation_notification}
        </div>
        """, unsafe_allow_html=True)

    st.session_state.messages.append(AIMessage(content=cancellation_notification))
    st.session_state.initial_message_sent = True

    # ===== LOGGING CONVERSACIÓN =====
    print("\n" + "="*80)
    print("🤖 BOT (MENSAJE PROACTIVO):")
    print("="*80)
    print(cancellation_notification)
    print("="*80 + "\n")

# Renderizar historial de messages
# Encontrar el índice del primer mensaje AI (el mensaje proactivo inicial)
first_ai_message_idx = None
for idx, msg in enumerate(st.session_state.messages):
    if isinstance(msg, AIMessage):
        first_ai_message_idx = idx
        break

# Renderizar mensajes
for idx, msg in enumerate(st.session_state.messages):
    if isinstance(msg, SystemMessage):
        continue

    # Saltar el primer mensaje AI (ya fue mostrado con estilo especial arriba)
    if idx == first_ai_message_idx:
        continue

    role = "assistant" if isinstance(msg, AIMessage) else "user"
    avatar = ASSISTANT_AVATAR if role == "assistant" else USER_AVATAR

    with st.chat_message(role, avatar=avatar):
        st.markdown(msg.content)

# Input del usuario y generación de respuesta
user_input = st.chat_input("Escriba su mensaje aquí...")

if user_input:
    # ===== LOGGING CONVERSACIÓN =====
    print("\n" + "="*80)
    print("👤 USUARIO:")
    print("="*80)
    print(user_input)
    print("="*80 + "\n")

    # Mostrar mensaje del usuario
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_input)

    st.session_state.messages.append(HumanMessage(content=user_input))

    # Generar respuesta del asistente
    try:
        with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
            with st.spinner("Procesando..."):
                # Ejecutar agente con la nueva API de LangGraph
                result = agent_executor.invoke({
                    "messages": st.session_state.messages
                })

                # Obtener la última respuesta del agente
                full_response = result["messages"][-1].content
                st.markdown(full_response)

        # ===== LOGGING CONVERSACIÓN =====
        print("="*80)
        print("🤖 BOT:")
        print("="*80)
        print(full_response)
        print("="*80 + "\n")

        st.session_state.messages.append(AIMessage(content=full_response))

        #  ACTUALIZAR ESTADO DEL FSM
        previous_state = st.session_state.state_manager.current_state
        st.session_state.state_manager.update_state(
            user_message=user_input,
            agent_response=full_response
        )
        new_state = st.session_state.state_manager.current_state

        # ===== LOGGING ESTADO FSM =====
        if previous_state != new_state:
            print("📊 CAMBIO DE ESTADO FSM:")
            print(f"   {previous_state.value} → {new_state.value}")
            print(f"   Progreso: {st.session_state.state_manager.get_progress_percentage()}%")
            print()
        
        #  Forzar rerun para actualizar el sidebar
        st.rerun()
        
    except Exception as e:
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("**Posibles soluciones:**")
        st.write("1. Verifica que tu `OPENAI_API_KEY` esté configurada en el archivo .env")
        st.write("2. Asegúrate de tener créditos en tu cuenta de OpenAI")
        st.write("3. Verifica tu conexión a internet")