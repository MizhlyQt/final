import streamlit as st
import time

# Configuracion inicial
st.set_page_config(page_title="Centro de Entretenimiento Inteligente", layout="centered")
st.title("🎬 Centro de Entretenimiento Inteligente")

# Inicializar estados
if 'modo' not in st.session_state:
    st.session_state.modo = ""
    st.session_state.luces = "#ffffff"
    st.session_state.musica = False
    st.session_state.volumen = 50
    st.session_state.pelicula = ""
    st.session_state.playlist = ""

# --- Ambiente 1: Comandos generales ---
st.header("🎙️ Control por voz o texto")
comando = st.text_input("Escribe un comando (ej: 'modo cine', 'poner música', 'encender luces'):")

if st.button("Ejecutar comando"):
    comando = comando.lower()
    if "cine" in comando:
        st.session_state.modo = "Modo Cine"
        st.session_state.luces = "#222222"
        st.session_state.musica = False
        st.session_state.volumen = 80
        st.session_state.pelicula = "Inception"
    elif "luces" in comando:
        st.session_state.luces = "#ffffff"
    elif "música" in comando:
        st.session_state.musica = True
        st.session_state.playlist = "Pop"

# Mostrar estado actual
def mostrar_estado():
    st.markdown(f"**Modo actual:** {st.session_state.modo}")
    st.markdown(f"**Color luces:** {st.session_state.luces}")
    st.markdown(f"**Música activa:** {'Sí' if st.session_state.musica else 'No'}")
    st.markdown(f"**Volumen:** {st.session_state.volumen}")
    st.markdown(f"**Película:** {st.session_state.pelicula}")
    st.markdown(f"**Playlist:** {st.session_state.playlist}")

st.divider()

# --- Ambiente 2: Personalización ---
st.header("🎛️ Personalización manual")
color = st.color_picker("Selecciona el color de las luces", st.session_state.luces)
volumen = st.slider("Volumen", 0, 100, st.session_state.volumen)
playlist = st.selectbox("Playlist", ["Jazz", "Pop", "Cine", "Rock"])
pelicula = st.selectbox("Película", ["Inception", "Matrix", "Frozen", "Top Gun"])

if st.button("Aplicar configuración"):
    st.session_state.luces = color
    st.session_state.volumen = volumen
    st.session_state.playlist = playlist
    st.session_state.pelicula = pelicula
    st.success("✅ Configuración aplicada")

st.divider()

# --- Estado del sistema ---
st.header("📺 Estado del sistema")
mostrar_estado()

# Simulación WOKWI (teórica)
st.subheader("🔧 Simulación de dispositivos (WOKWI)")
st.markdown("- LED RGB simulado con color de luces")
st.markdown("- Buzzer activo si la música está encendida")
st.markdown("- Pantalla muestra película y volumen")

st.code(f"""
LED RGB -> Color: {st.session_state.luces}
BUZZER -> Estado: {'ON' if st.session_state.musica else 'OFF'}
Pantalla -> {st.session_state.pelicula} | Volumen: {st.session_state.volumen}
""", language="text")

st.info("Puedes conectar esto a WOKWI con MQTT para simular los dispositivos reales")

