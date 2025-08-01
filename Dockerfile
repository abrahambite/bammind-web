# Dockerfile para BAMMIND Web App

# 1. Usar una imagen oficial de Python como base
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos primero para optimizar la caché
COPY requirements.txt .

# 4. Instalar todas las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto de los archivos de la aplicación al contenedor
COPY . .

# 6. Exponer el puerto que Gunicorn usará
EXPOSE 8080

# 7. El comando final para correr la aplicación cuando el contenedor inicie
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]