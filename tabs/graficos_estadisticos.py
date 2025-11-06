# Tab de Gráficos Estadísticos

import streamlit as st
import pandas as pd
import plotly.express as px

# Mostrar gráficos estadísticos interactivos
# df : DataFrame con los datos de accidentes
def show_graficos_estadisticos(df: pd.DataFrame):
    st.markdown("### 📈 Análisis Estadístico")
 