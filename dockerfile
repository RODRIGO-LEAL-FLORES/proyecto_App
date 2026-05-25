# Usamos una versión estable y ligera
FROM python:3.13-slim-bookwor

# Evita que Python genere archivos .pyc y permita logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear usuario para no ejecutar como root
RUN addgroup --system flask && adduser --system --group flask

WORKDIR /app

# Instalar dependencias primero (mejora el caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Cambiar permisos de la carpeta al usuario flask
RUN chown -R flask:flask /app

# Cambiar al usuario no privilegiado
USER flask

# Exponer el puerto
EXPOSE 5000

# Comando de ejecución
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]