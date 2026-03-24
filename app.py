import streamlit as st
import pandas as pd  # <--- Verifica que esta línea esté presente
# 1. CONFIGURACIÓN E IDIOMA
st.set_page_config(page_title="IPCL MENFA - Sistema de Gestión Técnica", layout="wide")

# Estilos de Interfaz Profesional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .modulo-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        border-top: 6px solid #00457C; box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 20px; min-height: 250px;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #00457C;
        color: white; font-weight: bold; height: 3.5em;
    }
    .status-box {
        padding: 10px; border-radius: 5px; background-color: #e9ecef;
        font-size: 0.9em; border-left: 4px solid #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE ESTADOS DE LA APLICACIÓN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user_data' not in st.session_state: st.session_state['user_data'] = {}

# --- COMPONENTES GLOBALES ---

def header_institucional():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.subheader(f"🏢 IPCL MENFA | Operador: {st.session_state['user_data'].get('nombre')} | {st.session_state['user_data'].get('rol')}")
    with c2:
        if st.button("Cerrar Sesión", key="logout"):
            st.session_state['auth'] = False
            st.rerun()
    st.divider()

# --- PANTALLA 1: REGISTRO ---
def pantalla_registro():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+MENDOZA", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Registro de Operaciones</h2>", unsafe_allow_html=True)
        with st.form("registro_profesional"):
            nombre = st.text_input("Nombre y Apellido")
            legajo = st.text_input("DNI / Legajo Técnico")
            rol = st.selectbox("Función", ["Jefe de Equipo", "Company Man", "Encargado de Turno", "Alumno Técnico"])
            if st.form_submit_button("Ingresar al Sistema"):
                if nombre and legajo:
                    st.session_state['auth'] = True
                    st.session_state['user_data'] = {"nombre": nombre, "rol": rol, "legajo": legajo}
                    st.rerun()
                else: st.error("Complete los datos.")

# --- PANTALLA 2: DASHBOARD PRINCIPAL ---
def dashboard():
    header_institucional()
    st.title("Panel de Control de Intervenciones")
    
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="modulo-card"><h3>📖 Manual de Procedimientos</h3><p>Fundamentos de Pulling, análisis de costos (30% OPEX) y objetivos de mantenimiento bajo normas API.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Manual Técnico"): st.session_state['pantalla'] = 'manual'; st.rerun()

    with c2:
        st.markdown('<div class="modulo-card"><h3>🏗️ Simulador de Pulling</h3><p>Ejecución de protocolos para Vástago Cortado y Pesca de Varilla con monitoreo de tensión en tiempo real.</p></div>', unsafe_allow_html=True)
        if st.button("Iniciar Simulación"): st.session_state['pantalla'] = 'simulador'; st.rerun()

    with c3:
        st.markdown('<div class="modulo-card"><h3>🧮 Ingeniería de Control</h3><p>Calculadora de densidades de ahogo, presiones y base de datos de varillas de bombeo API 11B.</p></div>', unsafe_allow_html=True)
        if st.button("Cálculos Críticos"): st.session_state['pantalla'] = 'ingenieria'; st.rerun()

# --- PANTALLA 3: MANUAL DE PROCEDIMIENTOS (DETALLADO) ---
def vista_manual():
    header_institucional()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Manual de Procedimientos y Costos Operativos")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🎯 Objetivos de Gestión
        * **Optimización**: Lograr una frecuencia de **1 intervención cada 2 años** en pozos estabilizados.
        * **Impacto Económico**: Las intervenciones representan hasta el **30% del costo operativo** en yacimientos profundos.
        * **Definición**: Reparación o cambio de elementos mediante equipo de pulling/guinche.
        """)
    with col2:
        st.info("**Normativas de Referencia:**\n\n* **API Spec 4F**: Estructuras.\n* **API RP 4G**: Inspección.\n* **API 11B**: Varillas.\n* **API RP 59**: Control de Pozos.")

# --- PANTALLA 4: SIMULADOR (DETALLADO) ---
def vista_simulador():
    header_institucional()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Simulador de Intervención Crítica")
    caso = st.selectbox("Protocolo Operativo:", ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla"], key="sel_caso")
    
    col_izq, col_der = st.columns([2, 1])
    
    with col_izq:
        st.subheader("Workstep de Operación")
        if "Vástago" in caso:
            pasos = [
                "Descomprimir entre columnas a pileta.", "Montar equipo y realizar Check-list (Jefe + Company).",
                "Retirar cabeza de mula y desplazar.", "Capturar vástago con pescador.",
                "Montar BOP de varillas.", "Clavar bomba y realizar prueba de hermeticidad/bloqueo."
            ]
        else:
            pasos = [
                "Verificar boca de pozo y ahogar (API RP 59).", "Charla de seguridad y Check-list.",
                "Retirar vástago y colocar maniobra.", "Constatar falta de peso (Pesca verificada).",
                "Sacar varillas en TIROS DOBLES revisando material.", "Probar hermeticidad de cañería."
            ]
        for i, p in enumerate(pasos): st.checkbox(f"{i+1}. {p}", key=f"chk_{i}")

    with col_der:
        st.markdown("### Monitor Martin Decker")
        tension = st.slider("Tensión (lbs)", 0, 70000, 45000, key="slider_tension")
        if tension < 38000: st.error("⚠️ PESCA DETECTADA")
        else: st.success("✅ Tensión Nominal")

# --- PANTALLA 5: INGENIERÍA (DETALLADO) ---
def vista_ingenieria():
    header_institucional()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Cálculos de Ingeniería de Control")
    c1, c2 = st.columns(2)
    with c1:
        prof = st.number_input("Profundidad (m)", value=1500)
        p_res = st.number_input("Presión de Reservorio (PSI)", value=1800)
        densidad = (p_res + 200) / ((prof * 3.28) * 0.052)
        st.metric("Densidad de Ahogo Requerida", f"{densidad:.2f} ppg")
    
    with c2:
        st.markdown("### Tabla de Varillas API 11B")
        df_var = pd.DataFrame({
            "Grado": ["D", "K", "KD", "Fibra"],
            "Peso (lb/ft)": [1.64, 1.63, 1.65, 0.65],
            "Resistencia (PSI)": [115000, 85000, 115000, 100000]
        })
        st.table(df_var)

# --- NAVEGACIÓN ---
if not st.session_state['auth']:
    pantalla_registro()
else:
    if st.session_state['pantalla'] == 'dashboard': dashboard()
    elif st.session_state['pantalla'] == 'manual': vista_manual()
    elif st.session_state['pantalla'] == 'simulador': vista_simulador()
    elif st.session_state['pantalla'] == 'ingenieria': vista_ingenieria()
def vista_diagnostico():
    st.header("🔬 Laboratorio de Análisis de Fallas")
    st.write("Identifique la causa raíz de la rotura para optimizar la frecuencia de intervención.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://via.placeholder.com/400x300.png?text=Imagen+de+Varilla+Cortada", caption="Muestra recuperada del pozo")
    
    with col2:
        opcion = st.radio("¿Qué tipo de falla observa?", 
                          ["Fatiga por Ciclos", "Corrosión por CO2/H2S", "Desgaste por Rozamiento", "Corte por Sobre-tensión"])
        
        if st.button("Registrar Diagnóstico"):
            if opcion == "Fatiga por Ciclos":
                st.success("Correcto. Se recomienda revisar el diseño de la sarta o el balance del A.I.B.")
            else:
                st.warning("El patrón indica fatiga. Revise los registros de torque de la última intervención.")

    st.markdown("""
    > **Nota Técnica:** El diagnóstico correcto permite alcanzar la meta de **2 años de operatividad**, reduciendo el 30% del OPEX mencionado en los manuales de MENFA.
    """)
