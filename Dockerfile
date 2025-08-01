# Dockerfile para BAMMIND Web App (Versión a prueba de fallos)

# 1. Usar una imagen oficial de Python como base
FROM python:3.11-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos primero
COPY requirements.txt .

# 4. Instalar todas las librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto de los archivos de la aplicación
COPY . .

# 6. Exponer el puerto que Gunicorn usará
EXPOSE 8080

# 7. El comando final y robusto para correr la aplicación
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]