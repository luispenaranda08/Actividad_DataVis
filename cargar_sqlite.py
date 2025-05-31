import pandas as pd
import sqlite3

# Cargar el dataset CSV
df = pd.read_csv("Air_Quality.csv")  # Cambia el nombre si tu archivo se llama diferente

# Conectarse (o crear) una base SQLite
conn = sqlite3.connect("mi_base.db")  # Esto creará el archivo mi_base.db

# Guardar el dataframe en la base como tabla
df.to_sql("mi_tabla", conn, if_exists="replace", index=False)

# Cerrar conexión
conn.close()

print("✅ Base de datos creada con éxito.")
