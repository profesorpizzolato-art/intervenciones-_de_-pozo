import streamlit as st
import pandas as pd
import numpy as np
import random
import io

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
        # Verificamos que existan los datos del usuario para no tener otro error
        u = st.session_state.get('user', {'nombre': 'Usuario', 'rol': 'Alumno'})
        st.subheader(f"🏢 IPCL MENFA | Operador: {u.get('nombre')} | Rol: {u.get('rol')}")
    with c2:
        # EL CAMBIO CRÍTICO: Agregamos key="btn_logout_unico"
        if st.button("Cerrar Sesión", key="btn_logout_unico"):
            st.session_state['auth'] = False
            st.session_state['pantalla'] = 'dashboard' # Reiniciamos la vista
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
import io

def generar_excel_reporte(df):
    output = io.BytesIO()
    # Usamos xlsxwriter que ya declaraste en requirements.txt
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Ranking_MENFA')
        
        workbook  = writer.book
        worksheet = writer.sheets['Ranking_MENFA']
        
        # Formato profesional para el encabezado
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#00457C',
            'font_color': 'white',
            'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 18)
            
    return output.getvalue()
# --- PANTALLAS ---

def vista_registro():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        # Cambio de use_container_width por width='stretch'
        st.image("logo_menfa.png", width="stretch") 
        st.markdown("<h2 style='text-align: center;'>Acceso al Sistema Técnico</h2>", unsafe_allow_html=True)
        # ... resto del código
        with st.form("login"):
            n = st.text_input("Nombre Completo")
            d = st.text_input("DNI / Legajo")
            r = st.selectbox("Función", ["Instructor", "Jefe de Equipo", "Company Man", "Alumno"])
            if st.form_submit_button("Ingresar"):
                if n and d:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": n, "dni": d, "rol": r}
                    st.rerun()

def generar_excel_reporte(df):
    output = io.BytesIO()
    # Creamos el escritor de Excel usando xlsxwriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte_MENFA')
        
        # Formato visual para el Excel
        workbook  = writer.book
        worksheet = writer.sheets['Reporte_MENFA']
        
        # Formato de encabezado (Azul MENFA)
        header_format = workbook.add_format({
            'bold': True, 'text_wrap': True,
            'valign': 'vcenter', 'fg_color': '#00457C',
            'font_color': 'white', 'border': 1
        })
        
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 20) # Ancho de columna
            
    return output.getvalue()
def vista_dashboard():
    header_app()
    st.title("Panel de Control de Intervenciones - IPCL MENFA")
    
    # --- CSS ACTUALIZADO PARA CARDS CON IMÁGENES DE FONDO ---
    st.markdown("""
        <style>
            .container-tecnico {
                display: flex; gap: 20px; justify-content: center;
                flex-wrap: wrap; margin-top: 20px;
            }
            .card-tecnica-img {
                flex: 1; min-width: 250px;
                height: 300px; padding: 25px; border-radius: 12px;
                color: white; font-weight: bold; position: relative;
                box-shadow: 0 5px 15px rgba(0,0,0,0.4);
                background-size: cover; background-position: center;
                transition: transform 0.3s ease;
                display: flex; flex-direction: column; justify-content: space-between;
            }
            .card-tecnica-img:hover { transform: translateY(-10px); }
            
            /* Sombreado de degradado para que el texto resalte */
            .card-text-overlay {
                background: linear-gradient(0deg, rgba(0,0,0,0.85) 15%, rgba(0,0,0,0) 100%);
                position: absolute; bottom: 0; left: 0; width: 100%;
                height: 100%; border-radius: 12px; padding: 25px;
                display: flex; flex-direction: column; justify-content: flex-end;
            }
            .card-text-overlay h3 { color: #fdfdfd; text-transform: uppercase; margin-bottom: 5px; }
            .card-text-overlay p { color: #e0e0e0; font-size: 1.1em; }
        </style>
    """, unsafe_allow_html=True)
    
    # --- FILA 1: OPERACIONES PRINCIPALES CON IMÁGENES DE ALTO IMPACTO ---
  # --- FILA 1: OPERACIONES PRINCIPALES ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # IMAGEN: Planos técnicos y carpetas de ingeniería
        img_activos = "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=600&h=400"
        st.markdown(f"""
            <div class="card-tecnica-img" style="background-image: url('{img_activos}');">
                <div class="card-text-overlay">
                    <h3>📋 Gestión de Activos</h3>
                    <p>Acceso a legajos técnicos y diseño de pozos de la Cuenca Cuyana.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Legajos", key="btn_legajos"): 
            st.session_state['pantalla'] = 'legajo'; st.rerun()
            
    with col2:
        # IMAGEN: Torre de perforación/pulling real
        img_simulador = "https://images.unsplash.com/photo-1516937941344-00b4e0337589?auto=format&fit=crop&w=600&h=400"
        st.markdown(f"""
            <div class="card-tecnica-img" style="background-image: url('{img_simulador}');">
                <div class="card-text-overlay">
                    <h3>🏗️ Simulador Pulling</h3>
                    <p>Práctica de maniobras de pesca y eventos operativos a tiempo real.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir Simulador", key="btn_simulador"): 
            st.session_state['pantalla'] = 'simulador'; st.rerun()
            
    with col3:
        # IMAGEN: Tablero de control con luces y métricas (representando el ranking/éxito)
        img_ranking = "https://images.unsplash.com/photo-1551288049-bbbda536339a?auto=format&fit=crop&w=600&h=400"
        st.markdown(f"""
            <div class="card-tecnica-img" style="background-image: url('{img_ranking}');">
                <div class="card-text-overlay">
                    <h3>🏆 Ranking MENFA</h3>
                    <p>Tabla de eficiencia operativa y cuadro de honor de los mejores operadores.</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Ranking", key="btn_ranking"): 
            st.session_state['pantalla'] = 'ranking'; st.rerun()
    # --- FILA 2: INGENIERÍA Y ADMINISTRACIÓN (Corregido) ---
    ca, cb, cc, cd = st.columns(4)
    
    with ca: 
        st.info("🧮 PUNTO LIBRE")
        if st.button("Cálculos", key="btn_calc_pl"): 
            st.session_state['pantalla'] = 'punto_libre'
            st.rerun()
            
    with cb: 
        st.warning("🛡️ SEGURIDAD")
        if st.button("Manual HSE", key="btn_hse"): 
            st.session_state['pantalla'] = 'hse'
            st.rerun()
            
    with cc: 
        st.success("🔬 INGENIERÍA")
        if st.button("Well Control", key="btn_wc"): 
            st.session_state['pantalla'] = 'well_control'
            st.rerun()
            
    with cd: 
        st.error("🔧 HERRAMIENTAS")
        if st.button("Torque/Calibración", key="btn_torque"): 
            st.session_state['pantalla'] = 'herramientas'
            st.rerun()
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
    # 1. El header siempre va primero
    header_app()
    
    # --- 🟢 SEGURO ANTICRASH (Fabricio, esto evita el error de la sesión vacía) ---
    if st.session_state.get('pozo_seleccionado') is None:
        st.warning("⚠️ No hay un pozo cargado en el sistema.")
        st.info("Por favor, ve al módulo 'Gestión de Activos' (Legajos) y selecciona un pozo para operar.")
        if st.button("Ir a Legajos", key="btn_go_legajos_fail"):
            st.session_state['pantalla'] = 'legajo'
            st.rerun()
        return # Cortamos la ejecución aquí si no hay pozo
    
   # 2. LÓGICA DE EMERGENCIA PASO A PASO
    if st.session_state.get('evento_activo') == "KICK":
        import time
        
        # --- INICIALIZACIÓN DEL PASO ---
        if 'paso_kick' not in st.session_state:
            st.session_state['paso_kick'] = 1
            st.session_state['inicio_kick'] = time.time()
        
        tiempo_transcurrido = time.time() - st.session_state['inicio_kick']
        tiempo_restante = max(0, 45 - int(tiempo_transcurrido)) # Damos 45s para el proceso completo

        st.error(f"🚨 ¡KICK DETECTADO! Tiempo crítico: {tiempo_restante}s")
        st.progress(tiempo_restante / 45)

        # --- FLUJO DE ACCIONES ---
        paso = st.session_state['paso_kick']

        if paso == 1:
            st.subheader("Paso 1: Detener maniobra y asegurar")
            st.info("El vástago está subiendo. ¿Qué acción realizas primero?")
            if st.button("Posicionar herramienta y asentar en cuñas", key="step1_ok"):
                st.session_state['paso_kick'] = 2
                st.rerun()
            if st.button("Salir corriendo de la locación", key="step1_fail"):
                st.error("❌ Abandono de puesto sin asegurar. Penalización máxima.")
                st.session_state['ranking'].loc[st.session_state['ranking']['Operador'] == st.session_state['user']['nombre'], 'Puntaje'] -= 1000

        elif paso == 2:
            st.subheader("Paso 2: Elección de Herramienta de Cierre")
            st.info("Necesitas cerrar la BOP manual. ¿Qué herramienta llevas al cabezal?")
            h_emerg = st.radio("Herramientas disponibles:", ["Llave Stillson", "Llave de Golpe (Slogging)", "Llave Francesa"], key="radio_h")
            if st.button("Confirmar Herramienta"):
                if h_emerg == "Llave de Golpe (Slogging)":
                    st.success("✅ Correcto. Corriendo al cabezal...")
                    st.session_state['paso_kick'] = 3
                    st.rerun()
                else:
                    st.warning("⚠️ Esa herramienta no dará el torque necesario. Perdiste tiempo.")

        elif paso == 3:
            st.subheader("Paso 3: Torque de Sellado")
            st.info("Aplica los golpes necesarios para sellar el empaque (Stripper/BOP).")
            golpes = st.number_input("Cantidad de golpes con maza:", 0, 10, 0)
            if st.button("Finalizar Cierre"):
                if golpes >= 6:
                    st.session_state['paso_kick'] = 4 # Éxito
                    st.rerun()
                else:
                    st.error("❌ Presión insuficiente. El pozo sigue fluyendo.")

        elif paso == 4:
            st.balloons()
            st.success(f"🎊 ¡POZO CONTROLADO! Tiempo total: {int(time.time() - st.session_state['inicio_kick'])}s")
            if st.button("Volver al Simulador"):
                st.session_state['evento_activo'] = None
                del st.session_state['paso_kick']
                del st.session_state['inicio_kick']
                st.rerun()

        # --- CONTROL DE DERRAME ---
        if tiempo_restante <= 0:
            st.error("💥 DESBORDE TOTAL. El pozo ha superado la capacidad de cierre.")
            if st.button("Reiniciar Intento"):
                st.session_state['evento_activo'] = None
                del st.session_state['paso_kick']
                del st.session_state['inicio_kick']
                st.rerun()
        
        time.sleep(1)
        st.rerun()
        return
    # 3. INTERFAZ NORMAL (Solo se llega aquí si hay pozo y NO hay emergencia)
    pozo = st.session_state['pozo_seleccionado']
    st.title(f"🏗️ Operando: {pozo['Pozo']}")
    
    # Botón para el instructor (vos)
    if st.sidebar.button("Simular Surgencia (Examen)", key="btn_trigger_kick"):
        st.session_state['evento_activo'] = "KICK"
        st.rerun()

    # --- SIMULACIÓN DE TENSIÓN ---
    tension = st.slider("Tensión del Gancho (lbs)", 0, 120000, 35000, key="slider_tension")
    
    c_graph, c_info = st.columns([2, 1])
    with c_graph:
        y = np.random.normal(tension, 500, 20)
        st.line_chart(y, width="stretch") # Recordá el width="stretch" que pedía Streamlit 2026
    
    with c_info:
        st.metric("Profundidad de Pesca", f"{pozo['Profundidad (m)']} m")
        st.metric("Punto Libre Estimado", f"{pozo['Profundidad (m)'] * 0.8:.0f} m")

    # ... acá seguís con tu gráfico de tensión y demás
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
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    st.markdown('<div class="modulo-header"><h2>🛠️ Catálogo Técnico de Herramientas y Torque</h2></div>', unsafe_allow_html=True)
    
    # --- MENÚ DE NAVEGACIÓN INTERNA ---
    tab_m, tab_h, tab_p, tab_c = st.tabs([
        "🔧 Llaves y Torque", 
        "🛠️ Herramientas de Mano", 
        "🎣 Herramientas de Pesca", 
        "📏 Calibración API"
    ])
    
    with tab_m:
        st.subheader("Control de Torque (API RP 7G-2)")
        col1, col2 = st.columns([2, 1])
        with col1:
            data_t = {
                "Elemento": ["Varilla 5/8\"", "Varilla 3/4\"", "Varilla 7/8\"", "Varilla 1\"", "Tubing 2 3/8\" EUE", "Tubing 2 7/8\" EUE"],
                "Torque Mín (ft-lbs)": [200, 350, 500, 800, 1200, 1700],
                "Torque Máx (ft-lbs)": [350, 600, 900, 1400, 1800, 2500]
            }
            st.table(pd.DataFrame(data_t))
        with col2:
            st.info("💡 **Dato MENFA:** En pozos con alta salinidad en Mendoza, se recomienda usar grasa con 50% de zinc para asegurar el sellado.")
            # Gráfico de Torque vs Tensión
            t_val = np.linspace(0, 1500, 15)
            s_val = t_val * 1.8
            df_chart = pd.DataFrame({"Torque": t_val, "Tensión Pin": s_val}).set_index("Torque")
            st.line_chart(df_chart, width="stretch")

    with tab_h:
        st.subheader("Herramental de Boca de Pozo")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Llaves de Golpe (Slogging Spanners)**")
            st.caption("Uso: Ajuste de bridas de BOP y bridas de producción.")
        with c2:
            st.markdown("**Llaves de Caño (Stillson/Rigid)**")
            st.caption("Uso: Conexiones auxiliares. Prohibido su uso en cuerpo de varilla.")
        with c3:
            st.markdown("**Elevadores de Varilla**")
            st.caption("Verificar: Seguro de traba y desgaste de asiento.")

    with tab_p:
        st.subheader("Herramientas de Pesca (Fishing Tools)")
        st.write("Selección según el tipo de 'pescado' en la Cuenca:")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.write("🎯 **Para Agarre Externo:**")
            st.markdown("- **Overshot:** El más versátil (Grapple tipo cesta o espiral).")
            st.markdown("- **Die Nipple:** Para agarrar por fuera mediante roscado.")
        with col_p2:
            st.write("🎯 **Para Agarre Interno:**")
            st.markdown("- **Taper Tap:** Rosca interna en el pescado.")
            st.markdown("- **Itco-Type Release Spear:** Agarre mecánico interno liberable.")
        st.warning("⚠️ Antes de bajar: Medir OD del Overhot y ID del Casing (debe haber margen de circulación).")

    with tab_c:
        st.subheader("Simulador de Chapas Calibre (Gauges)")
        st.write("Simulación de paso de herramienta:")
        
        c_sel = st.selectbox("Herramienta a Calibrar:", ["Bomba de Profundidad", "Pescante", "Centralizador", "Tapa de Pesca"])
        val_cal = st.number_input("Medida del Calibre No-Go (in):", value=2.500, format="%.3f")
        
        # Lógica de calibración
        metas = {"Bomba de Profundidad": 2.250, "Pescante": 1.750, "Centralizador": 2.875, "Tapa de Pesca": 2.000}
        
        if val_cal <= metas[c_sel]:
            st.success(f"✅ ¡APROBADO! La herramienta pasa por la chapa de {metas[c_sel]}\"")
        else:
            st.error(f"🚨 RECHAZADO: El OD ({val_cal}\") es superior al máximo permitido ({metas[c_sel]}\").")          
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
# --- SECCIÓN DE DESCARGA (Solo visible si hay datos) ---
    if not df_rank.empty:
        st.write("---")
        st.subheader("📥 Gestión Administrativa")
        
        # Preparamos los datos para el reporte
        df_reporte = df_rank.copy()
        df_reporte['Certificado'] = df_reporte['Puntaje'].apply(lambda x: 'SÍ' if x >= 4000 else 'NO')
        
        excel_data = generar_excel_reporte(df_reporte)
        
        st.download_button(
            label="📊 Descargar Reporte Final (Excel)",
            data=excel_data,
            file_name=f"Reporte_Alumnos_MENFA_{pd.Timestamp.now().strftime('%d-%m-%Y')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        st.caption("El reporte incluye nombres, puntajes y estado de certificación para el legajo del instituto.")
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
    elif pantalla == "herramientas":
         vista_herramientas()     
