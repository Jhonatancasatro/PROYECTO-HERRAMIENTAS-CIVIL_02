# Importar librerías
import pandas as pd
# Cargar el dataset 
df = pd.read_csv("dataset.csv", sep=";")
# Visualizar la información
print(df.head())       # Muestra las primeras 5 filas
df.info()              # Muestra las columnas, tipos de datos y no nulos
print(df.shape)        # Muestra las dimensiones (filas, columnas)

#Limpieza datos
print("valores nulos por columna:")
print(df.isnull().sum())  

duplicados = df.duplicated().sum()
print(f"filas duplicadas: {duplicados}")

df = df.drop_duplicates()
print(f"filas duplicadas eliminadas: {duplicados}")
print(f"Dimensiones despues de eliminar duplicados: {df.shape}")
