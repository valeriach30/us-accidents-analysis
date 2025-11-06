import streamlit as st
from data_manager import get_data_manager
from config import setup_page_config, apply_custom_css

def main():
    # Configurar página y estilos
    setup_page_config()
    apply_custom_css()
    
    # Título principal
    st.markdown('<h1 class="main-header">🚗 Análisis Geoespacial de Accidentes de Tránsito en Estados Unidos</h1>', unsafe_allow_html=True)
    
    # Información del proyecto
    with st.expander("📋 Información del Proyecto"):
        st.markdown("""
        **Estudiantes:** Darío Zamora Rojas, Valeria Chinchilla Mejías  
        **Fuente de datos:** [Kaggle - US Accidents Dataset](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) - [Archivo pre-filtrado en Google Drive](https://drive.google.com/file/d/1_T0CVP34NUlWyyYBjgdzTr32dLv6fpQu/view?usp=sharing)
        **Período:** 2020-2023 (muestra optimizada)  
        
        ---
        
        ### 🏗️ Arquitectura Modular
        
        Esta aplicación estará organizada en módulos independientes:
        - 📍 **Geoespacial**: Análisis de distribución geográfica
        - 🌤️ **Climático**: Relación entre clima y accidentes
        - ⏰ **Temporal**: Patrones de tiempo y horarios
        - 🛣️ **Infraestructura**: Análisis de elementos viales
        - 📊 **Dashboard**: Métricas generales y KPIs
        - 🗺️ **Mapas Avanzados**: Visualizaciones interactivas 3D
        """)
    
    # Inicializar datos 
    data_manager = get_data_manager()

    # Sidebar para filtros
    st.sidebar.markdown("## 🎛️ Filtros de Análisis")
    
    # Control de rendimiento
    st.sidebar.markdown("### ⚡ Configuración de rendimiento")
    
    performance_mode = st.sidebar.selectbox(
        "Modo de Rendimiento",
        ["🚀 Rápido (100k registros)", "⚖️ Balanceado (500k registros)", "🐌 Completo (1M registros)"],
        help="Controla la cantidad de datos que se van a procesar para optimizar rendimiento"
    )
    
    # Configurar límites según el modo
    if "Rápido" in performance_mode:
        sample_size = 100000
        warning_msg = "🚀 Modo rápido: Procesando 100k registros"
    elif "Balanceado" in performance_mode:
        sample_size = 500000
        warning_msg = "⚖️ Modo balanceado: Procesando 500k registros"
    else:
        sample_size = None  # Cargar todo (1M)
        warning_msg = "🐌 Modo completo: Procesando 1M registros)"
    
    st.sidebar.warning(warning_msg)
    
    # Botón para cargar datos
    if st.sidebar.button("📊 Cargar Dataset", type="primary"):
        st.session_state.data_loaded = True
        st.session_state.sample_size = sample_size
        # Limpiar cache cuando se cambia el modo de rendimiento
        if 'cached_sample_size' not in st.session_state or st.session_state.cached_sample_size != sample_size:
            st.cache_data.clear()
            st.session_state.cached_sample_size = sample_size
    
    # Verificar si los datos están cargados
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

    # Preguntas de investigación
    if not st.session_state.data_loaded:
        with st.expander("🔍 Preguntas de Investigación", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                #### 📍 **Análisis Geoespacial**
                - ¿Dónde se concentran más los accidentes?
                - ¿Qué estados tienen mayor severidad promedio?
                - ¿Existe correlación geográfica en los patrones?
                
                #### ⏰ **Análisis Temporal**
                - ¿En qué horarios ocurren más accidentes?
                - ¿Hay diferencias por día de la semana?
                - ¿Cómo ha evolucionado la tendencia anual?
                """)
            
            with col2:
                st.markdown("""
                #### 🌤️ **Factores Climáticos**
                - ¿Cómo influye el clima en la severidad?
                - ¿La visibilidad afecta la frecuencia de accidentes?
                - ¿Qué condiciones meteorológicas son más peligrosas?
                
                #### 🛣️ **Infraestructura Vial**
                - ¿Los semáforos reducen los accidentes graves?
                - ¿Qué elementos de infraestructura son más críticos?
                - ¿Las rotondas son más seguras que las intersecciones?
                """)
        
        return
    
    # Cargar datos con límite según modo de rendimiento
    sample_size = st.session_state.get('sample_size', 100000)
    
    with st.spinner(f'📊 Cargando {"todos los" if sample_size is None else f"{sample_size:,}"} registros del dataset...'):
        df = data_manager.load_data(sample_size=sample_size)
    
    if df is None or df.empty:
        st.error("❌ No se pudo cargar el dataset. Verificar conexión a internet.")
        return
    
    # Mostrar información sobre los datos cargados
    st.success(f"✅ **Datos cargados exitosamente**: {len(df):,} registros procesados")

if __name__ == "__main__":
    main()