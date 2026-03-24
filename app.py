import streamlit as st
import pandas as pd
import numpy as np
import random
# --- 4. LÓGICA DE EVENTOS ALEATORIOS (CONTINGENCIAS) ---
# Inicializar estado del evento si no existe
if 'evento_activo' not in st.session_state: 
    st.session_state['evento_activo'] = None

def generar_contingencia():
    """Simula imprevistos operativos aleatorios durante la maniobra."""
    eventos = [
        {"msg": "⚠️ ¡Pérdida de Circulación! El pozo está absorbiendo fluido de control.", "tipo": "error", "icono": "🚱"},
        {"msg": "⚠️ ¡Fuga en Manguera de Inyección! Detenga la bomba de superficie inmediatamente.", "tipo": "warning", "icono": "🧯"},
        {"msg": "⚠️ ¡Pescado con Arena! La tensión sube erráticamente, no hay despegue claro.", "tipo": "info", "icono": "⏳"},
        {"msg": "🚨 ¡Tormenta Eléctrica detectada! Evalúe suspender maniobra con varilla en boca de pozo.", "tipo": "error", "icono": "⚡"},
        {"msg": "✅ Operación normal. Siga tensionando con precaución.", "tipo": "success", "icono": "👍"}
    ]
    # Elegimos un evento al azar
    st.session_state['evento_activo'] = random.choice(eventos)
# 1. CONFIGURACIÓN E IDENTIDAD VISUAL DE IPCL MENFA
st.set_page_config(page_title="IPCL MENFA - Gestión Integral de Intervenciones", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .modulo-header {
        background-color: #00457C; color: white; padding: 15px;
        border-radius: 10px; margin-bottom: 20px; text-align: center;
    }
    .card-tecnica {
        background-color: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #00457C; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px; min-height: 220px;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #00457C;
        color: white; font-weight: bold; height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE ACTIVOS (MENDOZA)
if 'data_pozos' not in st.session_state:
    st.session_state['data_pozos'] = pd.DataFrame({
        "Pozo": ["MENFA-101", "MENFA-102", "MENFA-105", "Puesto-Pozo-8"],
        "Profundidad (m)": [1200, 1550, 1800, 1400],
        "Grado Varilla": ["Grado D", "Grado K", "Grado KD", "Grado D"],
        "Presión Reservorio (PSI)": [1500, 1850, 2100, 1600],
        "Historial Falla": ["Fatiga por Ciclos", "Corrosión por CO2/H2S", "Desgaste por Rozamiento", "Corte por Sobre-tensión"]
    })

# 3. GESTIÓN DE SESIÓN Y NAVEGACIÓN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {}
if 'pozo_seleccionado' not in st.session_state: st.session_state['pozo_seleccionado'] = None

# --- FUNCIONES DE APOYO ---
def volver_dashboard():
    st.session_state['pantalla'] = 'dashboard'
    st.rerun()

def header_app():
    c1, c2 = st.columns([4, 1])
    with c1:
        u = st.session_state['user']
        st.subheader(f"🏢 IPCL MENFA | Operador: {u.get('nombre')} | DNI: {u.get('dni')}")
    with c2:
        if st.button("Cerrar Sesión"):
            st.session_state['auth'] = False
            st.rerun()
    st.divider()

# --- PANTALLAS DEL SISTEMA ---

def vista_registro():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+MENDOZA", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema Técnico</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            nombre = st.text_input("Nombre Completo")
            dni = st.text_input("DNI / Legajo")
            rol = st.selectbox("Función", ["Instructor", "Jefe de Equipo", "Company Man", "Alumno"])
            if st.form_submit_button("Ingresar"):
                if nombre and dni:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": nombre, "dni": dni, "rol": rol}
                    st.rerun()
                else: st.error("Por favor, complete todos los campos.")

def vista_dashboard():
    header_app()
    st.title("Panel de Control de Operaciones")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card-tecnica"><h3>📋 Gestión de Activos</h3><p>Consulta de legajos, historial de fallas y datos de diseño del pozo.</p></div>', unsafe_allow_html=True)
        if st.button("Ver Legajos"): st.session_state['pantalla'] = 'legajo'; st.rerun()

    with col2:
        st.markdown('<div class="card-tecnica"><h3>🏗️ Simulador Pulling</h3><p>Worksteps Case 1 & 2. Protocolos de intervención y seguridad API.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Simulador"): st.session_state['pantalla'] = 'simulador'; st.rerun()

    with col3:
        st.markdown('<div class="card-tecnica"><h3>🎣 Pesca e Ingeniería</h3><p>Simulación de tensiones en tiempo real y diagnóstico de fallas (RCA).</p></div>', unsafe_allow_html=True)
        if st.button("Módulo de Pesca"): st.session_state['pantalla'] = 'pesca'; st.rerun()

    st.markdown("---")
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        if st.button("📖 Manual Técnico (Costos/API)"): st.session_state['pantalla'] = 'manual'; st.rerun()
    with col_inf2:
        if st.button("🧮 Calculadora de Ahogo"): st.session_state['pantalla'] = 'ingenieria'; st.rerun()

def vista_legajo():
    header_app()
    if st.button("⬅️ Volver"): volver_dashboard()
    st.markdown('<div class="modulo-header"><h2>Legajo Técnico de Pozos (Mendoza)</h2></div>', unsafe_allow_html=True)
    
    pozo_sel = st.selectbox("Seleccione Activo:", st.session_state['data_pozos']["Pozo"])
    detalles = st.session_state['data_pozos'][st.session_state['data_pozos']["Pozo"] == pozo_sel].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Profundidad", f"{detalles['Profundidad (m)']} m")
    c2.metric("Grado API 11B", detalles['Grado Varilla'])
    c3.metric("Presión Estática", f"{detalles['Presión Reservorio (PSI)']} PSI")
    
    st.info(f"**Historial de Integridad:** {detalles['Historial Falla']}")
    if st.button("Transferir Datos al Simulador"):
        st.session_state['pozo_seleccionado'] = detalles.to_dict()
        st.success(f"Parámetros de {pozo_sel} cargados correctamente.")

def vista_pesca_pro():
    header_app()
    if st.button("⬅️ Volver"): volver_dashboard()
    
    if not st.session_state['pozo_seleccionado']:
        st.warning("⚠️ Debe seleccionar un pozo en el módulo de 'Legajo' antes de operar.")
        return

    datos = st.session_state['pozo_seleccionado']
    st.markdown(f'<div class="modulo-header"><h2>Simulador de Pesca: {datos["Pozo"]}</h2></div>', unsafe_allow_html=True)
    
    tab_rca, tab_tension = st.tabs(["🔬 Diagnóstico de Falla", "📈 Monitor de Tensión"])
    
    with tab_rca:
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://via.placeholder.com/500x300.png?text=Imagen+Falla+Campo", caption="Muestra de pesca")
        with c2:
            opcion = st.radio("¿Qué diagnóstico observa?", ["Fatiga por Ciclos", "Corrosión por CO2/H2S", "Desgaste por Rozamiento", "Corte por Sobre-tensión"])
            if st.button("Validar Diagnóstico"):
                if opcion == datos['Historial Falla']: st.success("Correcto. Coincide con el historial.")
                else: st.error("Incorrecto. Revise el patrón de rotura.")

    with tab_tension:
        limites = {"Grado D": 115000, "Grado K": 85000, "Grado KD": 115000}
        max_load = limites[datos['Grado Varilla']]
        
        col_ctrl, col_graph = st.columns([1, 2])
        with col_ctrl:
            st.write(f"**Límite Fluencia:** {max_load} lbs")
            tension = st.slider("Carga en Martin Decker (lbs)", 0, int(max_load*1.2), 40000)
            if tension > max_load: st.error("🚨 ROTURA DE HERRAMIENTA")
            elif tension > max_load * 0.8: st.warning("⚠️ CARGA CRÍTICA")
        
        with col_graph:
            datos_y = np.linspace(30000, tension, 15) + np.random.normal(0, 1000, 15)
            st.line_chart(pd.DataFrame({"Tensión": datos_y}))

def vista_manual():
    header_app()
    if st.button("⬅️ Volver"): volver_dashboard()
    st.header("Manual de Gestión de Intervenciones")
    st.markdown("""
    ### 🎯 Objetivos MENFA
    * **OPEX**: Reducción del 30% del costo operativo mediante prevención.
    * **Frecuencia**: Meta de 1 intervención cada 2 años.
    * **Normas**: API 4F, 11B y RP 59.
    """)

def vista_simulador_pasos():
    header_app()
    if st.button("⬅️ Volver"): volver_dashboard()
    st.header("Protocolos Operativos Case 1 & 2")
    caso = st.selectbox("Seleccione el Caso:", ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla"])
    pasos = ["Ahogo de pozo", "Checklist Seguridad", "Desmonte de cabezal", "Pesca/Extracción", "Prueba Hermeticidad"]
    for p in pasos: st.checkbox(p)

def vista_ingenieria():
    header_app()
    if st.button("⬅️ Volver"): volver_dashboard()
    st.header("Cálculos de Control de Pozos (API RP 59)")
    prof = st.number_input("Profundidad (m)", 1200)
    p_res = st.number_input("Presión (PSI)", 1500)
    densidad = (p_res + 200) / ((prof * 3.28) * 0.052)
    st.metric("Densidad de Ahogo Requerida", f"{densidad:.2f} ppg")
def calculadora_punto_libre():
    st.subheader("🧮 Estimación de Punto Libre (Stretch Method)")
    st.write("Determine a qué profundidad está atrapada la sarta según su estiramiento.")
    
    c1, c2 = st.columns(2)
    with c1:
        pull_1 = st.number_input("Tensión Inicial (lbs)", value=20000)
        pull_2 = st.number_input("Tensión Final (lbs)", value=40000)
        estiramiento = st.number_input("Estiramiento observado (pulgadas)", value=15.0)
    
    with c2:
        # Constante para varilla de 7/8" (ejemplo)
        constante = 0.85 
        diff_pull = pull_2 - pull_1
        if diff_pull > 0:
            prof_libre = (estiramiento * constante * 1000000) / diff_pull
            st.metric("Profundidad del Atrapamiento", f"{prof_libre:.0f} metros")
            st.info("Cálculo basado en constantes elásticas de acero API 11B.")
# --- LÓGICA DE RUTEADOR ---
if not st.session_state['auth']:
    vista_registro()
else:
    p = st.session_state['pantalla']
    if p == 'dashboard': vista_dashboard()
    elif p == 'legajo': vista_legajo()
    elif p == 'pesca': vista_pesca_pro()
    elif p == 'manual': vista_manual()
    elif p == 'simulador': vista_simulador_pasos()
    elif p == 'ingenieria': vista_ingenieria()
