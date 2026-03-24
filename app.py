import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ==========================================
# 1. CONFIGURACIÓN E IDENTIDAD - IPCL MENFA
# ==========================================
st.set_page_config(page_title="IPCL MENFA - Simulador Integral", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .modulo-header {
        background-color: #00457C; color: white; padding: 20px;
        border-radius: 12px; margin-bottom: 25px; text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #00457C;
        color: white; font-weight: bold; height: 3.5em; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #002d52; border: 1px solid white; }
    .card-tecnica-img {
        height: 250px; padding: 20px; border-radius: 15px;
        color: white; position: relative;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        background-size: cover; background-position: center;
        display: flex; flex-direction: column; justify-content: flex-end;
    }
    .card-overlay {
        background: linear-gradient(0deg, rgba(0,0,0,0.9) 30%, rgba(0,0,0,0) 100%);
        padding: 15px; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SISTEMA DE ESTADOS (SESSION STATE)
# ==========================================
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {"nombre": "", "rol": ""}
if 'pozo_seleccionado' not in st.session_state: st.session_state['pozo_seleccionado'] = None
if 'evento_activo' not in st.session_state: st.session_state['evento_activo'] = None
if 'paso_kick' not in st.session_state: st.session_state['paso_kick'] = 0
if 'ranking' not in st.session_state:
    st.session_state['ranking'] = pd.DataFrame([{"Operador": "Fabricio", "Puntaje": 5000, "Estado": "Senior", "Fecha": "2026-03-20"}])

# Base de Datos de Pozos Mendoza
data_pozos = pd.DataFrame({
    "Pozo": ["BARRANCAS-101", "VIZCACHERAS-204", "LA-VENTANA-505", "PUESTO-POZO-8"],
    "Profundidad (m)": [1200, 1550, 1800, 1400],
    "Grado Varilla": ["Grado D", "Grado K", "Grado KD", "Grado D"],
    "Presión Reservorio (PSI)": [1500, 1850, 2100, 1600]
})

# ==========================================
# 3. FUNCIONES DE VISTA (PANTALLAS)
# ==========================================

def header_menfa():
    c1, c2 = st.columns([4, 1])
    with c1:
        u = st.session_state['user']
        st.subheader(f"🏢 IPCL MENFA | Operador: {u['nombre']} | Rol: {u['rol']}")
    with c2:
        if st.button("🚪 Cerrar Sesión", key="btn_logout_main"):
            st.session_state['auth'] = False
            st.rerun()
    st.divider()

def vista_registro():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; color: #00457C;'>IPCL MENFA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Instituto Privado de Capacitación Laboral</p>", unsafe_allow_html=True)
        # KEY ÚNICA PARA EL FORMULARIO DE INGRESO
        with st.form(key="form_login_unico"):
            n = st.text_input("Nombre y Apellido del Alumno")
            r = st.selectbox("Nivel de Acceso", ["Alumno", "Instructor", "Company Man"])
            if st.form_submit_button("INGRESAR AL SISTEMA"):
                if n:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": n, "rol": r}
                    if n not in st.session_state['ranking']['Operador'].values:
                        new_row = {"Operador": n, "Puntaje": 0, "Estado": "En Curso", "Fecha": time.strftime("%Y-%m-%d")}
                        st.session_state['ranking'] = pd.concat([st.session_state['ranking'], pd.DataFrame([new_row])], ignore_index=True)
                    st.rerun()

def vista_dashboard():
    header_menfa()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card-tecnica-img" style="background-image: url(\'https://images.unsplash.com/photo-1581094794329-c8112a89af12\');"><div class="card-overlay"><h3>LEGAJO POZOS</h3></div></div>', unsafe_allow_html=True)
        if st.button("Configurar Activos", key="btn_nav_legajo"): st.session_state['pantalla'] = 'legajo'; st.rerun()
            
    with col2:
        st.markdown('<div class="card-tecnica-img" style="background-image: url(\'https://images.unsplash.com/photo-1516937941344-00b4e0337589\');"><div class="card-overlay"><h3>SIMULADOR TORRE</h3></div></div>', unsafe_allow_html=True)
        if st.button("Operar Simulador", key="btn_nav_sim"): st.session_state['pantalla'] = 'simulador'; st.rerun()
            
    with col3:
        st.markdown('<div class="card-tecnica-img" style="background-image: url(\'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1\');"><div class="card-overlay"><h3>HERRAMIENTAS</h3></div></div>', unsafe_allow_html=True)
        if st.button("Taller y Torque", key="btn_nav_tool"): st.session_state['pantalla'] = 'herramientas'; st.rerun()

    st.markdown("### 🧮 Módulos de Ingeniería y Evaluación")
    ca, cb, cc, cd = st.columns(4)
    if ca.button("📏 Punto Libre", key="btn_nav_pl"): st.session_state['pantalla'] = 'punto_libre'; st.rerun()
    if cb.button("🔬 Well Control", key="btn_nav_wc"): st.session_state['pantalla'] = 'well_control'; st.rerun()
    if cc.button("🏆 Ranking", key="btn_nav_rank"): st.session_state['pantalla'] = 'ranking'; st.rerun()
    if cd.button("🎓 Diploma MENFA", key="btn_nav_dip"): st.session_state['pantalla'] = 'diploma'; st.rerun()

def vista_simulador():
    header_menfa()
    if not st.session_state['pozo_seleccionado']:
        st.warning("⚠️ Debes seleccionar un pozo en Legajos antes de operar."); st.button("Ir a Legajos", on_click=lambda: st.session_state.update({'pantalla':'legajo'}))
        return

    pozo = st.session_state['pozo_seleccionado']
    
    if st.session_state.get('evento_activo') == "KICK":
        if 'start_time' not in st.session_state: st.session_state['start_time'] = time.time()
        tiempo = 45 - int(time.time() - st.session_state['start_time'])
        
        if tiempo <= 0:
            st.error("💥 SURGENCIA NO CONTROLADA. El pozo se ha desbordado."); st.button("Reiniciar Simulador", key="btn_fail_kick", on_click=lambda: st.session_state.update({'evento_activo':None, 'paso_kick':0}))
        else:
            st.error(f"🚨 ¡KICK DETECTADO! Tiempo de cierre: {tiempo}s")
            st.progress(max(0, tiempo/45))
            if st.button("1. ASENTAR HERRAMIENTA", key="kick_step_1"): st.session_state['paso_kick'] = 1
            if st.session_state['paso_kick'] == 1:
                if st.button("2. CERRAR BOP / VÁLVULA TIW", key="kick_step_2"):
                    st.session_state['evento_activo'] = None; st.balloons()
                    st.session_state['ranking'].loc[st.session_state['ranking']['Operador'] == st.session_state['user']['nombre'], 'Puntaje'] += 1000
                    st.success("¡Pozo asegurado correctamente! Sumaste 1000 puntos.")
                    st.button("Volver al Control", key="btn_res_sim")
    else:
        st.title(f"Operando en {pozo['Pozo']}")
        tension = st.slider("Tensión en Gancho (lbs)", 0, 120000, 35000, key="sim_tens")
        st.line_chart(np.random.normal(tension, 500, 20))
        if st.sidebar.button("🚨 LANZAR SURGENCIA (EXAMEN)", key="btn_trigger_kick"):
            st.session_state['evento_activo'] = "KICK"; st.session_state.pop('start_time', None); st.rerun()

    if st.button("⬅️ Salir de Torre", key="btn_back_sim"): st.session_state['pantalla'] = 'dashboard'; st.rerun()

def vista_herramientas():
    header_menfa()
    if st.button("⬅️ Volver", key="btn_back_tools"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Taller de Herramientas y Torque</h2></div>', unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["⚙️ Calibración de Torque", "📋 Inventario Crítico"])
    with t1:
        st.latex(r"Torque = K \times D \times F")
        col1, col2 = st.columns(2)
        d = col1.number_input("Diámetro Varilla (pulg)", 0.75, key="inp_tool_d")
        f = col2.number_input("Tensión Objetivo (lbs)", 20000, key="inp_tool_f")
        st.metric("Torque Make-up Recomendado", f"{0.2 * d * f:.2f} lb-ft")
    with t2:
        st.write("Estado de Activos en Mendoza:")
        st.table(pd.DataFrame({"Herramienta": ["Pescador", "Socket", "Llave de Golpe"], "Estado": ["Operativo", "En Reparación", "Operativo"]}))

def vista_punto_libre():
    header_menfa()
    if st.button("⬅️ Volver", key="btn_back_pl"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Cálculo de Punto Libre (Stretch)</h2></div>', unsafe_allow_html=True)
    st.latex(r"L = \frac{Et \times Estiramiento \times 10^6}{P_2 - P_1}")
    et = st.selectbox("Constante de Varilla (Et):", [0.751, 1.022, 1.336], key="sb_pl_et")
    p1 = st.number_input("Tensión Inicial (lbs)", 15000, key="ni_pl_p1")
    p2 = st.number_input("Tensión Final (lbs)", 30000, key="ni_pl_p2")
    est = st.number_input("Estiramiento Medido (pulg)", 10.0, key="ni_pl_est")
    if p2 > p1:
        res = ((est * et * 1000000) / (p2 - p1)) * 0.3048
        st.metric("Profundidad de Atrapamiento", f"{res:.2f} metros")

def vista_diploma():
    header_menfa()
    if st.button("⬅️ Volver", key="btn_back_dip"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    
    u = st.session_state['user']['nombre']
    p = st.session_state['ranking'][st.session_state['ranking']['Operador'] == u]['Puntaje'].max()
    
    if p >= 1500:
        st.balloons()
        st.markdown(f"""
        <div style="border: 15px double #00457C; padding: 40px; text-align: center; background: white; color: #333;">
            <h1 style="color: #00457C;">IPCL MENFA</h1>
            <p><i>Instituto Privado de Capacitación Laboral - Mendoza</i></p>
            <hr style="width: 50%;">
            <h2>CERTIFICADO DE COMPETENCIA</h2>
            <p>Se otorga el presente a:</p>
            <h1 style="text-decoration: underline;">{u.upper()}</h1>
            <p>Por haber aprobado el entrenamiento intensivo en<br><b>Simulación de Perforación y Well Control</b>.</p>
            <br>
            <p>Instructor: Fabricio | Fecha: {time.strftime("%d/%m/%Y")}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Requieres 1500 puntos para el certificado. Actualmente tienes {p} puntos.")

def vista_legajo():
    header_menfa()
    if st.button("⬅️ Volver", key="btn_back_leg"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Gestión de Pozos</h2></div>', unsafe_allow_html=True)
    sel = st.selectbox("Seleccione el Pozo a Operar:", data_pozos["Pozo"], key="sb_sel_pozo")
    d = data_pozos[data_pozos["Pozo"] == sel].iloc[0]
    st.metric("Profundidad TVD", f"{d['Profundidad (m)']} m")
    if st.button("Cargar Datos en la Consola", key="btn_load_pozo"):
        st.session_state['pozo_seleccionado'] = d.to_dict()
        st.success(f"Pozo {sel} cargado correctamente.")

def vista_well_control():
    header_menfa()
    if st.button("⬅️ Volver", key="btn_back_wc"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Well Control & Hidrostática</h2></div>', unsafe_allow_html=True)
    st.latex(r"P_h = 0.052 \times \rho \times TVD[ft]")
    dens = st.number_input("Densidad del Lodo (ppg)", 9.5, key="ni_wc_dens")
    tvd = st.number_input("Profundidad (m)", 1500, key="ni_wc_tvd")
    ph = 0.052 * dens * (tvd * 3.281)
    st.metric("Presión Hidrostática", f"{ph:.0f} PSI")

# ==========================================
# 4. RUTEADOR PRINCIPAL
# ==========================================
if not st.session_state['auth']:
    vista_registro()
else:
    p = st.session_state['pantalla']
    if p == 'dashboard': vista_dashboard()
    elif p == 'legajo': vista_legajo()
    elif p == 'simulador': vista_simulador()
    elif p == 'herramientas': vista_herramientas()
    elif p == 'punto_libre': vista_punto_libre()
    elif p == 'well_control': vista_well_control()
    elif p == 'ranking':
        header_menfa()
        st.table(st.session_state['ranking'])
        if st.button("⬅️ Volver", key="btn_back_rank"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    elif p == 'diploma': vista_diploma()
        
