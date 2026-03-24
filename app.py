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
import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="MENFA - Simulador de Pesca Pro", layout="wide")

# 2. LÓGICA DE NAVEGACIÓN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {}

# --- MÓDULO DE PESCA Y GRÁFICOS ---
def vista_pesca_grafica():
    st.header("🎣 Módulo de Pesca y Análisis de Tensiones")
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()

    col_cfg, col_graf = st.columns([1, 2])

    with col_cfg:
        st.subheader("Configuración de Pesca")
        tipo_rotura = st.selectbox("Tipo de rotura detectada:", 
                                  ["Varilla Cortada (Cuerpo)", "Cuello de Bomba", "Bomba Aprisionada"])
        
        herramienta = st.radio("Seleccione Herramienta de Captura:", 
                               ["Overshot (Captura Exterior)", "Sucker Rod Socket", "Pescador de Cuello"])
        
        st.info("**Nota Técnica:** Según API 11B, el Overshot es preferible para varillas lisas, mientras que el Socket se utiliza para capturar cuellos de varilla.")

        # Simulación de Tensión
        tension_max = st.slider("Tensión aplicada (lbs)", 0, 100000, 45000)
        limite_fluencia = 85000 # Límite para Grado K
        
        if tension_max > limite_fluencia:
            st.error("🚨 ¡PELIGRO! Superó el límite de fluencia. Riesgo de corte de herramienta.")
        elif tension_max > limite_fluencia * 0.8:
            st.warning("⚠️ Precaución: Operando al 80% de la capacidad del material.")

    with col_graf:
        st.subheader("Gráfico de Tensión en Tiempo Real (Martin Decker)")
        # Generar datos simulados para el gráfico
        puntos = 20
        datos_y = np.linspace(0, tension_max, puntos) + np.random.normal(0, 1000, puntos)
        chart_data = pd.DataFrame({"Tiempo (min)": range(puntos), "Tensión (lbs)": datos_y})
        
        st.line_chart(chart_data, x="Tiempo (min)", y="Tensión (lbs)")
        
        st.markdown(f"""
        **Análisis de la Maniobra:**
        * **Peso de la sarta:** {tension_max * 0.7:.0f} lbs (Estimado)
        * **Punto de Pesca:** Detectado a {(tension_max/1.65):.0f} metros aprox.
        * **Estado:** {"En tensión de pesca" if tension_max > 40000 else "Buscando pescado"}
        """)

# --- DASHBOARD ACTUALIZADO CON MÓDULO DE PESCA ---
def dashboard_menfa():
    # ... (Mantenemos el header anterior)
    st.title("Panel de Control de Operaciones")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div style="border:1px solid #ddd; padding:10px;"><h4>📖 Manuales</h4><button>Ver</button></div>', unsafe_allow_html=True)
    with c2:
        if st.button("🏗️ Simulador"): 
            st.session_state['pantalla'] = 'simulador'; st.rerun()
    with c3:
        if st.button("🎣 Módulo de Pesca"): 
            st.session_state['pantalla'] = 'pesca'; st.rerun()
    with c4:
        if st.button("🧮 Ingeniería"): 
            st.session_state['pantalla'] = 'ingenieria'; st.rerun()

# --- LÓGICA DE RUTAS ---
if not st.session_state['auth']:
    # Lógica de registro...
    pass
else:
    if st.session_state['pantalla'] == 'dashboard': dashboard_menfa()
    elif st.session_state['pantalla'] == 'pesca': vista_pesca_grafica()
    # ... otras pantallas
    import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE ESCENARIO TÉCNICO
st.set_page_config(page_title="IPCL MENFA - Gestión de Intervenciones", layout="wide")

# Estilos CSS para apariencia de software industrial
st.markdown("""
    <style>
    .main { background-color: #f1f4f9; }
    .modulo-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        border-top: 6px solid #00457C; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #00457C;
        color: white; font-weight: bold; height: 3.5em;
    }
    .metric-box {
        background-color: #e9ecef; padding: 15px; border-radius: 10px;
        text-align: center; border: 1px solid #dee2e6;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONTROL DE SESIÓN Y NAVEGACIÓN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {}

# --- FUNCIONES DE SOPORTE ---
def header_app():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.write(f"🏢 **IPCL MENFA - Mendoza** | **Operador:** {st.session_state['user'].get('nombre')} | **Legajo:** {st.session_state['user'].get('dni')}")
    with c2:
        if st.button("Cerrar Sesión"):
            st.session_state['auth'] = False
            st.rerun()
    st.divider()

# --- PANTALLA: REGISTRO ---
def vista_registro():
    c1, c2, c3 = st.columns([1, 1.5, 1])
   with c2 as col2:
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+MENDOZA", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema de Operaciones</h2>", unsafe_allow_html=True)
        with st.form("login"):
            n = st.text_input("Nombre Completo")
            d = st.text_input("DNI / Legajo")
            r = st.selectbox("Rol Operativo", ["Instructor", "Jefe de Equipo", "Company Man", "Alumno"])
            if st.form_submit_button("Ingresar"):
                if n and d:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": n, "dni": d, "rol": r}
                    st.rerun()

# --- PANTALLA: DASHBOARD ---
def vista_dashboard():
    header_app()
    st.title("Panel de Control de Intervenciones")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="modulo-card"><h3>📖 Manual de Gestión</h3><p>Costos operativos (30% OPEX), optimización de frecuencias y fundamentos de pulling.</p></div>', unsafe_allow_html=True)
        if st.button("Manual Técnico"): st.session_state['pantalla'] = 'manual'; st.rerun()
    with col2:
        st.markdown('<div class="modulo-card"><h3>🏗️ Simulador de Pesca</h3><p>Ejecución de Worksteps para Vástago Cortado y Pesca de Varilla (Casos 1 y 2).</p></div>', unsafe_allow_html=True)
        if st.button("Simulador"): st.session_state['pantalla'] = 'simulador'; st.rerun()
    with col3:
        st.markdown('<div class="modulo-card"><h3>🧮 Ingeniería y Límites</h3><p>Cálculos API RP 59, tablas de varillas API 11B y análisis de fatiga de materiales.</p></div>', unsafe_allow_html=True)
        if st.button("Cálculos"): st.session_state['pantalla'] = 'ingenieria'; st.rerun()

# --- MÓDULO 1: MANUAL TÉCNICO DETALLADO ---
def pantalla_manual():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Manual de Procedimientos y Gestión de Producción")
    t1, t2 = st.tabs(["Economía de Operación", "Normativas Aplicables"])
    
    with t1:
        st.markdown("""
        ### Impacto en el OPEX
        En yacimientos profundos, las intervenciones representan el **30% del costo operativo total**. 
        **Meta MENFA:** Reducir la frecuencia a **1 intervención cada 2 años** en pozos estables.
        
        ### Definición Técnica
        Tarea de reparar o cambiar elementos mediante equipo de pulling o guinche apto para varillas y tubing.
        """)
    
    with t2:
        st.write("Lista de Estándares Críticos:")
        st.warning("- **API Spec 4F**: Estructuras de acero para perforación y pulling.\n- **API RP 4G**: Inspección y mantenimiento de mástiles.\n- **API 11B**: Especificaciones de varillas de bombeo.\n- **API RP 59**: Prácticas recomendadas para control de pozos.")

# --- MÓDULO 2: SIMULADOR DETALLADO ---
def pantalla_simulador():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Ejecución de Protocolos de Pesca")
    caso = st.radio("Seleccione Escenario:", ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla"], horizontal=True)
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Workstep de Campo")
        if "Vástago" in caso:
            pasos = ["Descomprimir columnas", "Check-list Jefe/Company", "Retirar cabeza de mula", "Pescar vástago", "Montar BOP", "Prueba de bloqueo"]
        else:
            pasos = ["Ahogar pozo (API RP 59)", "Retirar vástago", "Falta peso en Martin Decker (Verificar)", "Sacar en tiros dobles", "Bajar pescador", "Verificar anclaje"]
        
        for i, p in enumerate(pasos): st.checkbox(f"{i+1}. {p}", key=f"step_{i}")
        
    with c2:
        st.info("Monitor de Tensión")
        peso = st.slider("Carga (lbs)", 0, 100000, 45000, key="martin")
        if peso < 35000: st.error("⚠️ PESCA DETECTADA")
        else: st.success("✅ Columna Íntegra")

# --- MÓDULO 3: INGENIERÍA Y FATIGA ---
def pantalla_ingenieria():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.header("Ingeniería de Control y Límites de Material")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Control de Pozos (API RP 59)")
        prof = st.number_input("Profundidad (m)", value=1200)
        p_res = st.number_input("Presión Reservorio (PSI)", value=1500)
        margen = st.number_input("Margen de Seguridad (PSI)", value=200)
        
        densidad = (p_res + margen) / ((prof * 3.28) * 0.052)
        st.metric("Densidad de Ahogo Requerida", f"{densidad:.2f} ppg")

    with col_b:
        st.subheader("Resistencia de Varillas (API 11B)")
        grado = st.selectbox("Seleccione Grado:", ["Grado D", "Grado K", "Grado KD"])
        limites = {"Grado D": 115000, "Grado K": 85000, "Grado KD": 115000}
        
        st.write(f"Resistencia a la tracción: **{limites[grado]} PSI**")
        esfuerzo = st.progress(60, text="Esfuerzo actual (60%)")
        st.caption("No superar el 80% de la carga de fluencia durante la pesca.")

# --- NAVEGACIÓN ---
if not st.session_state['auth']:
    vista_registro()
else:
    if st.session_state['pantalla'] == 'dashboard': vista_dashboard()
    elif st.session_state['pantalla'] == 'manual': pantalla_manual()
    elif st.session_state['pantalla'] == 'simulador': pantalla_simulador()
    elif st.session_state['pantalla'] == 'ingenieria': pantalla_ingenieria()
import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. CONFIGURACIÓN Y ESTILO INDUSTRIAL
st.set_page_config(page_title="MENFA - Simulador de Pesca e Integridad", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .card {
        background-color: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #00457C; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. GESTIÓN DE SESIÓN
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {}

# --- VISTA: ANÁLISIS DE FALLAS Y PESCA ---
def vista_pesca_avanzada():
    st.title("🎣 Centro de Operaciones de Pesca")
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()

    tab_diag, tab_sim = st.tabs(["🔬 Diagnóstico de Falla", "📈 Simulación de Tensión"])

    with tab_diag:
        st.subheader("Identificación de Causa Raíz (RCA)")
        c1, c2 = st.columns(2)
        with c1:
            st.info("Analice la imagen del 'pescado' recuperado:")
            # Aquí simulas la imagen de la falla
            st.image("https://via.placeholder.com/500x300.png?text=Muestra+de+Falla+en+Varilla", use_container_width=True)
        with c2:
            falla = st.radio("¿Qué tipo de rotura observa?", 
                            ["Fatiga (Corte plano)", "Corrosión (Pitting)", "Sobre-tensión (Copa y Cono)", "Desgaste por Fricción"])
            if st.button("Confirmar Diagnóstico"):
                if falla == "Fatiga (Corte plano)":
                    st.success("Correcto. El 80% de las fallas en Mendoza son por fatiga. Revise el diseño de la sarta.")
                else:
                    st.error("Diagnóstico incorrecto. Observe el patrón de la rotura.")

    with tab_sim:
        st.subheader("Simulación de Captura y Tensión (Martin Decker)")
        
        # Parámetros de la Varilla (API 11B)
        grado = st.selectbox("Grado de la herramienta de pesca:", ["Grado D", "Grado K", "Grado KD"])
        limites = {"Grado D": 115000, "Grado K": 85000, "Grado KD": 115000}
        max_load = limites[grado]

        col_ctrl, col_graph = st.columns([1, 2])
        
        with col_ctrl:
            st.write(f"**Límite de Fluencia:** {max_load} lbs")
            tension = st.slider("Tensión aplicada (lbs)", 0, int(max_load * 1.2), 40000)
            
            # Lógica de seguridad
            if tension > max_load:
                st.error("🚨 ¡ROTURA! Se ha cortado la herramienta de pesca.")
            elif tension > max_load * 0.8:
                st.warning("⚠️ ZONA CRÍTICA: Deformación permanente probable.")
            else:
                st.success("✅ Operación Segura")

        with col_graph:
            # Gráfico dinámico de esfuerzo
            puntos = 15
            noise = np.random.normal(0, 800, puntos)
            data_y = np.linspace(35000, tension, puntos) + noise
            df_graph = pd.DataFrame({"Tiempo": range(puntos), "Tensión (lbs)": data_y})
            
            st.line_chart(df_graph, x="Tiempo", y="Tensión (lbs)")
            st.caption("Gráfico de tensión vs tiempo durante el desclavado de la bomba.")

# --- DASHBOARD PRINCIPAL ---
def dashboard_profesional():
    st.title(f"🚀 Plataforma MENFA | Operador: {st.session_state['user'].get('nombre')}")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card"><h3>📋 Manual de Procedimientos</h3><p>Costos operativos, frecuencias y normativas API.</p></div>', unsafe_allow_html=True)
        if st.button("Ver Documentación"): st.session_state['pantalla'] = 'manual'; st.rerun()

    with col2:
        st.markdown('<div class="card"><h3>🏗️ Simulador de Pulling</h3><p>Programas de pozo: Vástago y Varilla (Casos 1 y 2).</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Simulador"): st.session_state['pantalla'] = 'simulador'; st.rerun()

    with col3:
        st.markdown('<div class="card"><h3>🎣 Módulo de Pesca</h3><p>Análisis de fallas, captura y límites de fluencia con gráficos.</p></div>', unsafe_allow_html=True)
        if st.button("Iniciar Pesca"): st.session_state['pantalla'] = 'pesca'; st.rerun()

# --- NAVEGACIÓN ---
if not st.session_state['auth']:
    # Aquí iría tu función de registro (login_registro)
    st.title("Registro MENFA")
    nombre = st.text_input("Nombre")
    dni = st.text_input("DNI")
    if st.button("Ingresar"):
        st.session_state['auth'] = True
        st.session_state['user'] = {"nombre": nombre, "dni": dni}
        st.rerun()
else:
    if st.session_state['pantalla'] == 'dashboard': dashboard_profesional()
    elif st.session_state['pantalla'] == 'pesca': vista_pesca_avanzada()
    # Agregar las otras pantallas (manual, simulador, ingenieria) siguiendo el mismo patrón
