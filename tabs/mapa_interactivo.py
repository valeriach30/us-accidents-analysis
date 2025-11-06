# Tab de Mapa Interactivo

import streamlit as st
import pandas as pd
import pydeck as pdk

# Mostrar mapas interactivos con PyDeck
# df: DataFrame con los datos de accidentes
def show_mapa_interactivo(df: pd.DataFrame):
    st.markdown("### 🗺️ Visualización Geoespacial")
    
    # Controles del mapa
    col1, col2 = st.columns(2)
    
    with col1:
        # Límite de puntos para el mapa
        max_points = st.slider("📍 Máximo de puntos en el mapa", 1000, 1000000, 15000, 1000)
    
    with col2:
        # Colorear por severidad
        color_by = st.selectbox("🎨 Colorear por", ["Severidad", "Temperatura", "Visibilidad"])
    
    # Tomar muestra para el mapa y limpiar valores nulos
    df_mapa = df.sample(n=min(max_points, len(df)), random_state=42).copy()
    
    # Limpiar valores NaN que pueden causar errores en el mapa
    df_mapa = df_mapa.dropna(subset=['Start_Lat', 'Start_Lng', 'Severity'])
    
    # Rellenar valores NaN en otras columnas con valores por defecto
    if 'Temperature(F)' in df_mapa.columns:
        df_mapa['Temperature(F)'].fillna(df_mapa['Temperature(F)'].median(), inplace=True)
    if 'Visibility(mi)' in df_mapa.columns:
        df_mapa['Visibility(mi)'].fillna(df_mapa['Visibility(mi)'].median(), inplace=True)
    
    st.info(f"🗺️ Mostrando {len(df_mapa):,} puntos en el mapa")
    
   
    # ==================== MAPA DE DISPERSIÓN ====================
    
    # Configurar colores según la opción seleccionada
    if color_by == "Severidad":
        # Mapa de colores por severidad
        color_map = {
            1: [0, 255, 0, 160],    # Verde
            2: [255, 255, 0, 160],  # Amarillo
            3: [255, 165, 0, 160],  # Naranja
            4: [255, 0, 0, 160]     # Rojo
        }
        df_mapa['color'] = df_mapa['Severity'].apply(
            lambda x: color_map.get(x, [128, 128, 128, 160])
        )
        
    elif color_by == "Temperatura":
        # Normalizar temperatura a colores
        temp_col = df_mapa['Temperature(F)']
        temp_min = temp_col.min()
        temp_max = temp_col.max()
        
        if pd.notna(temp_min) and pd.notna(temp_max) and temp_max > temp_min:
            # Normalizar entre 0 y 1
            temp_norm = (temp_col - temp_min) / (temp_max - temp_min)
            # Crear colores (azul=frío, rojo=calor)
            df_mapa['color'] = temp_norm.apply(
                lambda x: [int(255*x) if pd.notna(x) else 128, 
                            100, 
                            int(255*(1-x)) if pd.notna(x) else 128, 
                            160]
            )
        else:
            # Color por defecto si no hay rango válido
            df_mapa['color'] = [[100, 100, 255, 160] for _ in range(len(df_mapa))]

    # Visibilidad   
    else:
        vis_col = df_mapa['Visibility(mi)']
        vis_max = vis_col.max()
        
        if pd.notna(vis_max) and vis_max > 0:
            # Normalizar visibilidad entre 0 y 1
            vis_norm = vis_col / vis_max
            # Crear colores más claros: rojo (baja) → amarillo (media) → verde (alta)
            df_mapa['color'] = vis_norm.apply(
                lambda x: [
                    int(255 * (1 - x)) if pd.notna(x) else 128,  # Rojo disminuye con más visibilidad
                    int(255 * min(2*x, 2*(1-x))) if pd.notna(x) else 128,  # Amarillo en el medio
                    int(255 * x) if pd.notna(x) else 128,  # Verde aumenta con más visibilidad
                    200  # Más opaco para mejor visibilidad
                ]
            )
        else:
            # Color por defecto
            df_mapa['color'] = [[100, 255, 100, 160] for _ in range(len(df_mapa))]
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_mapa,
        get_position=["Start_Lng", "Start_Lat"],
        get_color="color",
        get_radius=300,
        pickable=True,
        opacity=0.6,
        stroked=True,
        filled=True,
        radius_min_pixels=2,
        radius_max_pixels=10,
    )
    
    view_state = pdk.ViewState(
        latitude=37.0902,
        longitude=-95.7129,
        zoom=4,
        pitch=0,
        bearing=0,
        min_zoom=2,
        max_zoom=15,
    )
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Severidad:</b> {Severity}<br/>"
                    "<b>Ciudad:</b> {City}<br/>"
                    "<b>Estado:</b> {State}<br/>"
                    "<b>Temperatura:</b> {Temperature(F)}°F",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        },
        map_style='road',
    )
    
    st.pydeck_chart(r, use_container_width=True)
    
    # Leyendas
    st.markdown("---")

    st.markdown("#### 🎨 Leyenda de Colores")
    if color_by == "Severidad":
        st.markdown("""
        - 🟢 **Severidad 1** (Leve) - Demoras cortas
        - 🟡 **Severidad 2** (Moderada) - Demoras moderadas
        - 🟠 **Severidad 3** (Grave) - Demoras significativas
        - 🔴 **Severidad 4** (Muy Grave) - Demoras prolongadas
        """)
    elif color_by == "Temperatura":
        st.markdown("**Gradiente de temperatura:**")
        st.markdown("""
        - 🔵 Azul = Frío
        - 🟣 Morado = Templado
        - 🔴 Rojo = Calor
        """)
    else:
        st.markdown("**Gradiente de visibilidad:**")
        st.markdown("""
        - 🔴 Rojo = Baja Visibilidad
        - 🟡 Amarillo = Media
        - 🟢 Verde = Alta Visibilidad
        """)
