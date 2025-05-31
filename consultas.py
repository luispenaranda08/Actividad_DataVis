import sqlite3
import pandas as pd

# Conectarse a la base de datos
conn = sqlite3.connect("mi_base.db")

# Ejemplo 1: Mostrar las 10 primeras filas
def ver_datos():
    query = "SELECT * FROM mi_tabla LIMIT 10"
    df = pd.read_sql_query(query, conn)
    print(df)

# Ejemplo 2: Promedio de contaminantes por ciudad
def promedio_por_ciudad():
    query = """
    SELECT City,
           AVG(CO) AS avg_CO,
           AVG(CO2) AS avg_CO2,
           AVG(NO2) AS avg_NO2,
           AVG(SO2) AS avg_SO2,
           AVG(O3) AS avg_O3,
           AVG([PM2.5]) AS avg_PM25,
           AVG(PM10) AS avg_PM10,
           AVG(AQI) AS avg_AQI
    FROM mi_tabla
    GROUP BY City
    ORDER BY avg_AQI DESC
    """
    df = pd.read_sql_query(query, conn)
    print(df)

# Ejemplo 3: Datos para una ciudad específica
def datos_por_ciudad(ciudad):
    query = f"SELECT * FROM mi_tabla WHERE City = ? LIMIT 20"
    df = pd.read_sql_query(query, conn, params=(ciudad,))
    print(df)

# Cerrar conexión cuando termine
def cerrar_conexion():
    conn.close()

# ----------- PRUEBA -----------

if __name__ == "__main__":
    ver_datos()
    promedio_por_ciudad()
    datos_por_ciudad("Bogotá")  # Cambia por una ciudad existente si es necesario
    cerrar_conexion()
