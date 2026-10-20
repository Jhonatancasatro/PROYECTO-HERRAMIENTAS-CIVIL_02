import pandas as pd
import plotly.express as px

# Cargar el dataset, limpiar espacios y eliminar filas duplicadas
df = pd.read_csv("dataset.csv", sep=";")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo con el nombre exacto de tu Excel
fc = "Compressive Strength (28-day)(Mpa)"

# Calcular estadísticas descriptivas
media = df[fc].mean()
moda = df[fc].mode().iloc[0]
mediana = df[fc].median()
desviacion_estandar = df[fc].std()

# Crear el histograma de la resistencia del concreto
fig = px.histogram(
    df,
    x=fc,
    nbins=30,
    title="Distribución de la resistencia del concreto (sin filas duplicadas)",
    labels={fc: "Resistencia a la compresión (MPa)"}
)

# Agregar línea vertical para la Media (Rojo)
fig.add_vline(
    x=media,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Media: {media:.2f}",
)

# Agregar línea vertical para la Moda (Verde)
fig.add_vline(
    x=moda,
    line_dash="dot",
    line_color="green",
    annotation_text=f"Moda: {moda:.2f}",
)

# Agregar línea vertical para la Mediana (Azul)
fig.add_vline(
    x=mediana,
    line_dash="dashdot",
    line_color="blue",
    annotation_text=f"Mediana: {mediana:.2f}",
)

# Agregar cuadro de texto con la Desviación Estándar
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0.99,
    y=0.99,
    xanchor="right",
    yanchor="top",
    text=f"Desviación estándar: {desviacion_estandar:.2f} MPa",
    showarrow=False,
    bgcolor="white",
)

# Mostrar el gráfico interactivo
fig.show()