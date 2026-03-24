import streamlit as st
import pandas as pd
import numpy as np
import random
import streamlit as st
import pandas as pd
import numpy as np
import random

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL - IPCL MENFA MENDOZA
st.set_page_config(page_title="IPCL MENFA - Gestión Integral de Operaciones", layout="wide")

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

# 2. GESTIÓN DE ESTADOS Y BASE DE DATOS
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {}
if 'pozo_seleccionado' not in st.session_state: st.session_state['pozo_seleccionado'] = None
if 'evento_activo' not in st.session_state: st.session_state['evento_activo'] = None
if 'hse_ok' not in st.session_state: st.session_state['hse_ok'] = False
if 'ranking' not in st.session_state:
    st.session_state['ranking'] = pd.DataFrame([
        {"Operador": "Instructor Fabricio", "Puntaje": 5000, "Estado": "Excelente", "Pozo": "MENFA-101"}
    ])

# Base de Datos de Activos
data_pozos = pd.DataFrame({
    "Pozo": ["MENFA-101", "MENFA-102", "MENFA-105", "Puesto-Pozo-8"],
    "Profundidad (m)": [1200, 1550, 1800, 1400],
    "Grado Varilla": ["Grado D", "Grado K", "Grado KD", "Grado D"],
    "Presión Reservorio (PSI)": [1500, 1850, 2100, 1600],
    "Historial Falla": ["Fatiga por Ciclos", "Corrosión por CO2/H2S", "Desgaste por Rozamiento", "Corte por Sobre-tensión"]
})

# --- FUNCIONES DE APOYO ---
def header_app():
    c1, c2 = st.columns([4, 1])
    with c1:
        u = st.session_state['user']
        st.subheader(f"🏢 IPCL MENFA | Operador: {u.get('nombre')} | Rol: {u.get('rol')}")
    with c2:
        if st.button("Cerrar Sesión"):
            st.session_state['auth'] = False
            st.rerun()
    st.divider()

def generar_contingencia():
    eventos = [
        {"msg": "⚠️ ¡Pérdida de Circulación! El pozo absorbe fluido.", "tipo": "error", "icono": "🚱"},
        {"msg": "⚠️ ¡Fuga en Manguera! Detenga la bomba.", "tipo": "warning", "icono": "🧯"},
        {"msg": "⚠️ ¡Pescado con Arena! Tensión errática.", "tipo": "info", "icono": "⏳"},
        {"msg": "✅ Operación normal. Siga tensionando.", "tipo": "success", "icono": "👍"}
    ]
    st.session_state['evento_activo'] = random.choice(eventos)

# --- PANTALLAS ---

def vista_registro():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.image("https://via.placeholder.com/600x200.png?text=IPCL+MENFA+MENDOZA", use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema Técnico</h2>", unsafe_allow_html=True)
        with st.form("login"):
            n = st.text_input("Nombre Completo")
            d = st.text_input("DNI / Legajo")
            r = st.selectbox("Función", ["Instructor", "Jefe de Equipo", "Company Man", "Alumno"])
            if st.form_submit_button("Ingresar"):
                if n and d:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": n, "dni": d, "rol": r}
                    st.rerun()

def vista_dashboard():
    header_app()
    st.title("Panel de Control de Intervenciones")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="card-tecnica"><h3>📋 Gestión de Activos</h3><p>Legajos técnicos y datos de diseño de pozo.</p></div>', unsafe_allow_html=True)
        if st.button("Ver Legajos"): st.session_state['pantalla'] = 'legajo'; st.rerun()
    with c2:
        st.markdown('<div class="card-tecnica"><h3>🏗️ Simulador Pulling</h3><p>Operación de pesca con eventos en tiempo real.</p></div>', unsafe_allow_html=True)
        if st.button("Abrir Simulador"): st.session_state['pantalla'] = 'simulador'; st.rerun()
    with c3:
        st.markdown('<div class="card-tecnica"><h3>🏆 Ranking MENFA</h3><p>Cuadro de honor y eficiencia operativa.</p></div>', unsafe_allow_html=True)
        if st.button("Ver Ranking"): st.session_state['pantalla'] = 'ranking'; st.rerun()

    st.divider()
    ca, cb, cc = st.columns(3)
    with ca: 
        if st.button("🧮 Calculadora de Punto Libre"): st.session_state['pantalla'] = 'punto_libre'; st.rerun()
    with cb:
        if st.button("📖 Manual de Gestión (OPEX)"): st.session_state['pantalla'] = 'manual'; st.rerun()
    with cc:
        if st.button("🛡️ HSE y Seguridad"): st.session_state['pantalla'] = 'hse'; st.rerun()
    
    with cd: # O la columna que tengas libre
        if st.button("🔧 Herramientas / Torque"): st.session_state['pantalla'] = 'herramientas'; st.rerun()        
    with col_viz:
        st.write("**Esquema del Pozo**") graf_data = pd.DataFrame({'Tramo': ['Pozo'],'Libre (m)': [prof_m],'Atrapado (m)': [max(0, total_m - prof_m)]}).set_index('Tramo')
        st.bar_chart(graf_data, color=["#2ecc71", "#e74c3c"], width="stretch")
    with col_graph:
        y = np.linspace(25000, tension, 15) + np.random.normal(0, 1000, 15)
        # Actualizado para evitar el warning
        st.line_chart(y, width="stretch")
def vista_legajo():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Legajo Técnico de Pozos</h2></div>', unsafe_allow_html=True)
    pozo_sel = st.selectbox("Seleccione Activo:", data_pozos["Pozo"])
    detalles = data_pozos[data_pozos["Pozo"] == pozo_sel].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Profundidad", f"{detalles['Profundidad (m)']} m")
        st.metric("Grado API", detalles['Grado Varilla'])
    with col2:
        st.metric("P. Reservorio", f"{detalles['Presión Reservorio (PSI)']} PSI")
        st.info(f"Falla Histórica: {detalles['Historial Falla']}")
    
    if st.button("Cargar Datos al Simulador"):
        st.session_state['pozo_seleccionado'] = detalles.to_dict()
        st.success("Datos cargados.")

def vista_hse_seguridad():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>🛡️ Módulo de Seguridad (HSE)</h2></div>', unsafe_allow_html=True)
    
    st.subheader("Análisis de Trabajo Seguro (ATS)")
    c1, c2 = st.columns(2)
    with c1:
        s1 = st.checkbox("BOP instalada y probada")
        s2 = st.checkbox("Puesta a tierra de equipo")
        s3 = st.checkbox("EPP Completo")
    with c2:
        st.info("⚠️ El ATS es obligatorio antes de iniciar la pesca.")
        if s1 and s2 and s3:
            st.session_state['hse_ok'] = True
            st.success("ATS Aprobado.")
        else:
            st.session_state['hse_ok'] = False
            st.error("ATS Pendiente.")

def vista_simulador_operativo():
    header_app()
    if st.button("⬅️ Volver", key="btn_volver_sim"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()
    
    if not st.session_state.get('pozo_seleccionado') or not st.session_state.get('hse_ok'):
        st.warning("⚠️ Verifique: 1. Seleccionar Pozo en Legajos | 2. Completar ATS en Módulo HSE.")
        return

    datos = st.session_state['pozo_seleccionado']
    st.markdown(f'<div class="modulo-header"><h2>Pesca en Pozo: {datos["Pozo"]}</h2></div>', unsafe_allow_html=True)

    # CORRECCIÓN LÍNEA 214: Definimos 3 columnas para que 'with col3' funcione
    col1, col2, col3 = st.columns([2, 3, 3]) 
    
    with col1:
        st.subheader("Controles")
        if st.button("⏯️ Generar Evento"): 
            generar_contingencia()
        
        if st.session_state.get('evento_activo'):
            ev = st.session_state['evento_activo']
            st.info(f"{ev['icono']} {ev['msg']}")
        
        limites = {"Grado D": 115000, "Grado K": 85000, "Grado KD": 115000}
        limite_actual = limites.get(datos['Grado Varilla'], 100000)
        tension = st.slider("Tensión Aplicada (lbs)", 0, 150000, 40000)
        
        if tension > limite_actual: 
            st.error(f"🚨 SOBRETENSIÓN: Límite de {datos['Grado Varilla']} excedido")

    with col2:
        st.subheader("Indicador de Carga")
        # Simulación de tirones
        y = np.linspace(25000, tension, 15) + np.random.normal(0, 1500, 15)
        st.line_chart(y)

    with col3: # Ahora col3 existe correctamente
        st.subheader("Estado de Sarta")
        st.write(f"**Material:** {datos['Grado Varilla']}")
        st.write(f"**Profundidad:** {datos['Profundidad (m)']} m")
        
        if st.button("📝 Finalizar y Reportar"):
            puntos = 3000 if tension <= limite_actual else 500
            nuevo_registro = pd.DataFrame([{
                "Operador": st.session_state['user']['nombre'], 
                "Puntaje": puntos, 
                "Estado": "Finalizado", 
                "Pozo": datos['Pozo']
            }])
            # Unión de datos corregida
            st.session_state['ranking'] = pd.concat([st.session_state['ranking'], nuevo_registro], ignore_index=True)
            st.success("Operación reportada al Ranking.")


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
def vista_punto_libre():
    header_app()
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()
        
    st.markdown('<div class="modulo-header"><h2>🧮 Ingeniería: Cálculo de Punto Libre (Stretch)</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Datos de Entrada (API RP 11BR)")
        # Tabla de constantes de varillas de acero
        tabla_constantes = {
            "5/8\" (Et: 0.522)": 0.522,
            "3/4\" (Et: 0.751)": 0.751,
            "7/8\" (Et: 1.022)": 1.022,
            "1\" (Et: 1.336)": 1.336,
            "1 1/8\" (Et: 1.691)": 1.691
        }
        
        seleccion = st.selectbox("Diámetro de Varilla:", list(tabla_constantes.keys()))
        et_val = tabla_constantes[seleccion]
        
        p1 = st.number_input("Tensión Inicial $P_1$ (lbs)", value=10000, step=500)
        p2 = st.number_input("Tensión Final $P_2$ (lbs)", value=25000, step=500)
        estiramiento = st.number_input("Estiramiento Medido $E$ (pulgadas)", value=5.0, step=0.5)

    with col2:
        st.subheader("📊 Resultado del Análisis")
        delta_p = p2 - p1
        
        if delta_p > 0:
            # Cálculo: L (pies) = (E * Et * 1.000.000) / Delta P
            prof_pies = (estiramiento * et_val * 1000000) / delta_p
            prof_metros = prof_pies * 0.3048 # Conversión a metros
            
            st.metric("Punto de Atrapamiento", f"{prof_metros:.2f} metros")
            
            if st.session_state['pozo_seleccionado']:
                prof_total = st.session_state['pozo_seleccionado']['Profundidad (m)']
                st.write(f"Profundidad Total: {prof_total} m")
                st.progress(min(prof_metros / prof_total, 1.0))
        else:
            st.error("P2 debe ser mayor que P1 para calcular el estiramiento.")
def vista_punto_libre():
    header_app()
    c1, c2 = st.columns([4, 1])
    with c1:
        if st.button("⬅️ Volver al Panel"): 
            st.session_state['pantalla'] = 'dashboard'; st.rerun()
    with c2:
        if st.button("🔬 Ver Fórmula"): 
            st.session_state['pantalla'] = 'formulas'; st.rerun()
        
    st.markdown('<div class="modulo-header"><h2>🧮 Ingeniería: Cálculo de Punto Libre</h2></div>', unsafe_allow_html=True)
    
    col_in, col_out, col_viz = st.columns([1.5, 1.2, 1.3])
    
    with col_in:
        st.subheader("📥 Parámetros")
        tabla_constantes = {"5/8\"": 0.522, "3/4\"": 0.751, "7/8\"": 1.022, "1\"": 1.336}
        sel = st.selectbox("Diámetro de Varilla:", list(tabla_constantes.keys()))
        p1 = st.number_input("P1 (lbs)", 15000)
        p2 = st.number_input("P2 (lbs)", 35000)
        est = st.number_input("Estiramiento (pulg)", 12.0)

    with col_out:
        st.subheader("📊 Resultado")
        dp = p2 - p1
        if dp > 0:
            prof_m = ((est * tabla_constantes[sel] * 1000000) / dp) * 0.3048
            st.metric("Atrapamiento a:", f"{prof_m:.2f} m")
            
            if st.session_state['pozo_seleccionado']:
                total_m = st.session_state['pozo_seleccionado']['Profundidad (m)']
                st.write(f"Prof. Total: {total_m} m")
                
                with col_viz:
                    st.write("**Esquema del Pozo**")
                    # SOLUCIÓN AL ERROR: Creamos dos columnas separadas para que acepte dos colores
                    # O usamos una estructura que Streamlit entienda por color
                    graf_data = pd.DataFrame({
                        'Tramo': ['Pozo'],
                        'Libre (m)': [prof_m],
                        'Atrapado (m)': [max(0, total_m - prof_m)]
                    }).set_index('Tramo')
                    
                    # Al tener dos columnas (Libre y Atrapado), ahora sí acepta dos colores
                    st.bar_chart(graf_data, color=["#2ecc71", "#e74c3c"])
                    st.caption("🟢 Libre | 🔴 Atrapado")
        else:
            st.error("P2 debe ser mayor que P1")
            
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
def vista_well_control():
    header_app()
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.markdown('<div class="modulo-header"><h2>🛡️ Control de Pozo (Well Control)</h2></div>', unsafe_allow_html=True)
    
    st.info("🎯 Objetivo: Mantener el control primario del pozo mediante la columna hidrostática.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🛠️ Calculadora de Hidrostática")
        # Inputs técnicos
        tvd_m = st.number_input("Profundidad Vertical Verdadera (m):", value=1500, step=100)
        densidad_ppg = st.number_input("Densidad del Fluido (ppg):", value=9.5, step=0.1)
        
        # Conversión interna para la fórmula API (Metros a Pies)
        tvd_ft = tvd_m * 3.28084
        presion_hidro = 0.052 * densidad_ppg * tvd_ft
        
        st.metric("Presión Hidrostática (Ph)", f"{presion_hidro:.0f} PSI")
        st.caption("Fórmula: $P_h = 0.052 \times \rho \times TVD$")

    with col2:
        st.subheader("🚨 Cálculo de Ahogo (Kill Sheet)")
        presion_poro = st.number_input("Presión de Formación / Reservorio (PSI):", value=2000)
        
        # Cálculo de Densidad de Ahogo
        if tvd_ft > 0:
            kill_weight = presion_poro / (0.052 * tvd_ft)
            st.metric("Densidad de Ahogo Requerida", f"{kill_weight:.2f} ppg")
            
            # Alerta de seguridad
            if kill_weight > densidad_ppg:
                st.error(f"⚠️ ¡POZO BAJO PRESIÓN! Se requiere densificar de {densidad_ppg} a {kill_weight:.2f} ppg.")
            else:
                st.success("✅ Margen de seguridad correcto (Sobre-balanceado).")

    st.divider()
    
    # Visualización de presiones
    st.subheader("📈 Balance de Presiones en Fondo")
    chart_data = pd.DataFrame({
        'Tipo': ['Hidrostática', 'Formación'],
        'Presión (PSI)': [presion_hidro, presion_poro]
    })
    st.bar_chart(chart_data, x='Tipo', y='Presión (PSI)', color=["#3498db"])            
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
        for i, p in enumerate(pasos): st.checkbox(f"{i+1}. {p}", key=f"step_{i}")
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
        for i, p in enumerate(pasos): st.checkbox(f"{i+1}. {p}", key=f"step_{i}")
def vista_herramientas():
    header_app()
    if st.button("⬅️ Volver"): 
        st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.markdown('<div class="modulo-header"><h2>🛠️ Herramientas de Boca de Pozo y Torque</h2></div>', unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs(["🔧 Llaves y Calibres", "⚖️ Tablas de Torque", "📏 Simulador Calibrado"])
    
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Llaves Manuales vs Hidráulicas")
            st.write("""
            * **Llaves Manuales:** Uso para aproximación y desenoque inicial. Requieren estribo de seguridad.
            * **Llaves Hidráulicas (Power Tongs):** Garantizan el torque uniforme según API. Crucial para evitar 'saltos' de rosca.
            """)
        with c2:
            st.subheader("Chapas Calibre (No-Go Gauges)")
            st.info("💡 Antes de bajar cualquier herramienta, debe pasar por la chapa calibre para asegurar el OD (diámetro externo) correcto.")

    with t2:
        st.subheader("Torques Admisibles para Varillas de Acero")
        # Datos basados en recomendaciones de fabricantes para la Cuenca Cuyana
        df_torque = pd.DataFrame({
            "Diámetro (in)": ["5/8\"", "3/4\"", "7/8\"", "1\"", "1 1/8\""],
            "Torque Mín (ft-lbs)": [200, 350, 500, 800, 1100],
            "Torque Máx (ft-lbs)": [350, 600, 900, 1400, 1900]
        })
        st.table(df_torque)
        st.warning("⚠️ El exceso de torque estira el pin de la varilla y causa fallas por fatiga prematura.")

    with t3:
        st.subheader("Simulador de Calibración")
        st.write("Verificación de diámetro de varilla con Chapa Calibre:")
        diam_nominal = st.selectbox("Seleccione Diámetro Nominal:", ["5/8\"", "3/4\"", "7/8\"", "1\""])
        lectura_real = st.number_input("Lectura del Calibre (pulgadas):", value=0.875, format="%.3f")
        
        # Lógica de validación
        tolerancia = {"5/8\"": 0.625, "3/4\"": 0.750, "7/8\"": 0.875, "1\"": 1.000}
        
        if abs(lectura_real - tolerancia[diam_nominal]) < 0.010:
            st.success(f"✅ HERRAMIENTA CALIBRADA. Pasa por la chapa {diam_nominal}.")
        else:
            st.error(f"🚨 HERRAMIENTA FUERA DE CALIBRE. No debe bajar al pozo.")            
def monitor_barreras_seguridad():
    st.subheader("🛡️ Monitor de Barreras de Seguridad")
    
    if st.session_state['pozo_seleccionado']:
        datos = st.session_state['pozo_seleccionado']
        tvd_ft = datos['Profundidad (m)'] * 3.28
        presion_formacion = datos['Presión Reservorio (PSI)']
        
        # Simulamos una densidad de fluido actual (puedes conectarla a un slider)
        densidad_actual = st.sidebar.slider("Densidad Fluido en Pozo (ppg)", 8.3, 12.0, 9.5)
        ph_actual = 0.052 * densidad_actual * tvd_ft
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        # Margen de Sobre-balance (Trip Margin)
        margen = ph_actual - presion_formacion
        
        with col_m1:
            st.metric("P. Hidrostática", f"{ph_actual:.0f} PSI", delta=f"{margen:.0f} ppg")
        
        with col_m2:
            st.metric("P. Formación", f"{presion_formacion} PSI")
            
        with col_m3:
            if margen > 200:
                st.success("ESTADO: SEGURO")
            elif 0 < margen <= 200:
                st.warning("ESTADO: MARGEN CRÍTICO")
            else:
                st.error("ESTADO: ¡SURGENCIA (KICK)!")
                st.toast("🚨 ¡Cierre la BOP inmediatamente!", icon="🚨")

        # Gráfico comparativo de presiones
        df_press = pd.DataFrame({
            "Categoría": ["Hidrostática", "Formación"],
            "PSI": [ph_actual, presion_formacion]
        })
        st.bar_chart(df_press, x="Categoría", y="PSI", color=["#00457C"])

# --- MÓDULO DE CIERRE: BITÁCORA Y REPORTE ---
def vista_bitacora_y_reporte():
    header_app()
    if st.button("⬅️ Volver"): volver_dashboard()
    
    st.markdown('<div class="modulo-header"><h2>📝 Parte Diario de Operaciones (Bitácora)</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state['pozo_seleccionado']:
        st.warning("No hay datos de operación para reportar.")
        return

    datos = st.session_state['pozo_seleccionado']
    
    with st.container():
        st.subheader(f"Resumen de Intervención: {datos['Pozo']}")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            novedad = st.text_area("Descripción de la Maniobra:", 
                                  placeholder="Ej: Se bajó pescador Overshot, se tensionó hasta 45k lbs...")
            obs_tecnica = st.text_area("Observaciones Técnicas (Fallas detectadas):", 
                                      placeholder="Ej: Se observó fatiga en el cuello de la varilla...")
        
        with col_res2:
            st.info("Parámetros Finales Sugeridos para el Parte:")
            st.write(f"**- Equipo:** Pulling MENFA-01")
            st.write(f"**- Profundidad de Pesca:** {datos['Profundidad (m)']} m")
            st.write(f"**- Grado de Material:** {datos['Grado Varilla']}")
            voto = st.radio("Estado Final del Pozo:", ["Produciendo", "En Pesca (Pendiente)", "Ahogado/Cerrado"])

        if st.button("💾 Guardar y Finalizar Reporte"):
            # Aquí simulamos la creación de un registro
            reporte = {
                "Operador": st.session_state['user']['nombre'],
                "Pozo": datos['Pozo'],
                "Novedad": novedad,
                "Estado": voto,
                "Fecha": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }
            st.success("✅ Reporte guardado exitosamente en el servidor de IPCL MENFA.")
            st.balloons()
            
            # Opción de visualización del Ticket Final
            st.markdown("---")
            st.markdown("### 📄 TICKET DE OPERACIÓN")
            st.code(f"""
            INSTITUTO MENFA - MENDOZA
            CERTIFICADO DE MANIOBRA
            ---------------------------
            OPERADOR: {reporte['Operador']}
            POZO: {reporte['Pozo']}
            FECHA: {reporte['Fecha']}
            RESULTADO: {reporte['Estado']}
            DETALLE: {reporte['Novedad'][:50]}...
            ---------------------------
            SISTEMA DE GESTIÓN DE INTEGRIDAD
            """)

def modulo_hse_y_costos():
    st.markdown('<div class="modulo-header"><h2>🛡️ Seguridad y Control Económico</h2></div>', unsafe_allow_html=True)
    
    col_hse, col_money = st.columns(2)
    
    with col_hse:
        st.subheader("Análisis de Trabajo Seguro (ATS)")
        seg_1 = st.checkbox("BOP de varillas instalada y probada.")
        seg_2 = st.checkbox("Eslingas e instrumentación con certificación vigente.")
        seg_3 = st.checkbox("Personal con EPP completo (Casco, Guantes, Botas, Protección visual).")
        
        if not (seg_1 and seg_2 and seg_3):
            st.error("🚫 Bloqueo de Seguridad: No puede operar sin completar el ATS.")
        else:
            st.success("✅ Área Segura. Puede proceder al simulador.")

    with col_money:
        st.subheader("Impacto Económico (OPEX)")
        # Simulación de tiempo transcurrido (puedes usar el estado de la sesión)
        horas_op = st.number_input("Horas de Intervención Estimadas:", value=8)
        tarifa_pulling = 450 # USD/Hora
        costo_total = horas_op * tarifa_pulling
        
        st.metric("Costo Estimado de Operación", f"USD {costo_total:,}")
        st.caption("Nota: Las intervenciones representan el 30% del costo operativo en Mendoza.")

def gestion_fluidos_ahogo():
    st.subheader("🛢️ Selección de Fluido de Control")
    densidad_req = 9.2 # Valor que vendría de tu calculadora de ingeniería
    
    fluido = st.selectbox("Seleccione Fluido de Ahogo:", 
                         ["Agua Dulce (8.33 ppg)", "Salmuera (9.5 ppg)", "Lodo Base Aceite (10.2 ppg)"])
    
    if "Salmuera" in fluido:
        st.success("Hidrostática Correcta: El pozo está en equilibrio (Overbalanced).")
    elif "Agua" in fluido:
        st.warning("Peligro de Surgencia: La densidad es insuficiente para la presión de reservorio.")
    else:
        st.error("Peligro de Admisión: Fluido demasiado pesado. Riesgo de daño a la formación.")

# --- 5. LÓGICA DE RANKING Y GAMIFICACIÓN ---
if 'ranking' not in st.session_state:
    # Datos de ejemplo para que no aparezca vacío
    st.session_state['ranking'] = pd.DataFrame([
        {"Operador": "Instructor Fabricio", "Puntaje": 5000, "Estado": "Excelente", "Pozo": "MENFA-101"},
        {"Operador": "Alumno_Pro", "Puntaje": 4200, "Estado": "Seguro", "Pozo": "MENFA-102"}
    ])

def calcular_puntaje_final(novedad_msg, tension_max, limite, hse_ok, tiempo):
    score = 0
    # Bono por Seguridad
    if hse_ok: score += 1000
    
    # Bono por Integridad (No romper)
    if tension_max <= limite: 
        score += 2000
    else: 
        score -= 1500 # Penalización crítica por rotura
    
    # Eficiencia en tiempo (Supongamos meta de 10hs)
    if tiempo < 10: score += (10 - tiempo) * 100
    return score      
        # 1. Corrección del final de la función del simulador
    st.session_state['ranking'] = pd.concat([st.session_state['ranking'], pd.DataFrame([nuevo_rank])], ignore_index=True)
    st.success("Operación reportada al Ranking.")


# 2. Asegúrate de definir las funciones que faltan para que no den NameError
def vista_ranking():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>🏆 Ranking de Eficiencia MENFA</h2></div>', unsafe_allow_html=True)
    st.table(st.session_state['ranking'])
def vista_diploma():
    header_app()
    if st.button("⬅️ Volver"): 
        st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    # Buscamos el mejor puntaje del usuario actual en el ranking
    user_name = st.session_state['user']['nombre']
    df_rank = st.session_state['ranking']
    score_user = df_rank[df_rank['Operador'] == user_name]['Puntaje'].max() if user_name in df_rank['Operador'].values else 0

    if score_user >= 4000:
        st.balloons()
        st.markdown(f"""
        <div style="border: 10px solid #00457C; padding: 50px; text-align: center; background-color: white;">
            <h1 style="color: #00457C;">CERTIFICADO DE EXCELENCIA</h1>
            <p style="font-size: 20px;">IPCL MENFA - Mendoza, Argentina</p>
            <hr>
            <p style="font-size: 25px;">Se certifica que:</p>
            <h2 style="text-decoration: underline;">{user_name.upper()}</h2>
            <p style="font-size: 20px;">Ha completado exitosamente el entrenamiento de <br><b>SIMULACIÓN DE PESCA Y WELL CONTROL</b></p>
            <p style="font-size: 22px; color: #2ecc71;"><b>Puntaje Obtenido: {score_user} pts</b></p>
            <br><br>
            <div style="display: flex; justify-content: space-around;">
                <div>_______________________<br>Instructor Fabricio</div>
                <div>_______________________<br>Sello IPCL MENFA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("🖨️ Imprimir Pantalla (Ctrl+P)")
    else:
        st.error(f"Lo siento, {user_name}. Necesitas al menos 4000 puntos para obtener el diploma. Tu puntaje actual es {score_user}.") 
def vista_formulas():
    header_app()
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.markdown('<div class="modulo-header"><h2>🧮 Prontuario de Fórmulas Técnicas - IPCL MENFA</h2></div>', unsafe_allow_html=True)
    
    st.info("💡 Estas fórmulas rigen el comportamiento del simulador y los cálculos de intervención en la Cuenca Cuyana.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Control de Pozos (Well Control)")
        st.write("Para calcular la densidad de ahogo (Kill Mud Weight):")
        st.latex(r"D_{ahogo} [ppg] = \frac{P_{res} [psi]}{0.052 \times TVD [ft]}")
        
        st.write("Presión Hidrostática ($P_h$):")
        st.latex(r"P_h [psi] = 0.052 \times \rho [ppg] \times TVD [ft]")
        
        st.subheader("2. Mecánica de Varillas (API 11B)")
        st.write("Carga Máxima de Operación Sugerida ($T_{max}$):")
        st.latex(r"T_{max} [lbs] = S_f \times 0.90 \times \text{Límite de Fluencia}")
        st.caption("Donde $S_f$ es el factor de servicio (0.5 a 1.0 según corrosión).")

    with col2:
        st.subheader("3. Estiramiento y Punto Libre")
        st.write("Profundidad de Atrapamiento ($L$):")
        st.latex(r"L [m] = \left( \frac{E [in] \times Et \times 10^6}{\Delta P [lbs]} \right) \times 0.3048")
        
        st.write("Constante Elástica ($Et$) de la varilla:")
        st.latex(r"Et = \frac{1}{A [in^2] \times E_{acero}}")
        st.caption("Siendo $E_{acero} \approx 30 \times 10^6 psi$.")

    st.divider()
    
    st.subheader("4. Capacidades Volumétricas")
    cv_col1, cv_col2 = st.columns(2)
    with cv_col1:
        st.write("Volumen en Tubing ($V_t$):")
        st.latex(r"V_t [bbl] = ID^2 [in] \times 0.0009714 \times L [ft]")
    with cv_col2:
        st.write("Volumen Anular ($V_a$):")
        st.latex(r"V_a [bbl] = (ID_{csg}^2 - OD_{tbg}^2) \times 0.0009714 \times L [ft]")        
def vista_manual():
    header_app()
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.markdown('<div class="modulo-header"><h2>📖 Manual de Procedimientos - IPCL MENFA</h2></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["⚙️ Especificaciones API", "📉 Gestión OPEX", "🛡️ Protocolos HSE"])
    
    with tab1:
        st.subheader("Resistencia de Varillas (API 11B)")
        st.table({
            "Grado": ["Grado K", "Grado D", "Grado KD"],
            "Material": ["Acero al Níquel", "Acero al Carbono", "Aleación Especial"],
            "Límite Fluencia (psi)": ["85,000", "115,000", "115,000"],
            "Uso Recomendado": ["Corrosión leve", "Cargas pesadas", "Corrosión + Carga"]
        })
        st.info("💡 Nunca tensione por encima del 80% del límite de fluencia para evitar deformación plástica.")

    with tab2:
        st.subheader("Optimización de Costos en Mendoza")
        st.write("""
        * **Frecuencia de Intervención:** El objetivo es estirar el ciclo de vida del pozo a +24 meses.
        * **Costo de Equipo:** Cada hora de Pulling en Mendoza promedia los 450-600 USD.
        * **Impacto de Rotura:** Una rotura por sobre-tensión implica pesca con 'Overshot', aumentando el OPEX en un 40%.
        """)

    with tab3:
        st.subheader("Checklist de Seguridad Crítica")
        st.warning("1. Verificar estanqueidad de la BOP.\n2. Asegurar zona de exclusión debajo del bloque viajero.\n3. Controlar vientos de la torre (API 4F).")
# 3. LÓGICA PRINCIPAL DE NAVEGACIÓN (Al final de todo el archivo)
if not st.session_state['auth']:
    vista_registro()
else:
    pantalla = st.session_state.get('pantalla', 'dashboard')
    if pantalla == 'dashboard':
        vista_dashboard()
    elif pantalla == 'legajo':
        vista_legajo()
    elif pantalla == 'simulador':
        vista_simulador_operativo()
    elif pantalla == "punto_libre":
         vista_punto_libre()
    elif pantalla == 'hse':
        vista_hse_seguridad()
    elif pantalla == 'ranking':
        vista_ranking()
    elif pantalla == "manual":
         vista_manual()
    elif pantalla == "diploma":
         vista_diploma()
    elif pantalla == "formulas":
         vista_formulas()
    elif pantalla == "well_control":
         vista_well_control()
    elif pantalla == "monitor_barreras_seguridad":
         vista_monitor_barreras_seguridad()
        
