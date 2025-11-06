# Tab de Gráficos Estadísticos

import streamlit as st
import pandas as pd
import plotly.express as px

# Mostrar gráficos estadísticos interactivos
# df : DataFrame con los datos de accidentes
def show_graficos_estadisticos(df: pd.DataFrame):
    st.markdown("### 📈 Análisis Estadístico")
    
    # Subtabs para diferentes tipos de gráficos
    subtab1, subtab2, subtab3 = st.tabs(["Severidad", "Temporal", "Climático"])
    
    # ==================== SUBTAB 1: SEVERIDAD ====================
    with subtab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras: Distribución por Severidad
            st.markdown("#### 🚨 Distribución por Severidad")
            severity_counts = df['Severity'].value_counts().sort_index()
            fig_severity = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                labels={'x': 'Nivel de Severidad', 'y': 'Cantidad de Accidentes'},
                color=severity_counts.values,
                color_continuous_scale='Reds',
                text=severity_counts.values
            )
            fig_severity.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_severity.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_severity, use_container_width=True)
        
        with col2:
            # Gráfico de pie: Top 10 Estados
            st.markdown("#### 🗺️ Top 10 Estados con Más Accidentes")
            top_states = df['State'].value_counts().head(10)
            fig_states = px.pie(
                values=top_states.values,
                names=top_states.index,
                hole=0.4
            )
            fig_states.update_traces(textposition='inside', textinfo='percent+label')
            fig_states.update_layout(height=400)
            st.plotly_chart(fig_states, use_container_width=True)
    
    # ==================== SUBTAB 2: TEMPORAL ====================
    with subtab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de líneas: Accidentes por Hora del Día
            st.markdown("#### ⏰ Accidentes por Hora del Día")
            hourly = df['Hour'].value_counts().sort_index()
            fig_hourly = px.line(
                x=hourly.index,
                y=hourly.values,
                labels={'x': 'Hora del Día', 'y': 'Cantidad de Accidentes'},
                markers=True
            )
            fig_hourly.update_traces(line_color='#1f77b4', line_width=3)
            fig_hourly.update_layout(height=400)
            st.plotly_chart(fig_hourly, use_container_width=True)
        
        with col2:
            # Gráfico de barras: Accidentes por Día de la Semana
            st.markdown("#### 📅 Accidentes por Día de la Semana")
            dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = df['Day_of_Week'].value_counts().reindex(dias_orden)
            fig_days = px.bar(
                x=day_counts.index,
                y=day_counts.values,
                labels={'x': 'Día de la Semana', 'y': 'Cantidad de Accidentes'},
                color=day_counts.values,
                color_continuous_scale='Blues'
            )
            fig_days.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_days, use_container_width=True)
    
    # ==================== SUBTAB 3: CLIMÁTICO ====================
    with subtab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma: Distribución de Temperatura
            st.markdown("#### 🌡️ Distribución de Temperatura")
            fig_temp = px.histogram(
                df,
                x='Temperature(F)',
                nbins=50,
                labels={'Temperature(F)': 'Temperatura (°F)'},
                color_discrete_sequence=['#ff7f0e']
            )
            fig_temp.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            # Top 10 Condiciones Climáticas
            st.markdown("#### 🌤️ Top 10 Condiciones Climáticas")
            top_weather = df['Weather_Condition'].value_counts().head(10)
            fig_weather = px.bar(
                x=top_weather.values,
                y=top_weather.index,
                orientation='h',
                labels={'x': 'Cantidad de Accidentes', 'y': 'Condición Climática'},
                color=top_weather.values,
                color_continuous_scale='Viridis'
            )
            fig_weather.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_weather, use_container_width=True)
