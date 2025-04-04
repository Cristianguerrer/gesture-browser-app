# Imagen base ligera con Python
FROM python:3.14-rc-alpine

# Establece el directorio de trabajo
WORKDIR /game

# Instala dependencias necesarias y limpia cache
RUN apk add --no-cache curl p7zip && \
    echo "Dependencias instaladas correctamente."

# Descarga y extrae EmulatorJS
RUN curl -L -o emulatorjs.7z https://github.com/EmulatorJS/EmulatorJS/releases/download/v4.2.1/4.2.1.7z && \
    7z x emulatorjs.7z && \
    rm emulatorjs.7z && \
    echo "EmulatorJS descargado y extraído correctamente."

# Copia tu aplicación (si hay archivos locales adicionales)
COPY index. .

# Para kubernetes
# COPY index.html .

# Expone el puerto del servidor
EXPOSE 8080

# Comando por defecto al iniciar el contenedor
CMD ["python", "-m", "http.server", "8080"]
