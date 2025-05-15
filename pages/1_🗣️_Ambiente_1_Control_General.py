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
