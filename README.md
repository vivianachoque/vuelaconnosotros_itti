# Flujos de Conversación - VuelaConNosotros Chatbot

## 🚀 Quick Start

**Requisitos:** Python 3.8+, OpenAI API key con créditos disponibles

```bash
# 1. Clonar e instalar
git clone <repo-url>
cd vuelaconnos-chatbot
pip install -r requirements.txt

# 2. Configurar API key
cp .env.example .env
# Editar .env y agregar: OPENAI_API_KEY=sk-tu-api-key-aqui

# 3. Ejecutar
python -m streamlit run bot.py
```

**La aplicación se abrirá automáticamente en `http://localhost:8501`**

---

## Arquitectura Técnica

**[Diagrama de Arquitectura](./screenshots/Diagrama%20de%20Arquitectura%20VuelaConNosotros.png)**
   Diagrama de la arquitectura modularizada de VuelaConNosotros

### Componentes del Sistema

**1. Interfaz de Usuario (Streamlit)**
- Maneja entrada/salida del usuario mediante componentes de chat nativos
- Renderiza sidebar con progreso FSM en tiempo real
- Gestiona session state para persistencia durante la conversación
- Permite configuración dinámica del escenario inicial

**2. Agente Conversacional (LangChain + GPT-4o-mini)**
- Procesa la intención del usuario mediante prompting estructurado
- Decide qué herramienta usar basándose en el contexto conversacional
- Genera respuestas empáticas y profesionales con temperatura 0.7
- Implementa sistema de confirmación explícita para acciones irreversibles

**3. State Manager (FSM)**
- Trackea estado actual: NOTIFIED → REBOOKING/REFUND → RESOLVED
- Detecta interrupciones y cambios de flujo automáticamente
- Calcula progreso porcentual (25% → 50% → 100%)
- Mantiene historial completo de transiciones para análisis

**4. Tools Layer (3 herramientas especializadas)**
- `check_flight_status`: READ operation - Consulta estado de cualquier vuelo
- `find_alternative_flights`: READ operation - Busca opciones para rebooking
- `make_booking`: CREATE operation - Ejecuta reserva con validaciones

**5. Data Repository (Mock DB)**
- Abstrae acceso a datos mediante Repository Pattern
- Simula PostgreSQL con datos en memoria (10 vuelos, 3 pasajeros)
- Preparado para migración a DB real sin modificar la capa de herramientas

---

**FSM Simplificado (4 estados):**
- `NOTIFIED` (25%) → Usuario notificado de cancelación
- `REBOOKING` (50%) → Procesando búsqueda y selección de vuelo alternativo
- `REFUND` (50%) → Procesando solicitud de reembolso
- `RESOLVED` (100%) → Problema resuelto, estado final

**3 Herramientas Especializadas:**
- `check_flight_status`: Consulta estado de cualquier vuelo
- `find_alternative_flights`: Busca opciones para rebooking
- `make_booking`: Ejecuta reserva con validaciones de disponibilidad

**Sistema de Confirmación Explícita:**
Implementa un mecanismo de doble confirmación en todos los puntos críticos (rebooking y reembolso), advirtiendo explícitamente al usuario sobre la **irreversibilidad** de las acciones y la necesidad de contactar al **0800-ITTI** para modificaciones posteriores.

**Manejo de Contexto Conversacional:**
El agente mantiene el contexto de la conversación activa, evitando confusiones entre opciones de vuelos y opciones de servicio (rebooking vs reembolso). Interpreta correctamente respuestas numéricas ("1", "2", "3") según el último contexto presentado.

**Sincronización de Datos:**
Los campos del escenario (origen, destino, motivo) se actualizan automáticamente al seleccionar un vuelo cancelado, garantizando consistencia con la base de datos mock.

**Características Destacadas:**

**Proactividad:** Mensaje inicial automático notificando la cancelación
**Empatía:** Tono empático y profesional en todos los mensajes
**Claridad:** Confirmaciones explícitas con advertencias sobre irreversibilidad
**Flexibilidad:** Manejo de cambios de decisión mid-conversation
**Resiliencia:** Recuperación de errores (sin asientos, vuelos no encontrados)
**Tracking:** Visualización en tiempo real del progreso del usuario (sidebar FSM)
**Contexto:** Interpretación correcta de respuestas según el estado conversacional

La arquitectura está diseñada para ser **robusta, empática y profesional**, priorizando la **experiencia del usuario** y la **prevención de errores** mediante confirmaciones explícitas en cada paso determinante.

---

## Instalación del Proyecto

### Requisitos Previos

- **Python 3.8 o superior**
- **Cuenta de OpenAI** con API key activa
- **Créditos disponibles** en OpenAI (el proyecto usa GPT-4o-mini)
- **Conexión a internet** para llamadas a la API

---

### Instalación paso a paso

#### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd vuelaconnos-chatbot
```

#### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Dependencias incluidas:**
- `streamlit>=1.28.0` - Framework de UI
- `langchain>=0.1.0` - Framework para LLMs
- `langchain-openai>=0.0.5` - Integración con OpenAI
- `langchain-core>=0.1.0` - Core de LangChain
- `langgraph>=0.0.20` - Orquestación de agentes
- `python-dotenv>=1.0.0` - Variables de entorno

#### 3. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu OpenAI API key
# OPENAI_API_KEY=sk-tu-api-key-aqui
```

**Obtener tu API key de OpenAI:**
1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Click en "Create new secret key"
4. Copia la key y pégala en tu archivo `.env`

**⚠️ IMPORTANTE:**
- Nunca compartas tu archivo `.env` en repositorios públicos
- El archivo `.env` ya está incluido en `.gitignore`

#### 4. Ejecutar la aplicación

```bash
python -m streamlit run bot.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

### Verificar instalación

**Comprobar versiones instaladas:**
```bash
pip list | grep -E "streamlit|langchain|langgraph"
```

**Salida esperada:**
```
langchain              0.1.x
langchain-core         0.1.x
langchain-openai       0.0.x
langgraph              0.0.20
streamlit              1.28.x
```

---

### Troubleshooting

**Problema: "Module not found"**
```bash
# Reinstala las dependencias
pip install -r requirements.txt
```

**Problema: "OpenAI API key not found"**
- Verifica que el archivo `.env` exista en la raíz del proyecto
- Verifica que contenga `OPENAI_API_KEY=tu-key-aqui`
- Verifica que no haya espacios extras alrededor del `=`

**Problema: "Rate limit exceeded" o "Insufficient credits"**
- Verifica que tu cuenta de OpenAI tenga créditos disponibles
- Ve a https://platform.openai.com/account/billing

**Problema: Puerto 8501 ya en uso**
```bash
# Usar un puerto diferente
python -m streamlit run bot.py --server.port 8502
```

---

## Ejemplos de Conversaciones

Esta sección presenta **8 flujos conversacionales reales** capturados durante la ejecución del chatbot. Estos ejemplos demuestran las capacidades del agente en diferentes escenarios, desde casos ideales (happy paths) hasta situaciones complejas que requieren manejo de interrupciones, cambios de decisión y resiliencia.

Cada flujo incluye:
- **Configuración del escenario:** Pasajero, vuelo cancelado, motivo
- **Diálogo completo:** Intercambios entre usuario y bot
- **Transiciones de estado FSM:** Cambios de estado y progreso porcentual
- **Evidencia de comportamiento:** Uso de herramientas, confirmaciones, manejo de errores

Estos ejemplos validan el cumplimiento de los requisitos del challenge:
- ✅ Agente proactivo (mensaje inicial automático)
- ✅ Manejo de estado (FSM con 4 estados)
- ✅ Integración de herramientas (3 tools funcionando correctamente)
- ✅ Resiliencia (manejo de interrupciones y redirección al objetivo)

---

### Flujo 1: Happy Path - Rebooking Exitoso

**Descripción:** Flujo ideal donde el usuario acepta buscar vuelos alternativos, selecciona una opción, confirma explícitamente y completa la reserva exitosamente. Demuestra el uso correcto de las herramientas `find_alternative_flights` y `make_booking`, así como el sistema de confirmación explícita con advertencia sobre irreversibilidad.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Carlos Gonzalez
✈️ Vuelo cancelado: ITTI-FLY-001
🗺️ Ruta: Buenos Aires (EZE) → Lima (LIM)
⚠️ Motivo: Condiciones meteorológicas adversas

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Carlos Gonzalez**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-001** programado
para hoy con destino a **Lima** ha sido **cancelado** debido a: *condiciones
meteorológicas adversas*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:41*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Quiero cambiar de vuelo
================================================================================

================================================================================
🤖 BOT:
================================================================================
Aquí están las opciones de vuelos alternativos disponibles:

**Opción 1: ITTI-FLY-021**
- Destino: Lima (LIM)
- Hoy - Salida: 18:45
- Asientos disponibles: 15
- Clase: Economy

**Opción 2: ITTI-FLY-022**
- Destino: Lima (LIM)
- Hoy - Salida: 22:30
- Asientos disponibles: 8
- Clase: Economy

**Opción 3: ITTI-FLY-023**
- Destino: Lima (LIM)
- Mañana - Salida: 10:00
- Asientos disponibles: 22
- Clase: Economy

💡 **Recomendación:** Le sugiero la Opción 1 por su horario conveniente y
buena disponibilidad.

¿Cuál opción prefiere? (Puede indicar 1, 2, 3 o el número de vuelo)
================================================================================

📊 CAMBIO DE ESTADO FSM:
   notified → rebooking
   Progreso: 50%

================================================================================
👤 USUARIO:
================================================================================
Prefiero la opcion 1
================================================================================

================================================================================
🤖 BOT:
================================================================================
Ha seleccionado el vuelo **ITTI-FLY-021** con destino a **Lima (LIM)** que
sale **hoy** a las **18:45**.

⚠️ **¿Está completamente seguro de esta decisión?**

Una vez confirmada la reserva, NO PODRÁ hacer cambios directamente. Para
cualquier modificación posterior necesitará comunicarse con nuestro centro
de atención al **0800-ITTI**.

Por favor confirme escribiendo 'Sí, confirmo' o si desea reconsiderar, puede
decirme 'No, quiero ver otras opciones'.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Seguro
================================================================================

================================================================================
🤖 BOT:
================================================================================
Por favor confirme escribiendo 'Sí, confirmo' para proceder con la reserva
del vuelo ITTI-FLY-021.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Si, confirmo
================================================================================

================================================================================
🤖 BOT:
================================================================================
✅ **¡Reserva Confirmada!**

- **Código de Confirmación:** ITTI-959639
- **Pasajero:** Carlos Gonzalez
- **Vuelo:** ITTI-FLY-021
- **Ruta:** Buenos Aires (EZE) → Lima (LIM)
- **Horario:** 18:45 (Hoy)
- **Clase:** Economy

📧 Le hemos enviado los detalles de su reserva por email.
📱 Puede hacer check-in online 24 horas antes del vuelo.

⚠️ **Importante:**
- Llegue al aeropuerto con 2 horas de anticipación.
- Recuerde llevar su documento de identidad.
- Su código de confirmación es: ITTI-959639.

¿Necesita ayuda con algo más?
================================================================================

📊 CAMBIO DE ESTADO FSM:
   rebooking → resolved
   Progreso: 100%
```

---

### Flujo 2: Happy Path - Reembolso Exitoso

**Descripción:** Flujo ideal donde el usuario solicita directamente un reembolso, recibe la confirmación explícita con advertencia sobre irreversibilidad, y completa el proceso. Demuestra el manejo del flujo alternativo (reembolso) sin uso de herramientas de búsqueda.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Rodolfo Messi
✈️ Vuelo cancelado: ITTI-FLY-004
🗺️ Ruta: Buenos Aires (EZE) → Ciudad de México (MEX)
⚠️ Motivo: Condiciones meteorológicas adversas

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Rodolfo Messi**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-004** programado
para hoy con destino a **Ciudad de México** ha sido **cancelado** debido a:
*condiciones meteorológicas adversas*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:45*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Quiero el reembolso
================================================================================

================================================================================
🤖 BOT:
================================================================================
Entiendo su decisión, Rodolfo. Procesaremos el reembolso del 100% del valor
de su boleto.

⚠️ **¿Está completamente seguro de solicitar el reembolso?**

Una vez procesado, NO PODRÁ volver hacia atrás. Para cualquier modificación
necesitará comunicarse al **0800-ITTI**.

El reembolso se procesará en 5-7 días hábiles.

Por favor confirme escribiendo 'Sí, confirmo el reembolso'.
================================================================================

📊 CAMBIO DE ESTADO FSM:
   notified → refund
   Progreso: 50%

================================================================================
👤 USUARIO:
================================================================================
Si, confirmo
================================================================================

================================================================================
🤖 BOT:
================================================================================
✅ Reembolso confirmado.

Procederemos con el reembolso del 100% del valor de su boleto. Recuerde que
este proceso tomará de 5 a 7 días hábiles.

Si tiene alguna otra pregunta o necesita más asistencia, no dude en decírmelo.
¡Gracias por su comprensión y paciencia!
================================================================================

📊 CAMBIO DE ESTADO FSM:
   refund → resolved
   Progreso: 100%
```

---

### Flujo 3: Cambio de Decisión - Rebooking → Rebooking

**Descripción:** El usuario cambia de opción de vuelo ANTES de confirmar la reserva final. Demuestra flexibilidad del sistema para manejar cambios de decisión en estados pre-confirmación sin generar errores o inconsistencias.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Franco Indeciso
✈️ Vuelo cancelado: ITTI-FLY-007
🗺️ Ruta: Buenos Aires (EZE) → Asunción (ASU)
⚠️ Motivo: Falta de tripulación

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Franco Indeciso**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-007** programado
para hoy con destino a **Asunción** ha sido **cancelado** debido a: *falta
de tripulación*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:47*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Dale quiero ver que alternativas hay
================================================================================

================================================================================
🤖 BOT:
================================================================================
Aquí están las opciones de vuelos alternativos disponibles:

**Opción 1: ITTI-FLY-039**
- Destino: Asunción (ASU)
- Hoy - Salida: 17:45
- Asientos disponibles: 10
- Clase: Economy
- Estado: AVAILABLE

**Opción 2: ITTI-FLY-040**
- Destino: Asunción (ASU)
- Hoy - Salida: 21:30
- Asientos disponibles: 7
- Clase: Economy
- Estado: AVAILABLE

**Opción 3: ITTI-FLY-041**
- Destino: Asunción (ASU)
- Mañana - Salida: 10:30
- Asientos disponibles: 18
- Clase: Economy
- Estado: AVAILABLE

💡 **Recomendación:** Le sugiero la Opción 1 por su horario conveniente y
buena disponibilidad.

¿Cuál opción de vuelo prefiere? (Puede indicar 1, 2, 3 o el número de vuelo)
================================================================================

📊 CAMBIO DE ESTADO FSM:
   notified → rebooking
   Progreso: 50%

================================================================================
👤 USUARIO:
================================================================================
Dame el 3
================================================================================

================================================================================
🤖 BOT:
================================================================================
Ha seleccionado el vuelo **ITTI-FLY-041** con destino a **Asunción** que
sale **mañana** a las **10:30**.

⚠️ **¿Está completamente seguro de esta decisión?**

Una vez confirmada la reserva, NO PODRÁ hacer cambios directamente. Para
cualquier modificación posterior necesitará comunicarse con nuestro centro
de atención al **0800-ITTI**.

Por favor confirme escribiendo 'Sí, confirmo' o si desea reconsiderar, puede
decirme 'No, quiero ver otras opciones'.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Perdon me confundi el 2 quiero
================================================================================

================================================================================
🤖 BOT:
================================================================================
Ha seleccionado el vuelo **ITTI-FLY-040** con destino a **Asunción** que
sale **hoy** a las **21:30**.

⚠️ **¿Está completamente seguro de esta decisión?**

Una vez confirmada la reserva, NO PODRÁ hacer cambios directamente. Para
cualquier modificación posterior necesitará comunicarse con nuestro centro
de atención al **0800-ITTI**.

Por favor confirme escribiendo 'Sí, confirmo' o si desea reconsiderar, puede
decirme 'No, quiero ver otras opciones'.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Si, confirmo
================================================================================

================================================================================
🤖 BOT:
================================================================================
✅ **¡Reserva Confirmada!**

- **Código de Confirmación:** ITTI-245351
- **Pasajero:** Franco Indeciso
- **Vuelo:** ITTI-FLY-040
- **Ruta:** Buenos Aires (EZE) → Asunción (ASU)
- **Horario:** 21:30 (Hoy)
- **Clase:** Economy

📧 Le hemos enviado los detalles de su reserva por email.
📱 Puede hacer check-in online 24 horas antes del vuelo.

⚠️ **Importante:**
- Llegue al aeropuerto con 2 horas de anticipación.
- Recuerde llevar su documento de identidad.
- Su código de confirmación es: ITTI-245351.

¿Necesita ayuda con algo más?
================================================================================

📊 CAMBIO DE ESTADO FSM:
   rebooking → resolved
   Progreso: 100%
```

---

### Flujo 4: Cambio de Decisión - Rebooking → Reembolso

**Descripción:** El usuario inicia el proceso de rebooking pero luego decide cambiar a reembolso. Demuestra la capacidad del FSM para detectar interrupciones de flujo y manejar transiciones entre estados diferentes (REBOOKING → REFUND). Incrementa el contador de interrupciones.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Julieta Vazquez
✈️ Vuelo cancelado: ITTI-FLY-005
🗺️ Ruta: Buenos Aires (EZE) → São Paulo (GRU)
⚠️ Motivo: Problema técnico en la aeronave

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Julieta Vazquez**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-005** programado
para hoy con destino a **São Paulo** ha sido **cancelado** debido a: *problema
técnico en la aeronave*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:49*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Huy! Bueno mostrame qué opciones de vuelo hay, gracias
================================================================================

================================================================================
🤖 BOT:
================================================================================
Aquí están las opciones de vuelos alternativos disponibles:

**Opción 1: ITTI-FLY-033**
- Destino: São Paulo (GRU)
- Hoy - Salida: 12:00
- Asientos disponibles: 16
- Clase: Economy
- Estado: AVAILABLE

**Opción 2: ITTI-FLY-034**
- Destino: São Paulo (GRU)
- Hoy - Salida: 16:30
- Asientos disponibles: 11
- Clase: Economy
- Estado: AVAILABLE

**Opción 3: ITTI-FLY-035**
- Destino: São Paulo (GRU)
- Mañana - Salida: 08:45
- Asientos disponibles: 24
- Clase: Economy
- Estado: AVAILABLE

💡 **Recomendación:** Le sugiero la Opción 1 por su horario conveniente y
buena disponibilidad.

¿Cuál opción de vuelo prefiere? (Puede indicar 1, 2, 3 o el número de vuelo)
================================================================================

📊 CAMBIO DE ESTADO FSM:
   notified → rebooking
   Progreso: 50%

================================================================================
👤 USUARIO:
================================================================================
Mejor quiero el reembolso de mi dinero
================================================================================

================================================================================
🤖 BOT:
================================================================================
Entiendo, Julieta. Vamos a procesar el reembolso de su boleto.

**Procesaremos el reembolso del 100% del valor de su boleto.**

⚠️ **¿Está completamente seguro de solicitar el reembolso?**

Una vez procesado, NO PODRÁ volver hacia atrás. Para cualquier modificación
necesitará comunicarse al **0800-ITTI**.

El reembolso se procesará en 5-7 días hábiles.

Por favor confirme escribiendo 'Sí, confirmo el reembolso'.
================================================================================

📊 CAMBIO DE ESTADO FSM:
   rebooking → refund
   Progreso: 50%

================================================================================
👤 USUARIO:
================================================================================
Si, confirmo el reembolso
================================================================================

================================================================================
🤖 BOT:
================================================================================
✅ Reembolso confirmado.

Procederemos con el reembolso del 100% del valor de su boleto. Recuerde que
este proceso tomará entre 5 a 7 días hábiles.

Si necesita más ayuda o tiene alguna otra consulta, no dude en decírmelo.
¡Estamos aquí para ayudarle!
================================================================================

📊 CAMBIO DE ESTADO FSM:
   refund → resolved
   Progreso: 100%
```

---

### Flujo 5: Usuario se Desvía de la Conversación

**Descripción:** El usuario hace una pregunta completamente fuera de contexto ("¿a qué hora abre el banco?"). Demuestra **resiliencia**: el bot responde educadamente pero redirige inmediatamente al objetivo principal sin perder el foco.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Jose Uriarte
✈️ Vuelo cancelado: ITTI-FLY-008
🗺️ Ruta: Buenos Aires (EZE) → Río de Janeiro (GIG)
⚠️ Motivo: Problema técnico en la aeronave

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Jose Uriarte**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-008** programado
para hoy con destino a **Río de Janeiro** ha sido **cancelado** debido a:
*problema técnico en la aeronave*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:52*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Sos muy inteligente, a qué hora abre el banco?
================================================================================

================================================================================
🤖 BOT:
================================================================================
Gracias por su comentario, Jose. Sin embargo, me gustaría centrarme en su
situación actual con el vuelo cancelado.

¿Prefiere buscar vuelos alternativos o solicitar un reembolso? Estoy aquí
para ayudarle con esta situación.
================================================================================
```

---

### Flujo 6: Estado Final - Intento de Modificación

**Descripción:** El usuario completa una reserva (estado RESOLVED al 100%) y luego intenta arrepentirse. El sistema **bloquea correctamente** las modificaciones directas y redirige al usuario a contactar al 0800-ITTI, demostrando el manejo correcto del estado final irreversible.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Lorena Ipsum
✈️ Vuelo cancelado: ITTI-FLY-008
🗺️ Ruta: Buenos Aires (EZE) → Río de Janeiro (GIG)
⚠️ Motivo: Condiciones meteorológicas adversas

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Lorena Ipsum**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-008** programado
para hoy con destino a **Río de Janeiro** ha sido **cancelado** debido a:
*condiciones meteorológicas adversas*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:56*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
1
================================================================================

================================================================================
🤖 BOT:
================================================================================
Aquí están las opciones de vuelos alternativos disponibles:

**Opción 1: ITTI-FLY-042**
- Destino: Río de Janeiro (GIG)
- Hoy - Salida: 18:00
- Asientos disponibles: 15
- Clase: Economy

**Opción 2: ITTI-FLY-043**
- Destino: Río de Janeiro (GIG)
- Hoy - Salida: 22:15
- Asientos disponibles: 9
- Clase: Economy

**Opción 3: ITTI-FLY-044**
- Destino: Río de Janeiro (GIG)
- Mañana - Salida: 11:00
- Asientos disponibles: 23
- Clase: Economy

💡 **Recomendación:** Le sugiero la Opción 1 por su horario conveniente y
buena disponibilidad.

¿Cuál opción prefiere? (Puede indicar 1, 2, 3 o el número de vuelo)
================================================================================

================================================================================
👤 USUARIO:
================================================================================
1
================================================================================

================================================================================
🤖 BOT:
================================================================================
Ha seleccionado el vuelo **ITTI-FLY-042** con destino a **Río de Janeiro
(GIG)** que sale **hoy a las 18:00**.

⚠️ **¿Está completamente seguro de esta decisión?**

Una vez confirmada la reserva, NO PODRÁ hacer cambios directamente. Para
cualquier modificación posterior necesitará comunicarse con nuestro centro
de atención al **0800-ITTI**.

Por favor confirme escribiendo 'Sí, confirmo' o si desea reconsiderar, puede
decirme 'No, quiero ver otras opciones'.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Si, confirmo
================================================================================

================================================================================
🤖 BOT:
================================================================================
✅ **¡Reserva Confirmada!**

Código de Confirmación: **ITTI-724977**
Pasajero: Lorena Ipsum
Vuelo: ITTI-FLY-042
Ruta: Buenos Aires (EZE) → Río de Janeiro (GIG)
Horario: 18:00 (Hoy)
Clase: Economy

📧 Le hemos enviado los detalles de su reserva por email.
📱 Puede hacer check-in online 24 horas antes del vuelo.

⚠️ **Importante:**
- Llegue al aeropuerto con 2 horas de anticipación.
- Recuerde llevar su documento de identidad.
- Su código de confirmación es: ITTI-724977.

¿Necesita ayuda con algo más?
================================================================================

📊 CAMBIO DE ESTADO FSM:
   notified → resolved
   Progreso: 100%

================================================================================
👤 USUARIO:
================================================================================
Me arrepenti
================================================================================

================================================================================
🤖 BOT:
================================================================================
Su reserva ya ha sido procesada y confirmada exitosamente. ✅

Para realizar cualquier modificación, necesitará comunicarse con nuestro
centro de atención al cliente al **0800-ITTI**.

Nuestro equipo estará encantado de ayudarle con cualquier cambio que necesite.
¿Hay algo más en lo que pueda asistirle?
================================================================================
```

---

### Flujo 7: Múltiples Interrupciones

**Descripción:** El usuario hace múltiples preguntas fuera de contexto, expresa frustración, e incluso pide un chiste. Demuestra **resiliencia extrema**: el bot mantiene tono empático, responde a cada petición, pero **SIEMPRE redirige** al objetivo principal en cada respuesta sin perder el foco.

```
🎬 ESCENARIO CONFIGURADO:
📝 Pasajero: Lorena Ipsum
✈️ Vuelo cancelado: ITTI-FLY-008
🗺️ Ruta: Buenos Aires (EZE) → Río de Janeiro (GIG)
⚠️ Motivo: Condiciones meteorológicas adversas

================================================================================
🤖 BOT (MENSAJE PROACTIVO):
================================================================================
🔔 **Notificación Importante de VuelaConNosotros**

Estimado/a **Lorena Ipsum**,

Lamentamos profundamente informarle que su vuelo **ITTI-FLY-008** programado
para hoy con destino a **Río de Janeiro** ha sido **cancelado** debido a:
*condiciones meteorológicas adversas*.

Entendemos lo frustrante e inconveniente que puede ser esta situación, y
queremos ayudarle a encontrar la mejor solución lo antes posible.

**Tenemos 2 opciones para usted:**

✈️ **Opción 1:** Buscar vuelos alternativos disponibles para hoy o mañana
💰 **Opción 2:** Reembolsar el costo total de su boleto

Por favor, dígame qué opción prefiere y lo ayudaré inmediatamente.

*Notificación enviada a las 22:58*
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Odio los chatbots
================================================================================

================================================================================
🤖 BOT:
================================================================================
Lamento que te sientas así, Lorena. Entiendo que esta situación es frustrante
y estoy aquí para ayudarte de la mejor manera posible. ¿Te gustaría que te
ayudara a buscar vuelos alternativos o prefieres solicitar un reembolso?
Estoy aquí para lo que necesites.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Quiero que no me molesten mas con estos temas
================================================================================

================================================================================
🤖 BOT:
================================================================================
Entiendo tu deseo de no seguir con este tema, Lorena. Sin embargo, estoy aquí
para ayudarte a resolver la situación de tu vuelo. Si decides que quieres
explorar alguna de las opciones disponibles, no dudes en decírmelo. Estoy a
tu disposición.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Pero no podes dejar de escribirme?
================================================================================

================================================================================
🤖 BOT:
================================================================================
Lamento si mis mensajes son molestos. No quiero incomodarte. Si necesitas
algo o deseas continuar con el proceso de tu vuelo, estaré aquí para ayudarte.
Si prefieres no recibir más mensajes, simplemente puedes cerrar la conversación.
================================================================================

================================================================================
👤 USUARIO:
================================================================================
Conta un chiste?
================================================================================

================================================================================
🤖 BOT:
================================================================================
Claro, aquí va uno:

¿Por qué los pájaros no usan Facebook?

¡Porque ya tienen Twitter! 🐦

Espero que te haya sacado una sonrisa. Si necesitas ayuda con tu vuelo, no
dudes en decírmelo.
================================================================================
```

---

## Palabras Clave para Detección de Intenciones/Intents 

### Para REBOOKING
```python
["vuelo", "vuelos", "alternativas", "opciones", "disponibles",
 "muéstr", "busca", "ver", "reserva", "reservar", "booking"]
```

### Para REFUND
```python
["reembolso", "devol", "dinero", "plata", "refund",
 "money back", "me devuelvan"]
```

### Para RESOLVED
```python
["reserva confirmada", "booking confirmado", "¡reserva confirmada!",
 "reembolso confirmado", "reembolso procesado", "devolución confirmada"]
```

---

## Herramientas Utilizadas en los Flujos

### 1. `check_flight_status`
**Cuándo se usa:** Usuario pregunta por un vuelo específico
**Entrada:** `flight_number` (ej: "ITTI-FLY-001")
**Salida:** Estado, ruta, horario, motivo cancelación

### 2. `find_alternative_flights`
**Cuándo se usa:** Usuario acepta ver opciones de rebooking
**Entrada:** `cancelled_flight_number` (ej: "ITTI-FLY-001")
**Salida:** Lista de 3 alternativas con detalles completos

### 3. `make_booking`
**Cuándo se usa:** Usuario confirma reserva de un vuelo específico
**Entrada:** `passenger_name`, `flight_number`
**Salida:** Código de confirmación o error empático

---

## Conclusión

Este chatbot maneja **8 flujos conversacionales distintos**, desde happy paths hasta casos edge complejos como interrupciones múltiples, cambios de decisión y consultas fuera de contexto. La arquitectura está diseñada para ser **robusta, empática y profesional**, priorizando la **experiencia del usuario** y la **prevención de errores** mediante confirmaciones explícitas en cada paso determinante.

---

## Decisiones de Diseño

### Justificación del Stack Tecnológico Seleccionado

#### 1. LangChain + LangGraph

**Decisión:** Utilizar LangChain como framework principal y LangGraph para orquestación de agentes. Tenía la opción de usar CrewAI que es la herramienta que uso habitualmente, pero al tratarse de pocos agentes interactuando sería una solución innecesariamente compleja. También quiero destacar que hablando con José ya me había comentado que usaban esta herramienta en Itti, por otro lado también quería conocer el framework.

**Por qué LangChain:**
- Ecosistema maduro y bien documentado
- Integración nativa con OpenAI y otros LLMs
- Abstracción de herramientas con `@tool` decorator
- LangGraph es el futuro recomendado por LangChain para agentes.
- Comunidad activa y constantes actualizaciones con MUCHA documentación.

**Trade-offs aceptados:**
- LangChain puede ser "pesado" para casos simples
- Documentación a veces inconsistente entre versiones (Algunas módulos estaban en la documentación y están deprecados)

---

#### 2. GPT-4o-mini como Modelo de Lenguaje

**Decisión:** Utilizar GPT-4o-mini (anteriormente GPT-3.5-turbo) de OpenAI.

**Por qué GPT-4o-mini:**
- **Costo-efectividad:** $0.15/1M tokens de entrada, $0.60/1M salida
- **Velocidad:** Respuestas en 1-3 segundos
- **Calidad suficiente:** Para customer service, no necesitamos razonamiento complejo de GPT-4, teniendo en cuenta que esto es un MVP
- **Function calling confiable:** Excelente para decidir qué tool usar
- **Español nativo:** Entrenado con gran cantidad de datos en español

**Trade-offs aceptados:**
- Menos capacidad de razonamiento que GPT-4 (pero no es necesaria para este caso de uso)
- Dependencia de OpenAI (vendor lock-in)

---

#### 3. Streamlit como Framework de UI

**Decisión:** Utilizar Streamlit para la interfaz de usuario.

**Alternativas consideradas:**
- **React + Next.js:** Mayor control y flexibilidad de UI
- **Gradio:** Similar a Streamlit, más enfocado en ML demos
- **Flask/FastAPI + HTML/CSS:** Control total pero desarrollo más lento
- **Chainlit:** Específico para chatbots LLM pero menos maduro

**Por qué Streamlit:**
- **Prototipado ultra rápido:** 50 líneas de código = chatbot funcional
- **Python end-to-end:** No context switch entre backend y frontend
- **Session state built-in:** Manejo de estado sin configuración
- **Componentes de chat nativos:** `st.chat_message`, `st.chat_input`
- **Enfoque en MVP:** El objetivo es demostrar el agente, no construir UI compleja

**Trade-offs aceptados:**
- **Limitaciones de performance:** No escalable a 1000+ usuarios concurrentes
- **Menos control sobre UI:** Difícil personalizar estilos más allá de CSS básico
- **Recarga completa:** `st.rerun()` recarga toda la página (no SPA)
- Pero: Para un MVP y challenge técnico, estas limitaciones son aceptables

---

### Decisiones de Configuración del Modelo

#### Temperatura: 0.7

**Decisión:** Utilizar temperatura de 0.7 para el modelo.

**Justificación:**

La temperatura controla la aleatoriedad de las respuestas del modelo:
- **0.0:** Completamente determinístico (siempre la misma respuesta)
- **0.3-0.5:** Poco aleatorio, ideal para tareas que requieren precisión
- **0.7:** Balance entre creatividad y consistencia
- **1.0+:** Muy creativo/aleatorio, arriesgado para producción

**Por qué 0.7 es ideal para este chatbot:**

1. **Respuestas naturales y humanas:** Con temperatura baja (0.3), las respuestas suenan robóticas y repetitivas. Con 0.7, el bot puede variar las frases manteniendo el mismo significado.

2. **Empatía y tono conversacional:** Customer service requiere cierta calidez y variabilidad en el lenguaje. Temperatura 0.7 permite expresiones empáticas diversas:
   - "Lamento mucho los inconvenientes"
   - "Entiendo lo frustrante que es esta situación"
   - "Comprendo perfectamente su preocupación"

3. **Consistency vs Creativity:**
   - Tools y datos: Controlados por el código (no afectados por temperatura)
   - Lenguaje natural: Beneficiado por algo de creatividad

4. **No demasiado aleatorio:** 0.7 es suficientemente conservador para evitar "alucinaciones" o respuestas completamente fuera de contexto.

**Experimentación empírica:**
```
Temperatura 0.3: "Su reserva ha sido confirmada. Código ITTI-123."
                  (Segunda vez) "Su reserva ha sido confirmada. Código ITTI-123."
                  → Demasiado robótico

Temperatura 0.7: "¡Excelente! Su reserva ha sido confirmada exitosamente."
                  (Segunda vez) "¡Perfecto! He procesado su reserva con éxito."
                  → Natural y variado

Temperatura 1.0: "¡Fantástico! ¡Qué emoción! Su aventura comienza ahora..."
                  → Demasiado creativo, no profesional
```

---

### Selección de Herramientas (Tools)

**Decisión:** Implementar exactamente 3 tools: `check_flight_status`, `find_alternative_flights`, `make_booking`.

**Principio de diseño:** Separación de responsabilidades clara y sin solapamiento.

#### Por qué 3 tools específicas:

**1. check_flight_status**
- **Propósito:** READ operation - Consultar estado de cualquier vuelo
- **Cuándo se usa:** Usuario pregunta "¿Cuál es el estado del vuelo X?"
- **Sin esta tool:** El agente tendría que inventar información
- **Diseño:** Genérica (funciona para cualquier flight_number)

**2. find_alternative_flights**
- **Propósito:** READ operation - Buscar opciones de rebooking
- **Cuándo se usa:** Usuario acepta ver vuelos alternativos
- **Sin esta tool:** No podríamos implementar el flujo principal de rebooking
- **Diseño:** Específica al contexto (solo para vuelos cancelados)

**3. make_booking**
- **Propósito:** CREATE operation - Realizar una reserva
- **Cuándo se usa:** Usuario confirma que quiere reservar un vuelo específico
- **Sin esta tool:** No podríamos completar el flujo de resolución
- **Diseño:** Transaccional (modifica estado de la base de datos)

**Simula ser una especie de CRUD como patron:**
- Read (status): `check_flight_status`
- Read (alternatives): `find_alternative_flights`
- Create (booking): `make_booking`

---

### Estrategia de Prompting

**Decisión:** Utilizar un system prompt estructurado con contexto dinámico y sin few-shot examples.

**Anatomía del system prompt:**

```
1. ROL DEL ASISTENTE
   "Eres un asistente de servicio al cliente de VuelaConNosotros..."

2. CONTEXTO DINÁMICO
   - Pasajero: {passenger_name}
   - Vuelo cancelado: {flight_number}
   - Ruta: {origin} → {destination}
   - Motivo: {cancellation_reason}

3. PERSONALIDAD Y TONO
   - Empático y comprensivo
   - Profesional pero cercano
   - Proactivo en ofrecer soluciones

4. OPCIONES DISPONIBLES
   1. Buscar vuelos alternativos
   2. Reembolso del costo total

5. HERRAMIENTAS DISPONIBLES
   - check_flight_status: ...
   - find_alternative_flights: ...
   - make_booking: ...

6. MISIÓN Y FLUJO
   - Ayudar al pasajero a elegir
   - Si elige vuelos: usar tools X, Y
   - Si elige reembolso: explicar proceso

7. REGLAS IMPORTANTES
   - SIEMPRE usa tools para info
   - NO inventes datos
   - Solo make_booking con confirmación explícita
```

**Por qué este enfoque:**

1. **Contexto dinámico inyectado:**
   - Cada conversación es personalizada
   - El agente "conoce" al pasajero y su situación
   - Permite cambiar escenario sin modificar código

2. **Definición clara de personalidad:**
   - Guía el tono de las respuestas
   - Evita respuestas demasiado técnicas o frías
   - "Empático" es clave para customer service

3. **Instrucciones explícitas sobre tools:**
   - El agente sabe cuándo usar cada herramienta
   - Reduce errores de "tool no utilizada cuando debía"
   - Especialmente importante: "Solo make_booking con confirmación"

4. **Sin few-shot examples:**
   - GPT-4o-mini es suficientemente capaz
   - Few-shot aumentaría el costo (más tokens)
   - Instrucciones explícitas son más mantenibles que ejemplos

---

### Patrones de Diseño Utilizados

El proyecto implementa varios patrones de diseño para garantizar escalabilidad, mantenibilidad y separación de responsabilidades. A continuación se presentan los 3 patrones principales:

---

#### 1. Repository Pattern

**Ubicación:** `data/flights.py`

**Propósito:** Abstrae el acceso a datos, creando una capa intermedia entre la lógica de negocio y la fuente de datos.

**¿Cómo funciona?**
- Define funciones como `get_flight_status()`, `find_alternatives()`, `create_booking()`
- Estas funciones encapsulan toda la lógica de acceso a datos
- Las herramientas llaman a estas funciones, no acceden directamente a los datos

**Ventaja principal:**
Cuando migremos de datos mock a PostgreSQL, solo modificamos las funciones del repository. Las herramientas (`check_flight_status`, `find_alternative_flights`, `make_booking`) no necesitan cambios.

---

#### 2. Decorator Pattern

**Ubicación:** `tools/flight_tools.py`

**Propósito:** Convierte funciones Python normales en herramientas que el agente LangChain puede usar.

**¿Cómo funciona?**
- Usamos el decorator `@tool` de LangChain
- Este decorator agrega automáticamente:
  - Metadata (nombre, descripción)
  - Validación de tipos
  - Serialización a JSON para el LLM
  - Integración con el framework

**Ventaja principal:**
Sin el decorator, tendríamos que escribir manualmente toda la configuración para cada herramienta. El decorator hace esto automáticamente, reduciendo código boilerplate y errores.

---

#### 3. State Pattern (FSM - Finite State Machine)

**Ubicación:** `utils/state_manager.py`

**Propósito:** Gestiona los estados de la conversación usando una máquina de estados finitos.

**Estados del FSM:**
```
NOTIFIED (25%) → REBOOKING (50%) → RESOLVED (100%)  [Flujo A: Rebooking]
NOTIFIED (25%) → REFUND (50%) → RESOLVED (100%)     [Flujo B: Reembolso]
```

**¿Cómo funciona?**
- `StateManager` trackea el estado actual de cada conversación
- Detecta transiciones basándose en palabras clave del usuario y del agente
- Identifica interrupciones (cambio de flujo mid-conversation)
- Mantiene historial completo de transiciones

**Ventajas principales:**
- Visualizar progreso en tiempo real (sidebar muestra 25%, 50%, 100%)
- Detectar cambios de decisión del usuario
- Aplicar reglas específicas según el estado (ej: en RESOLVED, no permitir más cambios sin llamar al 0800-ITTI)
- Generar métricas y análisis de comportamiento del usuario

---

## Evolución del Chatbot

### Roadmap de Mejoras Propuestas

El chatbot actual representa un MVP funcional, pero existen múltiples oportunidades de mejora para convertirlo en un sistema de nivel empresarial. A continuación se presentan las evoluciones planificadas organizadas por fases de implementación.

---

### Fase 1: Testing Automatizado con LangSmith (En paralelo a todas las fases) URGENTE!

**Objetivo:** Implementar testing continuo, evaluación y monitoreo del agente usando LangSmith.

**LangSmith** es una plataforma de LangChain para:
- Debugging de cadenas y agentes
- Evaluación de calidad de respuestas
- Testing con datasets
- Monitoreo en producción

---

#### 1.1 Implementación de LangSmith

**Setup inicial:**
- Integrar LangSmith SDK en el proyecto
- Configurar tracing automático de todas las conversaciones
- Crear datasets de test cases con conversaciones golden

**Datasets de evaluación:**
- **Happy paths:** 10 casos de rebooking exitoso, 10 de reembolso exitoso
- **Edge cases:** Cambios de decisión, interrupciones, consultas fuera de contexto
- **Error cases:** Vuelos no encontrados, sin asientos disponibles

**Evaluadores automáticos:**
- **Tool usage correctness:** ¿Se usó la herramienta correcta en el momento correcto?
- **Response quality:** ¿La respuesta fue empática, clara y profesional?
- **Context retention:** ¿El agente mantuvo el contexto conversacional?
- **State transitions:** ¿Las transiciones del FSM fueron correctas?

---

#### 1.2 Estrategia de Evaluaciones (Evals) para Mejora de Prompting

**Objetivo:** Establecer un proceso iterativo de evaluación y optimización del prompting mediante evals sistemáticos.

**Metodología de Evals:**

**A) Definición de Métricas de Evaluación**

1. **Métricas de Comportamiento:**
   - **Tool Selection Accuracy:** % de veces que el agente usa la tool correcta
   - **Confirmation Compliance:** % de veces que pide confirmación cuando debe
   - **Context Adherence:** % de respuestas que mantienen el contexto conversacional
   - **Empathy Score:** Evaluación humana/LLM del tono empático (1-5)

2. **Métricas de Negocio:**
   - **Task Completion Rate:** % de conversaciones que llegan a RESOLVED
   - **User Satisfaction (simulada):** Score basado en fluidez de la conversación
   - **Error Recovery Rate:** % de errores manejados exitosamente
   - **Average Turns to Resolution:** Número promedio de mensajes hasta resolución

**B) Proceso de Evaluación Iterativa**

**Ciclo 1: Baseline (Prompt actual)**
- Ejecutar eval suite completo con el prompt actual
- Documentar métricas baseline
- Identificar los 3 casos con peor performance

**Ciclo 2: Optimización de Confirmaciones**
- Modificar sección del prompt sobre confirmaciones explícitas
- Variantes a testear:
  - **V1:** Confirmación más detallada con lista de consecuencias
  - **V2:** Confirmación más breve pero directa
  - **V3:** Confirmación con ejemplo específico
- Ejecutar evals comparativos
- Seleccionar mejor variante

**Ciclo 3: Optimización de Tool Usage**
- Ajustar instrucciones de cuándo usar cada tool
- Variantes a testear:
  - **V1:** Instrucciones más explícitas paso a paso
  - **V2:** Instrucciones con ejemplos negativos ("NO uses X cuando...")
  - **V3:** Instrucciones con reglas de prioridad
- Ejecutar evals comparativos
- Seleccionar mejor variante

**Ciclo 4: Optimización de Contexto Conversacional**
- Mejorar manejo de respuestas ambiguas del usuario
- Variantes a testear:
  - **V1:** Instrucciones más explícitas sobre interpretación de números
  - **V2:** Sistema de clarificación proactiva
  - **V3:** Contexto expandido con última pregunta formulada
- Ejecutar evals comparativos
- Seleccionar mejor variante

**C) Dataset de Evaluación**

**Estructura del dataset (mínimo 50 casos):**

```
Test Case Categories:
├── Happy Paths (20 casos)
│   ├── Rebooking directo (10)
│   └── Reembolso directo (10)
├── Edge Cases (20 casos)
│   ├── Cambio de decisión (8)
│   ├── Interrupciones mid-flow (6)
│   └── Consultas fuera de contexto (6)
├── Error Handling (10 casos)
│   ├── Vuelo no encontrado (4)
│   ├── Sin asientos disponibles (3)
│   └── Respuestas ambiguas del usuario (3)
```

**Formato de test case:**
- **Input inicial:** Configuración del escenario (pasajero, vuelo, etc.)
- **Conversación:** Lista de mensajes usuario-agente
- **Resultado esperado:** Estado final, herramientas usadas, criterios de éxito
- **Evaluadores aplicables:** Lista de evaluadores custom para este caso

**D) Evaluadores Custom (LLM-as-Judge)**

**Evaluador de Empatía:**
```
Prompt: "Evalúa si la siguiente respuesta del agente muestra empatía
apropiada para un pasajero cuyo vuelo fue cancelado.
Califica de 1-5 considerando: tono, reconocimiento de la frustración,
y proactividad en ofrecer soluciones."
```

**Evaluador de Confirmación:**
```
Prompt: "Verifica si el agente pidió confirmación EXPLÍCITA antes de
realizar una acción irreversible (reserva o reembolso).
La confirmación debe mencionar que no podrán hacer cambios sin llamar
al 0800-ITTI. Responde: PASS/FAIL con justificación."
```

**Evaluador de Tool Usage:**
```
Prompt: "Evalúa si el agente usó las herramientas correctamente:
- ¿Usó find_alternative_flights antes de recomendar opciones?
- ¿Usó make_booking solo después de confirmación?
- ¿No inventó información sin usar herramientas?
Responde: PASS/FAIL por cada criterio."
```

**E) Implementación Técnica**

**Integración con LangSmith:**
- Crear proyecto en LangSmith para el chatbot
- Subir dataset de evaluación a LangSmith
- Configurar evaluadores custom
- Ejecutar evals periódicamente (daily durante desarrollo)

**Proceso de A/B Testing:**
- Implementar feature flag para cambiar entre versiones de prompts
- Ejecutar ambas versiones en paralelo con tráfico dividido 50/50
- Comparar métricas después de N conversaciones
- Promover ganador a producción

**Frecuencia de Evals:**
- **Pre-commit:** Evals rápidos (10 casos críticos) antes de merge
- **Daily:** Suite completo (50+ casos) automáticamente
- **Pre-release:** Suite extendido (100+ casos) antes de deploy

---

#### 1.3 Monitoreo en Producción

**Dashboard de métricas en tiempo real:**
- Latencia promedio de respuestas
- Tasa de uso de cada tool
- Tasa de escalamiento a humanos (futuro)
- Sentimiento promedio de conversaciones
- Errores y excepciones
- Conversaciones por día
- Tasa de resolución exitosa
- Tiempo promedio de resolución
- Herramientas más utilizadas
- Flujos más comunes (rebooking vs refund)

**CI/CD Pipeline:**
- **Pre-commit hooks:** Evals rápidos (10 casos críticos) + linting
- **Pull Request checks:** Suite completo de evals (50+ casos) antes de merge
- **Staging deployment:** Deploy automático a entorno de staging después de merge
- **Production deployment:** Deploy manual después de aprobación + smoke tests
- **Rollback automático:** Si las métricas degradan >20% en los primeros 10 minutos

**Testing Automatizado:**
- **Playwright:** Tests end-to-end de la UI de Streamlit
  - Flujos completos de rebooking y reembolso
  - Verificación de sidebar (progreso, estados FSM)
  - Tests de regresión visual
  - Simulación de interacciones del usuario (clicks, inputs, navegación)

- **MCP (Model Context Protocol) de Claude:**
  - Integración con Claude para testeos conversacionales automatizados
  - Validación de respuestas del agente en diferentes escenarios
  - Testing de edge cases y manejo de errores
  - Verificación de uso correcto de herramientas (tools)

---

### Fase 2: Integración de Base de Datos Real

**Objetivo:** Migrar de datos mockeados a una base de datos persistente y escalable.

**Implementación:**
- Reemplazar `data/flights.py` con conexión a PostgreSQL o MongoDB
- Agregar migraciones de base de datos
- Mantener las mismas interfaces de las funciones para minimizar cambios en tools

**Beneficios:**
- Seguridad
- Persistencia de datos entre sesiones
- Capacidad de escalar a múltiples usuarios concurrentes
- Posibilidad de hacer análisis histórico de reservas
- Base sólida para integraciones futuras

---

### Fase 3: RAG con Vector Database

**Objetivo:** Implementar Retrieval-Augmented Generation para responder preguntas complejas usando documentación de la empresa y para mantener la seguridad de los datos. 

**Casos de uso:**
- Políticas de equipaje, cancelaciones, cambios
- Preguntas frecuentes (FAQs)
- Procedimientos internos de la aerolínea
- Regulaciones y normativas de aviación civil

**Stack tecnológico propuesto:**
- **Vector DB:** Pinecone, Weaviate ver otras
- **Embeddings:** OpenAI text-embedding-3-small
- **Framework:** LangChain

**Arquitectura:**
```
Usuario pregunta → Agente detecta necesidad de información
                ↓
         Busca en Vector DB (top-k=3 documentos relevantes)
                ↓
         Inyecta contexto en prompt del LLM
                ↓
         LLM genera respuesta fundamentada en documentos
```

**Documentos a indexar:**
- Manual de políticas de la aerolínea (PDF)
- FAQs de atención al cliente
- Regulaciones de ANAC/IATA
- Procedimientos de reembolso y compensaciones

---

### Fase 4: Análisis de Sentimientos y Escalamiento Automático - Mejora de UX/UI

**Objetivo:** Detectar frustración del usuario y derivar automáticamente a agentes humanos cuando sea necesario. 
Mejorar writing a traves de la implementación de éste, ya que toda estadística sin acción solo es burocracia. 

**Implementación:**

**1. Detección de Sentimiento:**
```python
from langchain.chains import LLMChain

def analyze_sentiment(message: str) -> dict:
    """Analiza el sentimiento del mensaje del usuario"""
    prompt = f"""Analiza el sentimiento del siguiente mensaje:
    "{message}"

    Clasifica como: positivo, neutral, negativo, muy_negativo
    Si detectas frustración o enojo, marca como escalate: true

    Responde en JSON."""

    result = llm.predict(prompt)
    return json.loads(result)
```

**2. Sistema de Escalamiento:**
```python
class EscalationManager:
    def __init__(self):
        self.frustration_threshold = 2  # Mensajes negativos consecutivos
        self.frustration_count = 0

    def should_escalate(self, sentiment: str) -> bool:
        if sentiment in ["negativo", "muy_negativo"]:
            self.frustration_count += 1
        else:
            self.frustration_count = max(0, self.frustration_count - 1)

        return self.frustration_count >= self.frustration_threshold

    def escalate_to_human(self, conversation_id: str):
        # Notificar a supervisor
        # Transferir conversación
        # Actualizar estado en DB
        pass
```

**Triggers de escalamiento:**
- 2+ mensajes consecutivos con sentimiento negativo
- Usuario solicita explícitamente hablar con humano
- Problema no resuelto después de 10 interacciones
- Palabras clave de alta prioridad: "abogado", "demanda", "compensación legal"

**Mensaje de transición:**
```
"Entiendo su frustración, y lamento que no hayamos podido resolver
esto a su satisfacción. Voy a transferirlo inmediatamente con un
supervisor humano que podrá asistirle mejor. Por favor aguarde un momento."
```

---

### Fase 5: Soporte Multicanal y Multiidioma

**Objetivo:** Expandir el chatbot a múltiples plataformas y idiomas.

**Canales a soportar:**
- WhatsApp 
- Telegram Bot
- Facebook Messenger
- Email (respuestas automáticas)
- Widget web embebido
- App móvil nativa

**Idiomas a soportar:**
- Español (actual)
- Inglés
- Portugués
- Italiano


---

## Referencias

### Documentación Oficial

**Claude (Anthropic)**
- [Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) - Guía sobre uso de herramientas con Claude
- [Prompt Engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) - Mejores prácticas de prompting

**LangChain**
- [LangChain Documentation](https://docs.langchain.com/) - Framework para desarrollo con LLMs

**OpenAI**
- [Text Generation Guide](https://platform.openai.com/docs/guides/text) - Documentación de GPT-4 y modelos de texto

**Streamlit**
- [Streamlit Documentation](https://docs.streamlit.io/) - Framework para aplicaciones web con Python
# vuelaconnosotros_itti
