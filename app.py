import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE ESTILO Y PÁGINA
st.set_page_config(page_title="IPCL MENFA - Gestión de Operaciones", layout="wide")

# Diseño estético (CSS)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .modulo-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-top: 6px solid #00457C;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        min-height: 220px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #00457C;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN (Control de navegación)
if 'auth' not in st.session_state:
    st.session_state['auth'] = False
if 'pantalla' not in st.session_state:
    st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state:
    st.session_state['user'] = {}

# --- COMPONENTES INTERNOS ---

def login_registro():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+MENDOZA", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema Técnico</h2>", unsafe_allow_html=True)
        with st.form("form_registro"):
            nombre = st.text_input("Instructor / Alumno")
            dni = st.text_input("DNI o Legajo")
            rol = st.selectbox("Rol", ["Instructor", "Alumno", "Supervisor de Campo"])
            if st.form_submit_button("Ingresar"):
                if nombre and dni:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": nombre, "rol": rol}
                    st.rerun()
                else:
                    st.error("Complete los datos de registro.")

def mostrar_header():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.write(f"🏢 **IPCL MENFA** | Usuario: {st.session_state['user']['nombre']} ({st.session_state['user']['rol']})")
    with c2:
        if st.button("Cerrar Sesión"):
            st.session_state['auth'] = False
            st.rerun()
    st.divider()

# --- MÓDULOS DEL DASHBOARD ---

def dashboard():
    mostrar_header()
    st.title("Panel Principal de Aplicación")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="modulo-card"><h3>📖 Módulo Teórico</h3><p>Conceptos de Pulling, costos (30% OPEX) y objetivos de mantenimiento (2 años/pozo).</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Manual Clase 11"): st.session_state['pantalla'] = 'clase'; st.rerun()

    with col2:
        st.markdown('<div class="modulo-card"><h3>🏗️ Simulador de Pesca</h3><p>Programas de pozo interactivos para Vástago y Varillas con control de peso en vivo.</p></div>', unsafe_allow_html=True)
        if st.button("Iniciar Simulación"): st.session_state['pantalla'] = 'simulador'; st.rerun()

    with col3:
        st.markdown('<div class="modulo-card"><h3>🧮 Ingeniería API</h3><p>Calculadora de ahogo (API RP 59) y especificaciones de varillas (API 11B).</p></div>', unsafe_allow_html=True)
        if st.button("Ir a Cálculos"): st.session_state['pantalla'] = 'calculos'; st.rerun()

# --- VISTAS DETALLADAS ---

def vista_simulador():
    mostrar_header()
    if st.button("⬅️ Volver al Panel"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Simulador de Intervenciones")
    tipo = st.selectbox("Protocolo Operativo:", ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla"], key="sel_sim")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Pasos del Programa de Pozo")
        pasos = ["Check-list API RP 4G", "Descomprimir Columnas", "Ahogar si es necesario"]
        if "Varilla" in tipo: pasos.extend(["Sacar en tiros dobles", "Bajar pescador"])
        else: pasos.extend(["Pescar vástago", "Montar BOP de varillas"])
        
        for i, p in enumerate(pasos): st.checkbox(p, key=f"p_{i}")
        
    with c2:
        st.info("Monitor de Carga")
        peso = st.slider("Carga Martin Decker (lbs)", 0, 60000, 45000, key="slider_m")
        if peso < 35000: st.error("⚠️ PESCA DETECTADA")
        else: st.success("✅ Peso íntegro")

def vista_calculos():
    mostrar_header()
    if st.button("⬅️ Volver al Panel"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Calculadora Técnica API")
    prof = st.number_input("Profundidad de Bomba (m)", value=1200)
    presion = st.number_input("Presión de Reservorio (PSI)", value=1500)
    
    st.divider()
    # Fórmulas API integradas
    p_ft = prof * 3.28
    densidad = (presion + 200) / (p_ft * 0.052)
    st.metric("Densidad de Ahogo Requerida (API RP 59)", f"{densidad:.2f} ppg")

# --- CONTROLADOR DE NAVEGACIÓN ---
if not st.session_state['auth']:
    login_registro()
else:
    if st.session_state['pantalla'] == 'dashboard': dashboard()
    elif st.session_state['pantalla'] == 'simulador': vista_simulador()
    elif st.session_state['pantalla'] == 'calculos': vista_calculos()
        
