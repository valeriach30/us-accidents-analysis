"""
Tab de Tabla Interactiva con filtros
"""

import streamlit as st
import pandas as pd


def show_tabla_interactiva(df: pd.DataFrame):
    """
    Muestra una tabla interactiva con filtros dinámicos
    
    Args:
        df: DataFrame con los datos de accidentes
    """
    st.markdown("### 📊 Exploración de Datos")
    
    # Filtros en columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Filtro por Estado
        estados_disponibles = ['Todos'] + sorted(df['State'].unique().tolist())
        estado_seleccionado = st.selectbox("🗺️ Estado", estados_disponibles, key="tabla_estado")
    
    with col2:
        # Filtro por Severidad
        severidades = ['Todas'] + sorted(df['Severity'].unique().tolist())
        severidad_seleccionada = st.selectbox("🚨 Severidad", severidades, key="tabla_severidad")
    
    with col3:
        # Filtro por Año
        años = ['Todos'] + sorted(df['Year'].unique().tolist(), reverse=True)
        año_seleccionado = st.selectbox("📅 Año", años, key="tabla_año")
    
    with col4:
        # Filtro por Condición Climática (Top 10)
        top_weather = df['Weather_Condition'].value_counts().head(10).index.tolist()
        climas = ['Todas'] + top_weather
        clima_seleccionado = st.selectbox("🌤️ Condición Climática", climas, key="tabla_clima")
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if estado_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['State'] == estado_seleccionado]
    
    if severidad_seleccionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Severity'] == severidad_seleccionada]
    
    if año_seleccionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Year'] == año_seleccionado]
    
    if clima_seleccionado != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Weather_Condition'] == clima_seleccionado]
    
    # Mostrar estadísticas de filtrado
    st.info(f"📊 Mostrando {len(df_filtrado):,} registros de {len(df):,} totales ({len(df_filtrado)/len(df)*100:.1f}%)")
    
    # Seleccionar columnas a mostrar
    columnas_mostrar = ['Start_Time', 'City', 'State', 'Severity', 'Weather_Condition', 
                       'Temperature(F)', 'Visibility(mi)', 'Distance(mi)']
    
    # Mostrar tabla interactiva
    st.dataframe(
        df_filtrado[columnas_mostrar].head(1000),
        use_container_width=True,
        height=400
    )
    
    # Botón de descarga
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos filtrados (CSV)",
        data=csv,
        file_name=f"accidentes_filtrados_{estado_seleccionado}_{año_seleccionado}.csv",
        mime="text/csv",
    )
    
    # Retornar el DataFrame filtrado para que otros tabs puedan usarlo
    return df_filtrado
