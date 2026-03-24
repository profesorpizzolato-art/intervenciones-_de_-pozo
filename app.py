import streamlit as st
import pandas as pd
import numpy as np
import random
BLOQUE 1: Lógica de Control de Eventos (Al inicio, debajo de las importaciones)
Python
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
BLOQUE 2: Interfaz de Punto Libre (Para reemplazar o añadir a vista_ingenieria())
Python
def vista_ingenieria_punto_libre():
    """Módulo para calcular la profundidad del atrapamiento (Stretch Method)."""
    header_app() # Tu función de encabezado institucional
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()
    
    st.markdown('<div class="modulo-header"><h2>🧮 Ingeniería de Pesca: Cálculo de Punto Libre</h2></div>', unsafe_allow_html=True)
    
    st.write("Si la sarta está atrapada por formación o arena, determine la profundidad del agarre (Punto Libre) antes de cortar.")
    
    col_input, col_res = st.columns(2)
    
    with col_input:
        st.subheader("Datos de Campo (API RP 11BR)")
        diametro = st.selectbox("Diámetro de Varilla (pulg):", ["3/4", "7/8", "1"])
        
        c1, c2 = st.columns(2)
        p1 = c1.number_input("Tensión Base (F1) (lbs)", value=20000, step=1000)
        p2 = c2.number_input("Tensión de Tracción (F2) (lbs)", value=40000, step=1000)
        
        estiramiento = st.number_input("Estiramiento Observado (∆L) (pulgadas)", value=12.0)
        
        # Constantes elásticas simplificadas (basadas en E=30x10^6 psi)
        constantes_elasticas = {"3/4": 0.75, "7/8": 0.88, "1": 1.12}
        
    with col_res:
        st.subheader("Resultado del Análisis")
        diff_tension = p2 - p1
        
        if diff_tension > 0:
            # Fórmula de Punto Libre para profundidad en metros
            prof_libre = (estiramiento * constantes_elasticas[diametro] * 1000000) / diff_tension
            st.metric("Profundidad de Atrapamiento Estimada", f"{prof_libre:.0f} metros")
            
            # Validación con el pozo seleccionado
            if st.session_state['pozo_seleccionado']:
                prof_bomba = st.session_state['pozo_seleccionado']['Profundidad (m)']
                if prof_libre < prof_bomba * 0.85:
                    st.error(f"¡Atención! El agarre está a {prof_bomba - prof_libre:.0f}m arriba de la bomba. Posible colapso de tubing o arenamiento masivo.")
                else:
                    st.success("El agarre es cerca de la bomba. Proceda con maniobra de desclave.")
        else:
            st.warning("Ingrese una tensión F2 mayor que F1.")
BLOQUE 3: Interfaz de Pesca con Contingencias (Para reemplazar vista_pesca_pro())
Python
def vista_pesca_con_contingencias():
    """Simulador de Pesca con botón de avance que dispara imprevistos operativos."""
    header_app()
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()
    
    if not st.session_state['pozo_seleccionado']:
        st.warning("⚠️ Primero debe seleccionar un pozo en el módulo de 'Legajo'.")
        return

    datos = st.session_state['pozo_seleccionado']
    st.markdown(f'<div class="modulo-header"><h2>Operación de Pesca: {datos["Pozo"]}</h2></div>', unsafe_allow_html=True)

    # --- ZONA DE EVENTOS ALEATORIOS ---
    col1_ev, col2_ev = st.columns([1, 3])
    with col1_ev:
        # BOTÓN CRÍTICO: Simula el avance del tiempo en la maniobra
        st.subheader("Tiempo Operativo")
        if st.button("⏯️ Avanzar Maniobra"):
            # Importante: Importa random dentro si no lo hiciste arriba
            import random 
            generar_contingencia()

    with col2_ev:
        # Muestra el evento si existe
        if st.session_state['evento_activo']:
            ev = st.session_state['evento_activo']
            if ev['tipo'] == "error": st.error(f"{ev['icono']} {ev['msg']}")
            elif ev['tipo'] == "warning": st.warning(f"{ev['icono']} {ev['msg']}")
            elif ev['tipo'] == "info": st.info(f"{ev['icono']} {ev['msg']}")
            else: st.success(f"{ev['icono']} {ev['msg']}")
    st.divider()

    # --- ZONA DE SIMULACIÓN GRÁFICA (Mantenemos tu slider y gráfico) ---
    t1, t2 = st.tabs(["📊 Monitor Martin Decker", "📋 Workstep"])
    
    with t1:
        # Parámetros de resistencia basados en el pozo
        limites_fluencia = {"Grado D": 115000, "Grado K": 85000, "Grado KD": 115000}
        max_load = limites_fluencia[datos['Grado Varilla']]
        
        col_slider, col_chart = st.columns([1, 2])
        with col_slider:
            st.write(f"**Límite Fluencia ({datos['Grado Varilla']}):** {max_load} lbs")
            # Slider de tensión que llega al 130% del límite
            tension = st.slider("Tensión Aplicada (lbs)", 0, int(max_load*1.3), 35000, step=1000, key="martin_slider")
            
            # Lógica técnica de castigo/alerta
            if tension > max_load:
                st.error(f"🚨 ¡ROTURA! Se ha cortado la herramienta de pesca por sobre-tensión (Superó {max_load} lbs). Operación fallida.")
            elif tension > max_load * 0.85:
                st.warning("⚠️ LÍMITE ELÁSTICO ALCANZADO. Deformación permanente probable.")
        
        with col_chart:
            # Gráfico dinámico de esfuerzo
            puntos = 15
            # Generamos datos con ruido simulando movimiento real
            noise = np.random.normal(0, 1000, puntos)
            data_y = np.linspace(25000, tension, puntos) + noise
            chart_data = pd.DataFrame({"Tiempo": range(puntos), "Tensión (lbs)": data_y})
            st.line_chart(chart_data, x="Tiempo", y="Tensión (lbs)")
    
    with t2:
        # Workstep basado en el historial del pozo
        st.subheader("Protocolo Operativo Sugerido")
        if "Corrosión" in datos['Historial Falla']:
            pasos = ["Ahogo de pozo (API RP 59)", "Revisar tubing por posibles pinchaduras", "Bajar pescador tipo 'Socket'", "Sacar varillas con precaución por fragilidad."]
        else:
            pasos = ["Ahogo de pozo", "Constatar falta de peso con Martin Decker", "Sacar varillas en tiros dobles revisando torque.", "Bajar pescador tipo 'Overshot'."]
        for i, p in enumerate(pasos): st.checkbox(f"{i+1}. {p}", key=f"step_{i}"
