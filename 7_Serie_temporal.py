import pandas as pd
import plotly.express as px

# Cargar el dataset, limpiar encabezados y eliminar filas duplicadas
df = pd.read_csv("dataset.csv", sep=";")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo y las columnas reales de tu dataset
fc = "Compressive Strength (28-day)(Mpa)"
cemento = "Cement"
agua = "Water"

# Ordenar el dataset por la cantidad de cemento para una mejor visualización de la línea
df_ordenado = df.sort_values(by=cemento)

# Crear un gráfico de líneas interactivo con marcadores
fig = px.line(
    df_ordenado,
    x=cemento,
    y=fc,
    markers=True,
    hover_data=[agua],
    title="Tendencia: Contenido de Cemento vs Resistencia a la Compresión",
    labels={
        cemento: "Cemento (kg/m³)",
        fc: "Resistencia (MPa)",
    },
)

# Ajustar el tamaño de los puntos
fig.update_traces(marker={"size": 6})

# Mostrar el gráfico interactivo
fig.show()