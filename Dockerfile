# Imagen base con Python 3.10
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de archivos
COPY . .

# Exponer el puerto que Render espera
EXPOSE 10000

# Iniciar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]