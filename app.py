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
