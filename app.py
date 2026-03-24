import streamlit as st
import pandas as pd
import numpy as np
import time

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL - IPCL MENFA
st.set_page_config(page_title="IPCL MENFA - Simulador Integral", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .modulo-header {
        background-color: #00457C; color: white; padding: 20px;
        border-radius: 12px; margin-bottom: 25px; text-align: center;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; background-color: #00457C;
        color: white; font-weight: bold; height: 3.5em;
    }
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

# 2. INICIALIZACIÓN DE VARIABLES (SESSION STATE)
if 'auth' not in st.session_state: st.session_state['auth'] = False
if 'pantalla' not in st.session_state: st.session_state['pantalla'] = 'dashboard'
if 'user' not in st.session_state: st.session_state['user'] = {"nombre": "", "rol": ""}
if 'pozo_seleccionado' not in st.session_state: st.session_state['pozo_seleccionado'] = None
if 'evento_activo' not in st.session_state: st.session_state['evento_activo'] = None
if 'paso_kick' not in st.session_state: st.session_state['paso_kick'] = 0
if 'ranking' not in st.session_state:
    st.session_state['ranking'] = pd.DataFrame([{"Operador": "Fabricio", "Puntaje": 5000, "Estado": "Senior"}])

# Data Maestra de Pozos (Mendoza)
data_pozos = pd.DataFrame({
    "Pozo": ["BARRANCAS-101", "VIZCACHERAS-204", "LA-VENTANA-505", "PUESTO-POZO-8"],
    "Profundidad (m)": [1200, 1550, 1800, 1400],
    "Grado Varilla": ["Grado D", "Grado K", "Grado KD", "Grado D"],
    "Presión Reservorio (PSI)": [1500, 1850, 2100, 1600],
    "Img_Falla": [
        "https://images.unsplash.com/photo-1581094794329-c8112a89af12", 
        "https://images.unsplash.com/photo-1516937941344-00b4e0337589",
        "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1",
        "https://images.unsplash.com/photo-1454165205744-3b78555e5572"
    ]
})

# --- 3. FUNCIONES DE CABECERA ---
def header_app():
    c1, c2 = st.columns([4, 1])
    with c1:
        u = st.session_state['user']
        st.subheader(f"🏢 IPCL MENFA | Operador: {u['nombre']} | {u['rol']}")
    with c2:
        if st.button("🚪 Salir", key="logout_btn"):
            st.session_state['auth'] = False; st.rerun()
    st.divider()

# --- 4. TODAS LAS VISTAS (SIN RECORTES) ---

def vista_registro():
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("<h1 style='text-align: center; color: #00457C;'>IPCL MENFA</h1>", unsafe_allow_html=True)
        st.info("Ingreso al Sistema de Simulación Técnica")
        with st.form("login"):
            n = st.text_input("Nombre y Apellido")
            r = st.selectbox("Rol", ["Alumno", "Instructor", "Company Man"])
            if st.form_submit_button("INICIAR"):
                if n:
                    st.session_state['auth'] = True
                    st.session_state['user'] = {"nombre": n, "rol": r}
                    if n not in st.session_state['ranking']['Operador'].values:
                        new_row = {"Operador": n, "Puntaje": 1000, "Estado": "Activo"}
                        st.session_state['ranking'] = pd.concat([st.session_state['ranking'], pd.DataFrame([new_row])], ignore_index=True)
                    st.rerun()

def vista_dashboard():
    header_app()
    col1, col2, col3 = st.columns(3)
    
    menus = [
        {"tit": "GESTIÓN LEGAJOS", "img": "https://images.unsplash.com/photo-1581094794329-c8112a89af12", "id": "legajo"},
        {"tit": "SIMULADOR TORRE", "img": "https://images.unsplash.com/photo-1516937941344-00b4e0337589", "id": "simulador"},
        {"tit": "TALLER HERRAMIENTAS", "img": "https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1", "id": "herramientas"}
    ]
    
    for i, m in enumerate(menus):
        with [col1, col2, col3][i]:
            st.markdown(f'<div class="card-tecnica-img" style="background-image: url(\'{m["img"]}\');"><div class="card-overlay"><h3>{m["tit"]}</h3></div></div>', unsafe_allow_html=True)
            if st.button(f"Abrir {m['tit']}", key=f"btn_{m['id']}"):
                st.session_state['pantalla'] = m['id']; st.rerun()

    st.markdown("### 🛠️ Módulos de Cálculo y Evaluación")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📏 Punto Libre"): st.session_state['pantalla'] = 'punto_libre'; st.rerun()
    if c2.button("🔬 Well Control"): st.session_state['pantalla'] = 'well_control'; st.rerun()
    if c3.button("🏆 Ranking"): st.session_state['pantalla'] = 'ranking'; st.rerun()
    if c4.button("🎓 Diploma"): st.session_state['pantalla'] = 'diploma'; st.rerun()

def vista_legajo():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Base de Datos de Pozos</h2></div>', unsafe_allow_html=True)
    sel = st.selectbox("Seleccione Pozo:", data_pozos["Pozo"])
    d = data_pozos[data_pozos["Pozo"] == sel].iloc[0]
    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.metric("Profundidad TVD", f"{d['Profundidad (m)']} m")
        st.metric("Presión Poro", f"{d['Presión Reservorio (PSI)']} PSI")
        if st.button("CARGAR A SIMULADOR"):
            st.session_state['pozo_seleccionado'] = d.to_dict()
            st.success("Configuración enviada.")
    with c2:
        st.image(d['Img_Falla'], caption="Falla Detectada", use_container_width=True)

def vista_simulador_operativo():
    header_app()
    if not st.session_state['pozo_seleccionado']:
        st.warning("⚠️ Seleccioná un pozo en Legajos primero."); return

    if st.session_state.get('evento_activo') == "KICK":
        if 'start_time' not in st.session_state: st.session_state['start_time'] = time.time()
        tiempo = 45 - int(time.time() - st.session_state['start_time'])
        if tiempo <= 0:
            st.error("💥 SURGENCIA NO CONTROLADA. Pozo perdido."); st.button("Reiniciar", on_click=lambda: st.session_state.update({'evento_activo': None, 'paso_kick': 0}))
        else:
            st.error(f"🚨 KICK ACTIVO! Tiempo para el cierre: {tiempo}s")
            st.progress(max(0, tiempo/45))
            if st.button("1. ASENTAR EN CUÑAS"): st.session_state['paso_kick'] = 1
            if st.session_state['paso_kick'] == 1:
                if st.button("2. CERRAR BOP / TIW"):
                    st.session_state['evento_activo'] = None; st.balloons()
                    st.session_state['ranking'].loc[st.session_state['ranking']['Operador'] == st.session_state['user']['nombre'], 'Puntaje'] += 1000
                    st.rerun()
    else:
        st.title(f"Operando: {st.session_state['pozo_seleccionado']['Pozo']}")
        st.line_chart(np.random.normal(35000, 800, 30))
        if st.sidebar.button("🚨 ACTIVAR KICK (EXAMEN)"): 
            st.session_state['evento_activo'] = "KICK"; st.session_state.pop('start_time', None); st.rerun()

    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()

def vista_herramientas():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Taller de Herramientas y Torque</h2></div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["⚙️ Calibración", "📋 Inventario"])
    with t1:
        st.latex(r"T = K \times D \times F")
        diam = st.number_input("Diámetro (pulg)", 0.75)
        fuerza = st.number_input("Tensión (lbs)", 20000)
        st.metric("Torque Make-up", f"{0.2 * diam * fuerza:.2f} lb-ft")
    with t2:
        st.table(pd.DataFrame({"Herramienta": ["Pescador", "Socket", "BOP"], "Estado": ["OK", "Reparación", "OK"]}))

def vista_punto_libre():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Cálculo de Punto Libre</h2></div>', unsafe_allow_html=True)
    st.latex(r"L = \frac{Et \times Est \times 10^6}{P_2 - P_1}")
    c1, c2 = st.columns(2)
    with c1:
        et = st.selectbox("Varilla:", [0.751, 1.022, 1.336])
        p1 = st.number_input("P1 (lbs)", 15000); p2 = st.number_input("P2 (lbs)", 30000)
        est = st.number_input("Estiramiento (pulg)", 10.0)
    with c2:
        if p2 > p1:
            res = ((est * et * 1000000) / (p2 - p1)) * 0.3048
            st.metric("Profundidad Atrapada", f"{res:.2f} m")

def vista_well_control():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.markdown('<div class="modulo-header"><h2>Well Control & Hidrostática</h2></div>', unsafe_allow_html=True)
    st.latex(r"P_h = 0.052 \times \rho \times TVD[ft]")
    dens = st.number_input("Densidad (ppg)", 9.5)
    tvd = st.number_input("TVD (m)", 1500)
    st.metric("P. Hidrostática", f"{0.052 * dens * (tvd * 3.281):.0f} PSI")

def vista_ranking():
    header_app()
    if st.button("⬅️ Volver"): st.session_state['pantalla'] = 'dashboard'; st.rerun()
    st.table(st.session_state['ranking'].sort_values("Puntaje", ascending=False))

def vista_diploma():
    header_app()
    if st.button("⬅️ Volver al Panel"): 
        st.session_state['pantalla'] = 'dashboard'
        st.rerun()
    
    # Verificación de puntaje para otorgar el certificado
    user_name = st.session_state['user']['nombre']
    user_data = st.session_state['ranking'][st.session_state['ranking']['Operador'] == user_name]
    puntaje = user_data['Puntaje'].max() if not user_data.empty else 0
    
    if puntaje >= 1500:
        st.balloons()
        # Estructura del Diploma con Estilo Institucional
        st.markdown(f"""
        <div style="
            border: 15px double #00457C; 
            padding: 50px; 
            text-align: center; 
            background-color: white; 
            color: #333;
            font-family: 'Georgia', serif;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        ">
            <h1 style="color: #00457C; margin-bottom: 5px;">IPCL MENFA</h1>
            <p style="font-style: italic; font-size: 1.2em;">Instituto Privado de Capacitación Laboral - Mendoza</p>
            <hr style="width: 50%; border: 1px solid #00457C;">
            <br>
            <p style="font-size: 1.5em;">Certifica que el Operador:</p>
            <h2 style="font-size: 2.5em; text-transform: uppercase; text-decoration: underline;">{user_name}</h2>
            <br>
            <p style="font-size: 1.2em; line-height: 1.6;">
                Ha cumplido satisfactoriamente con las exigencias teóricas y prácticas del<br>
                <b>Simulador de Perforación y Well Control (Nivel I)</b>,<br>
                demostrando competencia en maniobras de cierre de pozo y cálculos de ingeniería.
            </p>
            <br><br>
            <div style="display: flex; justify-content: space-around; margin-top: 50px;">
                <div style="border-top: 2px solid #333; width: 200px; padding-top: 10px;">
                    <p><b>Instructor Fabricio</b><br>Especialista Técnico</p>
                </div>
                <div style="border-top: 2px solid #333; width: 200px; padding-top: 10px;">
                    <p><b>Dirección IPCL</b><br>MENFA Mendoza</p>
                </div>
            </div>
            <br>
            <p style="font-size: 0.8em; color: gray;">Emitido el {time.strftime("%d/%m/%Y")} | Código de Validación: MENFA-{random.randint(1000,9999)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Opción para que el alumno guarde su mérito
        st.info("💡 Podés imprimir esta pantalla o guardarla como PDF para tu legajo personal.")
    else:
        st.warning(f"⚠️ El certificado aún no está disponible. Se requieren 1500 puntos (actualmente tenés {puntaje}). ¡Seguí operando en el simulador!")

# --- 5. RUTEADOR PRINCIPAL (EL MOTOR) ---
if not st.session_state['auth']:
    vista_registro()
else:
    pantalla = st.session_state['pantalla']
    if pantalla == 'dashboard': vista_dashboard()
    elif pantalla == 'legajo': vista_legajo()
    elif pantalla == 'simulador': vista_simulador_operativo()
    elif pantalla == 'herramientas': vista_herramientas()
    elif pantalla == 'punto_libre': vista_punto_libre()
    elif pantalla == 'well_control': vista_well_control()
    elif pantalla == 'ranking': vista_ranking()
    elif pantalla == 'diploma': vista_diploma()
