# Imagen base
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Puerto para exponer
EXPOSE 10000

# Comando para ejecutar la API
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
