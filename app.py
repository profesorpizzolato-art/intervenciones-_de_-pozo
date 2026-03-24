import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Simulador MENFA", layout="wide")

# Inicializar estados de sesión si no existen
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'usuario_data' not in st.session_state:
    st.session_state['usuario_data'] = {}

# 2. FUNCIÓN DE LOGO Y REGISTRO
def mostrar_registro():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo MENFA (Imagen inicial)
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+-+MENDOZA", use_container_width=True)
        st.subheader("📝 Registro de Operaciones")
        
        with st.form("registro_usuario"):
            nombre = st.text_input("Nombre y Apellido")
            legajo = st.text_input("Legajo / DNI")
            turno = st.selectbox("Turno", ["Mañana", "Tarde", "Noche"])
            
            btn_registro = st.form_submit_button("Ingresar al Sistema")
            
            if btn_registro:
                if nombre and legajo:
                    st.session_state['autenticado'] = True
                    st.session_state['usuario_data'] = {
                        "nombre": nombre,
                        "legajo": legajo,
                        "turno": turno
                    }
                    st.rerun()
                else:
                    st.warning("Por favor, complete sus datos para continuar.")

# 3. FUNCIÓN DEL SIMULADOR PRINCIPAL
def mostrar_simulador():
    # Encabezado con datos del usuario
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("🏗️ Simulador de Pulling y Pesca")
        user = st.session_state['usuario_data']
        st.write(f"**Operador:** {user['nombre']} | **Legajo:** {user['legajo']} | **Turno:** {user['turno']}")
    with c2:
        if st.button("Cerrar Sesión", key="logout_btn"):
            st.session_state['autenticado'] = False
            st.rerun()

    st.divider()

    # --- SIDEBAR CON KEYS ÚNICAS (Para evitar el error DuplicateElementId) ---
    st.sidebar.header("⚙️ Parámetros de Simulación")
    
    tipo_op = st.sidebar.selectbox(
        "Seleccione el Caso de Pesca:",
        ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla"],
        key="sb_tipo_operacion" # Identificador único
    )
    
    grado_varilla = st.sidebar.selectbox(
        "Grado de Varilla (API 11B):",
        ["Grado D", "Grado KD", "Grado K"],
        key="sb_grado_varilla" # Identificador único
    )

    # --- CUERPO DEL SIMULADOR ---
    tab1, tab2 = st.tabs(["📋 Programa de Pozo", "🧮 Cálculos de Ingeniería"])

    with tab1:
        st.subheader(f"Guía Operativa: {tipo_op}")
        # Lógica de pasos basada en tus archivos DOCX
        if "Vástago" in tipo_op:
            pasos = ["Descomprimir columnas", "Retirar cabeza de mula", "Capturar vástago", "Montar BOP de varillas"]
        else:
            pasos = ["Ahogar pozo (API RP 59)", "Retirar vástago", "Sacar varillas en tiros dobles", "Bajar pescador"]
            
        for i, p in enumerate(pasos):
            st.checkbox(p, key=f"step_{i}")

    with tab2:
        st.subheader("Cálculos de Control de Pozos")
        st.info("Sección técnica para cálculo de densidades y volúmenes de ahogo.")
        # Aquí puedes agregar las fórmulas que definimos antes

# 4. CONTROL DE FLUJO
if not st.session_state['autenticado']:
    mostrar_registro()
else:
    mostrar_simulador()
import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE ESTILO Y PÁGINA
st.set_page_config(page_title="MENFA - Gestión de Intervenciones", layout="wide")

# CSS para diseño de "Cards" (Módulos)
st.markdown("""
    <style>
    .modulo-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00457C;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #00457C;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'pantalla' not in st.session_state:
    st.session_state['pantalla'] = 'inicio'
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = None

# --- COMPONENTE: HEADER ---
def mostrar_header():
    c1, c2 = st.columns([3, 1])
    with c1:
        st.image("https://via.placeholder.com/400x100.png?text=IPCL+MENFA+MENDOZA", width=300)
    with c2:
        if st.session_state['usuario']:
            st.write(f"👤 **{st.session_state['usuario']}**")
            if st.button("Cerrar Sesión"):
                st.session_state['usuario'] = None
                st.session_state['pantalla'] = 'inicio'
                st.rerun()

# --- PANTALLA: REGISTRO INICIAL ---
def pantalla_registro():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Sistema de Control de Pozos</h2>", unsafe_allow_html=True)
        with st.form("registro_form"):
            nombre = st.text_input("Nombre del Instructor/Alumno")
            legajo = st.text_input("DNI / Matrícula")
            submit = st.form_submit_button("Ingresar a la Plataforma")
            if submit and nombre and legajo:
                st.session_state['usuario'] = nombre
                st.rerun()

# --- PANTALLA: MENÚ DE MÓDULOS (Dashboard) ---
def dashboard_principal():
    mostrar_header()
    st.title("Panel de Control Educativo")
    
    # ORGANIZACIÓN EN GRILLA (Módulos de todo lo hablado)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="modulo-card"><h3>📖 Contenido Teórico</h3><p>Acceso a la Clase 11: Conceptos de Pulling, costos operativos (30%) y objetivos de frecuencia.</p></div>', unsafe_allow_html=True)
        if st.button("Ver Clase 11", key="btn_clase"):
            st.session_state['pantalla'] = 'clase'
            st.rerun()

    with col2:
        st.markdown('<div class="modulo-card"><h3>🏗️ Simulador de Pesca</h3><p>Módulos de Vástago Cortado y Pesca de Varillas con monitor Martin Decker.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Simulador", key="btn_sim"):
            st.session_state['pantalla'] = 'simulador'
            st.rerun()

    with col3:
        st.markdown('<div class="modulo-card"><h3>🧮 Calculadora API</h3><p>Cálculos de ahogo (API RP 59), densidades, volúmenes y tipos de varillas (API 11B).</p></div>', unsafe_allow_html=True)
        if st.button("Ir a Cálculos", key="btn_calc"):
            st.session_state['pantalla'] = 'calculos'
            st.rerun()

    st.divider()
    st.subheader("📋 Estado de Normativas")
    st.info("Cumplimiento actual: API Spec 4F (Estructuras) | API RP 4G (Mantenimiento) | API 11B (Varillas)")

# --- VISTAS ESPECÍFICAS (SIMULADOR, CÁLCULOS, ETC.) ---
def vista_simulador():
    mostrar_header()
    if st.button("⬅️ Volver al Panel"):
        st.session_state['pantalla'] = 'inicio'
        st.rerun()
    
    st.subheader("Módulo de Simulación en Vivo")
    op = st.selectbox("Seleccione Programa de Pozo:", ["Vástago Cortado", "Pesca de Varilla"], key="sel_op")
    
    # Aquí va el monitor de peso y los pasos que definimos antes
    st.write(f"Ejecutando protocolo para: **{op}**")
    peso = st.slider("Carga en Gancho (lbs)", 0, 60000, 45000, key="slider_peso")
    if peso < 35000: st.error("¡PESCA DETECTADA!")

# --- LÓGICA DE NAVEGACIÓN ---
if st.session_state['usuario'] is None:
    pantalla_registro()
else:
    if st.session_state['pantalla'] == 'inicio':
        dashboard_principal()
    elif st.session_state['pantalla'] == 'simulador':
        vista_simulador()
    # Aquí puedes añadir las funciones para 'clase' y 'calculos' siguiendo la misma lógica
