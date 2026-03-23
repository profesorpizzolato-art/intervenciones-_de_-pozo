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
