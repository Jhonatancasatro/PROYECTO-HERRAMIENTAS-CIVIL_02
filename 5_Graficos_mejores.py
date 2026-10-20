import pandas as pd
import plotly.express as px

# Cargar el dataset, normalizar encabezados y eliminar filas duplicadas
df = pd.read_csv("dataset.csv", sep=";")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir las variables del dataset usando los nombres exactos de tu dataset
fc = "Compressive Strength (28-day)(Mpa)"
cemento = "Cement"
escoria = "Slag"
ceniza = "Fly ash"
agua = "Water"
superplastificante = "SP"
agregado_grueso = "Coarse Aggr."
agregado_fino = "Fine Aggr."

# Crear el diagrama 3D interactivo
fig = px.scatter_3d(
    df,
    x=agua,
    y=cemento,
    z=fc,
    color=fc,
    color_continuous_scale="Viridis",
    opacity=0.8,
    hover_data=[escoria, ceniza, superplastificante, agregado_grueso, agregado_fino],
    title="Diagrama 3D Avanzado: Agua, Cemento y Resistencia del Concreto",
    labels={
        agua: "Agua (kg/m³)",
        cemento: "Cemento (kg/m³)",
        fc: "Resistencia a la compresión (MPa)",
    },
)

# Ajustar tamaño de puntos y la escena 3D
fig.update_traces(marker={"size": 5})
fig.update_layout(
    scene={
        "xaxis_title": "Agua (kg/m³)",
        "yaxis_title": "Cemento (kg/m³)",
        "zaxis_title": "Resistencia (MPa)",
        "camera": {"eye": {"x": 1.6, "y": 1.6, "z": 1.2}},
    },
    coloraxis_colorbar={"title": "Resistencia (MPa)"},
)

# Mostrar el gráfico interactivo
fig.show()