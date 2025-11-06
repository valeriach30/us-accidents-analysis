import streamlit as st

# Configuración de la página Streamlit
def setup_page_config():
    st.set_page_config(
        page_title="Análisis Geoespacial de Accidentes de Tránsito - Estados Unidos",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Aplicar CSS personalizado
def apply_custom_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            padding: 1rem 0;
        }
        .section-header {
            font-size: 2rem;
            color: #ff7f0e;
            border-bottom: 2px solid #ff7f0e;
            padding-bottom: 0.5rem;
            margin: 1rem 0;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .stAlert {
            margin-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
