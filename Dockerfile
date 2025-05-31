# Imagen base oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY . /app

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto por donde Dash corre (por defecto es 8050)
EXPOSE 8050

# Cargar la base de datos (si aún no existe)
RUN python cargar_sqlite.py

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
