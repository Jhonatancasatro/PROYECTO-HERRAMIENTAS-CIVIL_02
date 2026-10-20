import pandas as pd
from sklearn.linear_model import LinearRegression

# Cargar el dataset en formato CSV (delimitado por punto y coma)
df = pd.read_csv("dataset.csv", sep=";")
df.columns = df.columns.str.strip()
df = df.drop_duplicates()

# Definir la variable objetivo y la variable de entrada de tu dataset
fc = "Compressive Strength (28-day)(Mpa)"
X = df[["Cement"]]
y = df[fc]

# Entrenar el modelo lineal
modelo = LinearRegression()
modelo.fit(X, y)

# Predecir la resistencia para una mezcla con 350 kg/m³ de cemento
cemento_nuevo = pd.DataFrame({"Cement": [350]})
resistencia_predicha = modelo.predict(cemento_nuevo)[0]
print(f"Resistencia predicha para 350 kg/m³ de cemento: {resistencia_predicha:.2f} MPa")

# Calcular R² sobre los mismos datos usados para entrenar
r2 = modelo.score(X, y)
print(f"Coeficiente de determinación R²: {r2:.4f}")