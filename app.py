import streamlit as st
import pandas as pd

# Configuración de la página al estilo IPCL MENFA
st.set_page_config(page_title="Simulador de Intervención - MENFA", layout="wide")

def main():
    st.title("🏗️ Simulador de Pulling y Pesca de Varillas")
    st.sidebar.image("https://via.placeholder.com/150?text=MENFA+Mendoza", width=150) # Espacio para tu logo
    st.sidebar.markdown("### Configuración de Operación")

    # --- SIDEBAR: Parámetros del Pozo ---
    tipo_operacion = st.sidebar.selectbox(
        "Seleccione el Caso de Pesca:",
        ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla de Bombeo"]
    )
    
    profundidad_fallo = st.sidebar.number_input("Profundidad del fallo (m)", value=1200, step=50)
    peso_nominal_columna = st.sidebar.number_input("Peso nominal de columna (lbs)", value=45000, step=1000)

    # --- CUERPO PRINCIPAL ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header(f"Procedimiento Operativo: {tipo_operacion}")
        
        if tipo_operacion == "1er Caso: Vástago Cortado":
            steps = [
                "Verificar estado de boca de pozo y descompresar.",
                "Montar equipo y realizar charla de seguridad/Checklist.",
                "Retirar cabeza de mula (A.I.B.).",
                "Bajar pescador y realizar pesca de vástago.",
                "Montar BOP de varillas y verificar peso total.",
                "Clavar bomba y realizar prueba de hermeticidad/bloqueo."
            ]
        else:
            steps = [
                "Ahogar pozo y montar equipo.",
                "Tomar medida de enganche y retirar vástago.",
                "Extraer varillas en TIROS DOBLES revisando material.",
                "Bajar pescador (probar si es positiva/negativa).",
                "Verificar anclaje de bomba y probar hermeticidad de cañería."
            ]

        for i, step in enumerate(steps, 1):
            st.checkbox(f"{i}. {step}", key=f"step_{i}")

    with col2:
        st.info("📊 **Monitor de Cargas (Martin Decker)**")
        # Simulación de peso real vs nominal
        peso_actual = st.slider("Lectura de peso actual (lbs)", 0, 100000, int(peso_nominal_columna * 0.6))
        
        diferencia = peso_actual - peso_nominal_columna
        
        if peso_actual < peso_nominal_columna * 0.9:
            st.warning(f"⚠️ ¡PESCA VERIFICADA! Falta peso: {abs(diferencia)} lbs.")
        else:
            st.success("✅ Peso de columna completo.")

        st.divider()
        st.markdown("### Normativa Aplicable")
        st.caption("Seguridad bajo normas API Spec 4F y API 11B.")

    # --- SECCIÓN TÉCNICA: Cuestionario Dinámico ---
    st.divider()
    st.subheader("📝 Evaluación de Maniobra")
    pregunta = st.radio(
        "Según la Clase 11: ¿Cuál es el objetivo de frecuencia de intervención en yacimientos estables?",
        ["Una vez por año", "Una vez cada 2 años", "Cada 6 meses"]
    )
    
    if st.button("Validar Respuesta"):
        if pregunta == "Una vez cada 2 años":
            st.balloons()
            st.success("Correcto. El objetivo es optimizar para bajar costos operativos.")
        else:
            st.error("Incorrecto. Repase el material de la Clase 11.")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Simulador de Intervención - IPCL MENFA", layout="wide")

def main():
    st.title("🏗️ Simulador de Pulling y Pesca de Varillas - MENFA")
    
    # --- BARRA LATERAL ---
    st.sidebar.header("Configuración de Operación")
    tipo_operacion = st.sidebar.selectbox(
        "Seleccione el Caso de Pesca:",
        ["1er Caso: Vástago Cortado", "2do Caso: Pesca de Varilla de Bombeo"]
    )
    
    profundidad_m = st.sidebar.number_input("Profundidad del pozo (m)", value=1500, step=100)
    presion_reservorio_psi = st.sidebar.number_input("Presión de Reservorio (PSI)", value=1800, step=50)

    # --- PESTAÑAS PARA ORGANIZAR EL CONTENIDO ---
    tab1, tab2, tab3 = st.tabs(["📋 Guía Operativa", "🧮 Cálculos de Ahogo", "📝 Evaluación"])

    # --- TAB 1: GUÍA OPERATIVA ---
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"Programa de Pozo: {tipo_operacion}")
            if tipo_operacion == "1er Caso: Vástago Cortado":
                steps = [
                    "Verificar estado de boca de pozo y descompresar a pileta.",
                    "Realizar charla de seguridad y Check-list del equipo.",
                    "Retirar cabeza de mula y desarmar puente de producción.",
                    "Bajar pescador y realizar pesca de vástago.",
                    "Montar BOP de varillas y verificar peso con Martin Decker.",
                    "Probar hermeticidad y funcionamiento con prueba de bloqueo."
                ]
            else:
                steps = [
                    "Verificar estado de boca de pozo y ahogar si es necesario.",
                    "Montar equipo y realizar Check-list.",
                    "Retirar vástago de bombeo y colocar v/b de maniobra.",
                    "Constatar falta de peso (Pesca verificada).",
                    "Sacar varillas en TIROS DOBLES revisando material.",
                    "Bajar pescador y verificar si la pesca es positiva.",
                    "Probar hermeticidad de la cañería de producción."
                ]

            for i, step in enumerate(steps, 1):
                st.checkbox(f"{i}. {step}", key=f"step_{i}")

        with col2:
            st.info("📊 **Monitor Martin Decker**")
            peso_nominal = 45000 # lbs (según Clase 11)
            peso_actual = st.slider("Lectura de peso (lbs)", 0, 60000, 25000)
            
            if peso_actual < peso_nominal * 0.8:
                st.error(f"⚠️ ¡PESCA VERIFICADA! Peso insuficiente.")
            else:
                st.success("✅ Peso de columna normal.")

    # --- TAB 2: CÁLCULOS DE AHOGO (NUEVA SECCIÓN) ---
    with tab2:
        st.subheader("Calculadora de Control de Pozo (Well Control)")
        st.write("Determine la densidad del fluido necesaria para neutralizar la presión del reservorio.")
        
        c1, c2 = st.columns(2)
        with c1:
            margen_seguridad = st.number_input("Margen de seguridad (PSI)", value=200)
            presion_objetivo = presion_reservorio_psi + margen_seguridad
            
            # Cálculo de densidad (ppg) -> Densidad = Presión / (Profundidad_ft * 0.052)
            # Convertimos profundidad m a ft
            prof_ft = profundidad_m * 3.28084
            densidad_req = presion_objetivo / (prof_ft * 0.052)
            
            st.metric("Densidad de Ahogo Requerida", f"{densidad_req:.2f} ppg")
        
        with c2:
            st.help("Fórmula aplicada: $D = P / (h \\times 0.052)$")
            st.markdown(f"""
            **Resumen de Control:**
            - Profundidad: {prof_ft:.0f} ft
            - Presión a vencer: {presion_objetivo} PSI
            - Norma aplicable: **API RP 59**
            """)

    # --- TAB 3: EVALUACIÓN ---
    with tab3:
        st.subheader("Cuestionario de Repaso - Clase 11")
        q1 = st.radio("¿Cuál es el costo operativo aproximado de las intervenciones en yacimientos profundos?", 
                      ["10%", "30%", "50%"])
        
        if st.button("Enviar Respuesta"):
            if q1 == "30%":
                st.success("¡Correcto! Es un costo significativo para la operadora.")
            else:
                st.error("Incorrecto. Revise el texto de la Clase 11.")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd

# Configuración de la interfaz
st.set_page_config(page_title="Simulador MENFA - Pulling & Pesca", layout="wide")

def main():
    st.title("🏗️ Sistema de Simulación de Intervención - MENFA")
    st.markdown("---")

    # --- PANEL LATERAL: DATOS DEL POZO ---
    st.sidebar.header("📥 Parámetros del Pozo")
    profundidad_m = st.sidebar.number_input("Profundidad (m)", value=1500, min_value=100)
    presion_res_psi = st.sidebar.number_input("Presión de Reservorio (PSI)", value=1800)
    
    # Datos de cañería para cálculos de volumen
    diametro_csg = st.sidebar.selectbox("Diámetro CSG (pulg)", [5.5, 7.0, 9.625])
    
    # --- PESTAÑAS PRINCIPALES ---
    tab1, tab2, tab3 = st.tabs(["📋 Programas de Pozo", "🧮 Cálculos de Ingeniería", "🎓 Evaluación Técnica"])

    # --- PESTAÑA 1: PROGRAMAS OPERATIVOS ---
    with tab1:
        tipo_caso = st.radio("Seleccione la maniobra:", ["Vástago Cortado", "Pesca de Varillas"])
        
        col_pro, col_mon = st.columns([2, 1])
        
        with col_pro:
            st.subheader(f"Pasos Operativos - {tipo_caso}")
            if tipo_caso == "Vástago Cortado":
                pasos = [
                    "Verificar presión entre columnas y descomprimir.",
                    "Montar equipo y realizar Check-list (Jefe de Equipo + Company).",
                    "Retirar cabeza de mula y desplazar a un costado.",
                    "Bajar pescador y realizar captura de vástago.",
                    "Montar BOP de varillas y verificar peso en Martin Decker.",
                    "Clavar bomba y realizar prueba de hermeticidad."
                ]
            else:
                pasos = [
                    "Ahogar pozo (según cálculos en Tab 2).",
                    "Retirar vástago y colocar v/b de maniobra.",
                    "Constatar falta de peso (Pesca verificada).",
                    "Extraer varillas en TIROS DOBLES revisando material.",
                    "Bajar pescador y verificar si la pesca es positiva.",
                    "Probar hermeticidad de la cañería de producción."
                ]
            
            for p in pasos:
                st.checkbox(p)

        with col_mon:
            st.info("⚡ **Indicador Martin Decker**")
            # Simulación de pérdida de peso en pesca de varillas
            peso_ref = 45000 # lbs (Referencia Clase 11)
            peso_sim = st.slider("Lectura Real (lbs)", 0, 60000, 45000)
            
            if peso_sim < peso_ref * 0.85:
                st.error("⚠️ ALERTA: FALTA DE PESO. Pesca Verificada.")
            else:
                st.success("✅ Peso de columna íntegro.")

    # --- PESTAÑA 2: CÁLCULOS DE INGENIERÍA (AHOGO) ---
    with tab2:
        st.subheader("🧮 Ingeniería de Control de Pozos (Well Control)")
        
        c1, c2, c3 = st.columns(3)
        
        # 1. Cálculo de Densidad de Ahogo
        with c1:
            st.markdown("**1. Densidad de Fluido**")
            margen = st.number_input("Margen de Seguridad (PSI)", value=200)
            p_total = presion_res_psi + margen
            prof_ft = profundidad_m * 3.2808
            # Fórmula: Densidad = Presión / (Profundidad_ft * 0.052)
            densidad_ppg = p_total / (prof_ft * 0.052)
            st.metric("Densidad Requerida", f"{densidad_ppg:.2f} ppg")
            st.caption("Fórmula: $P / (h \times 0.052)$")

        # 2. Cálculo de Presión Hidrostática Actual
        with c2:
            st.markdown("**2. Hidrostática Actual**")
            densidad_actual = st.number_input("Densidad actual del fluido (ppg)", value=8.33)
            p_hidro = densidad_actual * 0.052 * prof_ft
            st.metric("Presión Hidrostática", f"{p_hidro:.0f} PSI")
            
            balance = p_hidro - presion_res_psi
            if balance < 0:
                st.warning(f"Bajo balance: {abs(balance):.0f} PSI")
            else:
                st.success(f"Sobrebalance: {balance:.0f} PSI")

        # 3. Cálculo de Volumen de Ahogo
        with c3:
            st.markdown("**3. Volumen del Pozo**")
            # Factor de capacidad simplificado (bbl/m)
            capacidad = (diametro_csg**2) / 314  # Galones/pie aprox convertido
            vol_total = capacidad * profundidad_m
            st.metric("Volumen Estimado", f"{vol_total:.1f} bbl")
            st.caption("Basado en diámetro de CSG y profundidad.")

    # --- PESTAÑA 3: EVALUACIÓN ---
    with tab3:
        st.subheader("📝 Validación de Conocimientos")
        q = st.radio("¿Qué norma API regula la inspección y mantenimiento del mástil del equipo de Pulling?",
                    ["API 11B", "API RP 4G", "API Spec 9A"])
        
        if st.button("Validar"):
            if q == "API RP 4G":
                st.balloons()
                st.success("¡Correcto! Es la norma clave para el Check-list de seguridad.")
            else:
                st.error("Incorrecto. API RP 4G es para inspección de estructuras.")

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import numpy as np

# Configuración profesional
st.set_page_config(page_title="Simulador Técnico - IPCL MENFA", layout="wide")

def main():
    st.title("🏗️ Simulador Avanzado de Pulling y Pesca - MENFA")
    st.markdown("---")

    # --- DATOS DE REFERENCIA (API 11B) ---
    datos_varillas = {
        "Grado D (Acero Carbono)": {"peso_lb_ft": 1.64, "resistencia_psi": 115000},
        "Grado K (Corrosión Moderada)": {"peso_lb_ft": 1.63, "resistencia_psi": 85000},
        "Grado KD (Aleación Especial)": {"peso_lb_ft": 1.65, "resistencia_psi": 115000},
        "Varilla de Fibra de Vidrio": {"peso_lb_ft": 0.65, "resistencia_psi": 100000}
    }

    # --- SIDEBAR: CONFIGURACIÓN ---
    st.sidebar.header("⚙️ Configuración del Pozo")
    tipo_varilla = st.sidebar.selectbox("Tipo de Varilla (API 11B):", list(datos_varillas.keys()))
    profundidad_m = st.sidebar.number_input("Profundidad de la Bomba (m)", value=1200)
    
    # Cálculo automático de peso teórico
    peso_u = datos_varillas[tipo_varilla]["peso_lb_ft"]
    prof_ft = profundidad_m * 3.2808
    peso_teorico_total = peso_u * prof_ft

    # --- PESTAÑAS ---
    tab1, tab2, tab3 = st.tabs(["📊 Monitor de Cargas", "🧮 Ingeniería de Ahogo", "📋 Programas API"])

    # --- TAB 1: MONITOR DE CARGAS Y GRÁFICOS ---
    with tab1:
        st.subheader("Visualización del Martin Decker")
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.metric("Peso Teórico en Aire", f"{peso_teorico_total:.0f} lbs")
            peso_real = st.slider("Lectura del Indicador (lbs)", 0, int(peso_teorico_total * 1.2), int(peso_teorico_total * 0.5))
            
            diferencial = peso_teorico_total - peso_real
            if diferencial > (peso_teorico_total * 0.15):
                st.error(f"⚠️ PESCA DETECTADA: Faltan {diferencial:.0f} lbs")
            else:
                st.success("✅ Columna Íntegra")

        with c2:
            # Gráfico de comportamiento de carga
            st.write("**Gráfico de Tensión en la Maniobra**")
            chart_data = pd.DataFrame({
                "Tensión": [0, peso_real * 0.5, peso_real, peso_real * 1.1],
                "Tiempo (min)": [0, 5, 10, 15]
            })
            st.line_chart(chart_data, x="Tiempo (min)", y="Tensión")

    # --- TAB 2: CÁLCULOS DE AHOGO ---
    with tab2:
        st.subheader("Cálculos de Control de Pozo (API RP 59)")
        col_a, col_b = st.columns(2)
        
        with col_a:
            presion_res = st.number_input("Presión de Reservorio (PSI)", value=1500)
            overbalance = st.number_input("Margen de Seguridad (PSI)", value=200)
            densidad_req = (presion_res + overbalance) / (prof_ft * 0.052)
            st.metric("Densidad de Ahogo", f"{densidad_req:.2f} ppg")
            
        with col_b:
            st.info("""
            **Resistencia de Materiales:**
            - Límite Elástico: {0} PSI
            - No exceder el 80% de la carga de fluencia durante la pesca.
            """.format(datos_varillas[tipo_varilla]["resistencia_psi"]))

    # --- TAB 3: PROGRAMAS API ---
    with tab3:
        st.subheader("Checklist de Procedimiento")
        op = st.radio("Maniobra:", ["1er Caso: Vástago", "2do Caso: Varillas"])
        
        if op == "1er Caso: Vástago":
            pasos = ["Descomprimir columnas", "Retirar cabeza de mula", "Capturar vástago", "Montar BOP"]
        else:
            pasos = ["Ahogar pozo", "Retirar vástago", "Sacar en tiros dobles", "Bajar pescador"]
            
        for p in pasos:
            st.checkbox(p)

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Simulador MENFA - Acceso Restringido", layout="wide")

# 2. SISTEMA DE REGISTRO / LOGIN
def login_modulo():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #00457C;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # LOGO MENFA (Reemplaza la URL por la de tu logo oficial)
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+-+MENDOZA", use_container_width=True)
        
        st.subheader("🔐 Registro de Instructor / Alumno")
        with st.form("login_form"):
            nombre = st.text_input("Nombre Completo")
            legajo = st.text_input("Legajo o DNI")
            rol = st.selectbox("Rol", ["Alumno", "Instructor", "Supervisor (Company)"])
            
            submit = st.form_submit_button("Ingresar al Simulador")
            
            if submit:
                if nombre and legajo:
                    st.session_state['autenticado'] = True
                    st.session_state['usuario'] = nombre
                    st.session_state['rol'] = rol
                    st.rerun()
                else:
                    st.error("Por favor, complete todos los campos para el registro.")

# 3. CONTENIDO DEL SIMULADOR (Solo si está autenticado)
def mostrar_simulador():
    # Encabezado con logo pequeño y usuario
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title(f"🏗️ Simulador de Intervención")
        st.caption(f"Operando como: {st.session_state['usuario']} ({st.session_state['rol']})")
    with c2:
        if st.button("Cerrar Sesión"):
            st.session_state['autenticado'] = False
            st.rerun()

    st.divider()

    # --- DATOS DE REFERENCIA (API 11B) ---
    datos_varillas = {
        "Grado D (API 11B)": {"peso_lb_ft": 1.64, "resistencia": 115000},
        "Grado KD (Aleación)": {"peso_lb_ft": 1.65, "resistencia": 115000}
    }

    # --- ESTRUCTURA DE PESTAÑAS ---
    t1, t2 = st.tabs(["📊 Operación en Vivo", "🧮 Ingeniería de Ahogo"])

    with t1:
        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Procedimiento de Pesca")
            tipo = st.radio("Seleccione el Caso:", ["Vástago Cortado", "Pesca de Varilla"])
            
            # Lógica simplificada de pasos basada en tus archivos
            pasos = ["Charla de Seguridad", "Check-list API RP 4G", "Descomprimir Columnas"]
            if tipo == "Pesca de Varilla":
                pasos.append("Ahogar pozo (API RP 59)")
            
            for p in pasos:
                st.checkbox(p)
        
        with col_b:
            st.info("Monitor Martin Decker")
            peso_real = st.slider("Carga en el Gancho (lbs)", 0, 60000, 45000)
            if peso_real < 35000:
                st.error("⚠️ PESCA DETECTADA")
            else:
                st.success("✅ Columna Íntegra")

    with t2:
        st.subheader("Cálculos de Control (Well Control)")
        p_res = st.number_input("Presión de Reservorio (PSI)", value=1800)
        st.write(f"Cálculo de densidad requerida según profundidad y presión...")

# --- FLUJO PRINCIPAL ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    login_modulo()
else:
    mostrar_simulador()
