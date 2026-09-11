#Construir la Imagen del servicio

#La imagen base

FROM python:3.13-slim

#La carpeta de trabajo dentro del contenedor

WORKDIR /servicio

#Que los mensajes salgan inmediatamente en la consola

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

#Copiar los archivos de requerimientos
COPY requirements.txt .

#Instalar las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

#Copiar el resto de los archivos del proyecto
COPY . .

#documentar el puerto que se va a exponer
EXPOSE 8080

#Comando para ejecutar el servicio
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"] #comando para ejecutar el servicio, sh sirve para ejecutar el comando en un shell, -c indica que se va a ejecutar un comando, y uvicorn main:app --host 0.0.0.0 --port ${PORT} sirve para ejecutar el servicio, main es el nombre del archivo donde se encuentra la aplicación, app es el nombre de la aplicación, --host