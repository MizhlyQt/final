import streamlit as st

st.set_page_config(page_title="Centro Multimedial")

page_style = """
<style>
/* Fondo principal */
[data-testid="stAppViewContainer"] {
    background-color: #453863;
}

/* Fondo del sidebar */
[data-testid="stSidebar"] {
    background-color: #1f1536;
}

/* Color de todos los textos */
[data-testid="stMarkdownContainer"] {
    color: #ffffff;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

st.title("🎬 Centro de Entretenimiento Inteligente")

st.markdown("""
¡Bienvenid@! Usa el menú lateral para explorar:
- ⏯️ Control por Botones
- 🎛️ Control por Voz
- 📶 Control por Sliders
""")
