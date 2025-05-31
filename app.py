import pandas as pd
import sqlite3
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import os

# 1. Cargar datos desde SQLite
conn = sqlite3.connect("mi_base.db")
df = pd.read_sql_query("SELECT * FROM mi_tabla", conn)
conn.close()

# 2. Columnas categóricas y numéricas
columnas_categoricas = ["City"]
columnas_numericas = ['CO', 'CO2', 'NO2', 'SO2', 'O3', 'PM2.5', 'PM10', 'AQI']

# 3. Inicializar Dash
app = dash.Dash(__name__)
app.title = "Dashboard Calidad del Aire"

# 4. Layout de la App
app.layout = html.Div(style={"maxWidth": "1000px", "margin": "0 auto", "fontFamily": "Arial"}, children=[
    html.H1("🌍 Dashboard de Calidad del Aire", style={"textAlign": "center", "color": "#2c3e50"}),
    html.Hr(),

    html.Div([
        html.Label("Selecciona una ciudad:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id='dropdown-ciudad',
            options=[{"label": ciudad, "value": ciudad} for ciudad in df["City"].unique()],
            value=df["City"].unique()[0],
            clearable=False,
            style={"width": "300px"}
        ),
    ], style={"marginBottom": "20px"}),

    html.Div([
        html.Label("Selecciona una variable:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id='dropdown-variable',
            options=[
                {"label": col, "value": col} for col in columnas_categoricas + columnas_numericas
            ],
            value="AQI",
            clearable=False,
            style={"width": "300px"}
        ),
    ], style={"marginBottom": "20px"}),

    dcc.Graph(id='grafico-principal'),

    html.Div("Fuente: Air_Quality.csv", style={"textAlign": "center", "marginTop": "40px", "color": "#7f8c8d"})
])

# 5. Callback: actualiza gráfico según selección
@app.callback(
    Output("grafico-principal", "figure"),
    [Input("dropdown-variable", "value"),
     Input("dropdown-ciudad", "value")]
)
def actualizar_grafico(variable, ciudad):
    df_filtrado = df[df["City"] == ciudad]

    if variable in columnas_categoricas:
        fig = px.histogram(df_filtrado, x=variable, title=f"Distribución de {variable} en {ciudad}")
    else:
        fig = px.line(df_filtrado, x="Date", y=variable, title=f"{variable} a lo largo del tiempo en {ciudad}")
        fig.update_traces(mode="lines+markers")

    fig.update_layout(
        template="plotly_white",
        xaxis_title=variable if variable in columnas_categoricas else "Fecha",
        yaxis_title="Frecuencia" if variable in columnas_categoricas else variable,
        margin={"l": 40, "r": 40, "t": 60, "b": 40}
    )

    return fig

# 6. Ejecutar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=True)
