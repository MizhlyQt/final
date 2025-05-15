import streamlit as st

# 🔧 Inicializar variables de sesión ANTES de usarlas
if 'modo' not in st.session_state:
    st.session_state.modo = ""
if 'luces' not in st.session_state:
    st.session_state.luces = "#ffffff"
if 'musica' not in st.session_state:
    st.session_state.musica = False
if 'volumen' not in st.session_state:
    st.session_state.volumen = 50
if 'pelicula' not in st.session_state:
    st.session_state.pelicula = ""
if 'playlist' not in st.session_state:
    st.session_state.playlist = ""

# ✅ Ya puedes usar las variables
st.header("🎛️ Personalización manual")
color = st.color_picker("Selecciona el color de las luces", st.session_state.luces)
volumen = st.slider("Volumen", 0, 100, st.session_state.volumen)
playlist = st.selectbox("Playlist", ["Jazz", "Pop", "Cine", "Rock"], 
                        index=["Jazz", "Pop", "Cine", "Rock"].index(st.session_state.playlist or "Jazz"))
pelicula = st.selectbox("Película", ["Inception", "Matrix", "Frozen", "Top Gun"],
                        index=["Inception", "Matrix", "Frozen", "Top Gun"].index(st.session_state.pelicula or "Inception"))

if st.button("Aplicar configuración"):
    st.session_state.luces = color
    st.session_state.volumen = volumen
    st.session_state.playlist = playlist
    st.session_state.pelicula = pelicula
    st.success("✅ Configuración aplicada")

st.divider()

# Función para mostrar el estado (puedes copiarla desde la página 1 si no está acá)
def mostrar_estado():
    st.markdown(f"**Modo actual:** {st.session_state.modo}")
    st.markdown(f"**Color luces:** {st.session_state.luces}")
    st.markdown(f"**Música activa:** {'Sí' if st.session_state.musica else 'No'}")
    st.markdown(f"**Volumen:** {st.session_state.volumen}")
    st.markdown(f"**Película:** {st.session_state.pelicula}")
    st.markdown(f"**Playlist:** {st.session_state.playlist}")

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
Pantalla -> {st.session_state.pelicula} | Volumen: {st.session_state.volumen}
""", language="text")

st.info("Puedes conectar esto a WOKWI con MQTT para simular los dispositivos reales")
