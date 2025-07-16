# Imagen base con Python 3.10
FROM python:3.10-slim

# Crear y usar directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
COPY app.py .
COPY modelo_estres_hidrico_maiz.h5 .
COPY scaler_estres_hidrico_maiz.pkl .

# Instalar dependencias
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Exponer el puerto de la API
EXPOSE 10000

# Comando de arranque del servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]