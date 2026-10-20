from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.linear_model import LinearRegression

# Configuración de la página del dashboard
st.set_page_config(
    page_title="Dashboard de resistencia del concreto",
    page_icon="🏗️",
    layout="wide",
)

# Definir la ruta del dataset local (dataset.csv)
DATASET = Path(__file__).resolve().parent / "dataset.csv"

# Variables adaptadas a los nombres exactos de tus columnas
FC = "Compressive Strength (28-day)(Mpa)"
COMPONENTES = {
    "Cemento": "Cement",
    "Escoria": "Slag",
    "Ceniza volante": "Fly ash",
    "Agua": "Water",
    "Superplastificante": "SP",
    "Agregado grueso": "Coarse Aggr.",
    "Agregado fino": "Fine Aggr.",
}

# Título principal del Dashboard
st.title("Dashboard de resistencia del concreto")
st.caption("Indicadores, análisis de mezclas y predicción de resistencia")

# Validar si existe el archivo
if not DATASET.is_file():
    st.error(f"No se encontró el archivo del dataset: {DATASET}")
    st.stop()

# Cargar el dataset considerando el separador correcto (punto y coma o coma según Excel)
try:
    df = pd.read_csv(DATASET, sep=";")
    if len(df.columns) <= 1:
        df = pd.read_csv(DATASET, sep=",")
except Exception:
    df = pd.read_csv(DATASET)

df.columns = df.columns.str.strip()

# Validar columnas requeridas
columnas_requeridas = [FC, *COMPONENTES.values()]
faltantes = [col for col in columnas_requeridas if col not in df.columns]
if faltantes:
    st.error(
        "Faltan columnas requeridas en el archivo CSV: " + ", ".join(faltantes)
    )
    st.stop()

# Limpieza de datos (eliminar duplicados)
filas_originales = len(df)
df = df.drop_duplicates().copy()
duplicados_eliminados = filas_originales - len(df)

# Barra lateral (Sidebar) con estadísticas generales
with st.sidebar:
    st.header("Datos")
    st.write(f"Registros cargados: {filas_originales:,}")
    st.write(f"Duplicados excluidos: {duplicados_eliminados:,}")
    st.write(f"Registros analizados: {len(df):,}")
    st.caption("Los análisis excluyen filas idénticas en todas sus columnas.")

# Estadísticas de la resistencia
media = df[FC].mean()
mediana = df[FC].median()
moda = df[FC].mode().iloc[0]
desviacion_estandar = df[FC].std()

# Pestañas principales del Dashboard
tab_resumen, tab_distribucion, tab_mezclas, tab_correlaciones, tab_modelo = (
    st.tabs(
        [
            "Resumen",
            "Distribución",
            "Mezclas y componentes",
            "Correlaciones",
            "Modelo predictivo",
        ]
    )
)

# 1. PESTAÑA: RESUMEN (KPIs)
with tab_resumen:
    st.subheader("Indicadores clave (KPIs)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Resistencia Promedio", f"{media:.2f} MPa")
    kpi2.metric("Mediana", f"{mediana:.2f} MPa")
    kpi3.metric("Moda", f"{moda:.2f} MPa")
    kpi4.metric("Desviación Estándar", f"{desviacion_estandar:.2f} MPa")

    st.markdown("---")
    st.subheader("Vista previa de los datos limpios")
    st.dataframe(df.head(10), use_container_width=True)

# 2. PESTAÑA: DISTRIBUCIÓN
with tab_distribucion:
    st.subheader("Distribución de la Resistencia a la Compresión")
    fig_hist = px.histogram(
        df,
        x=FC,
        nbins=20,
        title="Histograma de Resistencia (28 días)",
        labels={FC: "Resistencia (MPa)"},
        color_discrete_sequence=["#1f77b4"],
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# 3. PESTAÑA: MEZCLAS Y COMPONENTES
with tab_mezclas:
    st.subheader("Gráfico 3D interactivo de la mezcla")
    componente_x = st.selectbox(
        "Selecciona Eje X:", list(COMPONENTES.keys()), index=3
    )  # Agua por defecto
    componente_y = st.selectbox(
        "Selecciona Eje Y:", list(COMPONENTES.keys()), index=0
    )  # Cemento por defecto

    fig_3d = px.scatter_3d(
        df,
        x=COMPONENTES[componente_x],
        y=COMPONENTES[componente_y],
        z=FC,
        color=FC,
        color_continuous_scale="Viridis",
        opacity=0.8,
        title=f"Relación 3D: {componente_x} vs {componente_y} vs Resistencia",
        labels={
            COMPONENTES[componente_x]: componente_x,
            COMPONENTES[componente_y]: componente_y,
            FC: "Resistencia (MPa)",
        },
    )
    fig_3d.update_traces(marker={"size": 5})
    st.plotly_chart(fig_3d, use_container_width=True)

# 4. PESTAÑA: CORRELACIONES
with tab_correlaciones:
    st.subheader("Mapa de calor de correlaciones")
    cols_corr = [FC, *COMPONENTES.values()]
    matriz_corr = df[cols_corr].corr()

    fig_corr = px.imshow(
        matriz_corr,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="Blues",
        title="Matriz de Correlación de Variables",
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# 5. PESTAÑA: MODELO PREDICTIVO
with tab_modelo:
    st.subheader("Modelo de Regresión Lineal")

    # Entrenamiento del modelo usando Cemento como predictor principal
    X = df[["Cement"]]
    y = df[FC]

    modelo = LinearRegression()
    modelo.fit(X, y)
    r2 = modelo.score(X, y)

    st.write(f"**Coeficiente de determinación ($R^2$):** {r2:.4f}")

    # Simulador interactivo para predecir resistencia
    st.markdown("### Simulador de resistencia")
    cemento_input = st.slider(
        "Cantidad de Cemento (kg/m³)",
        float(df["Cement"].min()),
        float(df["Cement"].max()),
        float(df["Cement"].mean()),
    )

    prediccion = modelo.predict([[cemento_input]])[0]
    st.success(
        f"Resistencia estimada para **{cemento_input:.1f} kg/m³** de cemento: **{prediccion:.2f} MPa**"
    )