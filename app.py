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
