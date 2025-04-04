# 🎮 Gesture-browser-app 
## Servidor Web de EmulatorJS con Python y Docker

Este proyecto configura un servidor web ligero en Python, que sirve contenido del emulador [EmulatorJS](https://github.com/EmulatorJS/EmulatorJS) utilizando Docker y `docker-compose`.

## 🚀 Características

- Imagen ligera basada en `python:3.14-rc-alpine`.
- Descarga y descompresión automática de EmulatorJS.
- Servidor HTTP listo en el puerto `8080`.
- Fácil de desplegar con Docker Compose.

## 🛠️ Estructura del Proyecto

```
📁 gesture-browser-app/
├── roms/
├── Dockerfile
├── docker-compose.yaml
├── index.html
└── README.md
```

## 🐳 Uso con Docker Compose

### 1. Clona el repositorio

```bash
git clone https://github.com/Cristianguerrer/gesture-browser-app.git
cd gesture-browser-app
```

### 2. Ejecuta el contenedor

```bash
docker-compose up --build
```

Este comando construirá la imagen, descargará EmulatorJS y expondrá el servidor en [http://localhost:80](http://localhost:80).

## 🧱 Contenido del Dockerfile

```Dockerfile
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
COPY index.html .

# Expone el puerto del servidor
EXPOSE 8080

# Comando por defecto al iniciar el contenedor
CMD ["python", "-m", "http.server", "8080"]
```

## 🧪 Verifica que funciona

Abre tu navegador y visita:

```
http://localhost:80
```

Deberías ver el EmulatorJS.
![alt text](image.png)

## 🧩 docker-compose.yml

```yaml
version: '3.0'

services:
  snes9x:
    build: .
    container_name: snes9x
    ports:
      - "80:8080"
    volumes:
      - ./roms/juego-top-gear.smc:/game/juego-top-gear.smc
```

## 📜 Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).
