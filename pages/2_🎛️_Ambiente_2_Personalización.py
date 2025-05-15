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
