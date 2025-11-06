"""
Gestor de datos para el análisis de accidentes de tránsito en Estados Unidos
Optimizado para manejar datasets grandes con Polars y GeoPandas
"""

import streamlit as st
import pandas as pd
import polars as pl
import geopandas as gpd
import gdown
from pathlib import Path
import os
from typing import Optional, Tuple
import numpy as np

# Gestor de datos
class DataManager:    
    # Archivo pre-filtrado en Google Drive
    GDRIVE_FILE_ID = "1_T0CVP34NUlWyyYBjgdzTr32dLv6fpQu"
    GDRIVE_URL = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    
    def __init__(self):
        self.data_path = "us_accidents.csv"
        self.df = None
        self.gdf = None
    
    # Descargar dataset
    @st.cache_data
    def download_dataset(_self) -> str:
        with st.spinner("Descargando dataset desde Google Drive..."):
            try:
                output_path = _self.data_path
                
                # Descargar solo si no existe
                if not os.path.exists(output_path):
                    gdown.download(_self.GDRIVE_URL, output_path, quiet=False)

                return output_path
            except Exception as e:
                st.error(f"❌ Error descargando dataset: {str(e)}")
                return None
    
    # Cargar datos
    @st.cache_data
    def load_data(_self, force_reload: bool = False, sample_size: Optional[int] = None) -> pd.DataFrame:
        # Descargar dataset si no existe localmente
        csv_file = _self.download_dataset()
        if csv_file is None:
            st.error("❌ Error: no se pudo descargar el archivo CSV")
            return None
        
        with st.spinner("Cargando dataset..."):
            try:
                # Leer con Polars
                df_pl = pl.read_csv(csv_file)
                
                # Disminuir tamaño si se especifica sample_size
                if sample_size is not None and sample_size < len(df_pl):
                    df_pl = df_pl.sample(n=sample_size, seed=42)
                    st.warning(f"📊 Muestra tomada: {sample_size:,} registros para optimizar rendimiento")
                
                # Convertir a Pandas para compatibilidad con GeoPandas y Streamlit
                df = df_pl.to_pandas()
                
                # Procesamiento de fechas y columnas
                df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
                df['Hour'] = df['Start_Time'].dt.hour
                df['Day_of_Week'] = df['Start_Time'].dt.day_name()
                df['Month'] = df['Start_Time'].dt.month
                df['Year'] = df['Start_Time'].dt.year
                
                st.success(f"✅ Dataset procesado: {len(df):,} registros de {df['State'].nunique()} estados")
                return df
                
            except Exception as e:
                st.error(f"Error cargando dataset: {str(e)}")
                return None

    # Crear GeoDataFrame
    @st.cache_data
    def create_geodataframe(_self, df: pd.DataFrame) -> gpd.GeoDataFrame:
        if df is None or df.empty:
            return None
        
        try:
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df['Start_Lng'], df['Start_Lat']),
                crs="EPSG:4326"
            )
            return gdf
        except Exception as e:
            st.error(f"Error creando GeoDataFrame: {str(e)}")
            return None
    
    # Resumen de datos
    def get_data_summary(self, df: pd.DataFrame) -> dict:
        if df is None or df.empty:
            return {}
        
        summary = {
            'total_accidents': len(df),
            'date_range': f"{df['Start_Time'].min().strftime('%Y-%m-%d')} a {df['Start_Time'].max().strftime('%Y-%m-%d')}",
            'states_count': df['State'].nunique(),
            'cities_count': df['City'].nunique(),
            'severity_distribution': df['Severity'].value_counts().to_dict(),
            'most_common_weather': df['Weather_Condition'].value_counts().head().to_dict(),
            'avg_temperature': round(df['Temperature(F)'].mean(), 2) if 'Temperature(F)' in df.columns else 'N/A'
        }
        
        return summary
    
    # Filtros de datos
    def filter_data(self, df: pd.DataFrame, **filters) -> pd.DataFrame:
        if df is None or df.empty:
            return df
        
        filtered_df = df.copy()
        
        # Filtro por severidad
        if 'severity' in filters and filters['severity']:
            filtered_df = filtered_df[filtered_df['Severity'].isin(filters['severity'])]
        
        # Filtro por estado
        if 'states' in filters and filters['states']:
            filtered_df = filtered_df[filtered_df['State'].isin(filters['states'])]
        
        # Filtro por año
        if 'years' in filters and filters['years']:
            filtered_df = filtered_df[filtered_df['Year'].isin(filters['years'])]
        
        # Filtro por condición climática
        if 'weather' in filters and filters['weather']:
            filtered_df = filtered_df[filtered_df['Weather_Condition'].isin(filters['weather'])]
        
        return filtered_df


# Función para inicializar el gestor de datos
@st.cache_resource
def get_data_manager():
    return DataManager()