# 🚗 Análisis Geoespacial de Accidentes de Tránsito en Estados Unidos

### 👥 Estudiantes

- Darío Zamora Rojas
- Valeria Chinchilla Mejías

### 🎯 Objetivos del Análisis

La aplicación está diseñada para responder cuatro preguntas principales de investigación:

1. **📍 ¿Dónde ocurren más accidentes y con qué severidad?**

   - Identificación de puntos geográficos con mayor concentración de accidentes
   - Análisis de diferencias regionales entre estados
   - Visualización de distribución de severidad (escala 1-4)

2. **🌤️ ¿Qué relación existe entre las condiciones climáticas y los accidentes?**

   - Evaluación del impacto de diferentes condiciones climáticas
   - Análisis de variables como precipitación, temperatura y visibilidad
   - Correlación entre clima y severidad de accidentes

3. **⏰ ¿En qué horarios o momentos del día se reportan más accidentes?**

   - Identificación de patrones horarios y semanales
   - Comparación entre días laborales y fines de semana
   - Análisis de tendencias temporales por año

4. **🛣️ ¿Qué papel juega la infraestructura vial cercana?**
   - Análisis de distribución geográfica de accidentes
   - Patrones de concentración por estado y ciudad
   - Evaluación de severidad promedio por región

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- pip (gestor de paquetes)

### Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/valeriach30/us-accidents-analysis.git
cd us-accidents-analysis
```

2. **Crear entorno virtual (recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

### 🎮 Ejecución

```bash
streamlit run app.py
```

La aplicación estará disponible en: `http://localhost:8501`

## 📊 Estructura del Proyecto

```
us-accidents-analysis/
├── app.py                      # Aplicación principal de Streamlit
├── data_manager.py             # Gestor de datos y optimizaciones
├── config.py                   # Configuración de página y estilos CSS
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación del proyecto
├── .gitignore                  # Archivos ignorados por Git
└── tabs/                       # Módulos de visualización
    ├── __init__.py             # Inicialización del paquete
    ├── tabla_interactiva.py    # Tab de exploración de datos
    ├── graficos_estadisticos.py # Tab de visualizaciones estadísticas
    └── mapa_interactivo.py     # Tab de mapas geoespaciales
```

## 📚 Dataset

**Fuente**: [US-Accidents Dataset en Kaggle](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)

### Características del Dataset Procesado:

- **Período**: 2020-2023 (optimizado para rendimiento)
- **Registros disponibles**: Hasta 1,000,000 según modo de rendimiento
- **Cobertura**: Estados Unidos continental
- **Archivo**: CSV pre-filtrado en Google Drive (descarga automática)

### Variables Principales:

- **Geoespaciales**:
  - `Start_Lat`, `Start_Lng` - Coordenadas del accidente
  - `City`, `State` - Ubicación administrativa
- **Temporales**:

  - `Start_Time` - Fecha y hora del inicio
  - `Hour` - Hora del día (0-23)
  - `Day_of_Week` - Día de la semana
  - `Month`, `Year` - Mes y año

- **Severidad**:

  - `Severity` - Escala 1-4 basada en impacto en tráfico

- **Climáticas**:

  - `Temperature(F)` - Temperatura en Fahrenheit
  - `Visibility(mi)` - Visibilidad en millas
  - `Weather_Condition` - Descripción de condición climática

- **Otras**:
  - `Distance(mi)` - Distancia afectada por el accidente
