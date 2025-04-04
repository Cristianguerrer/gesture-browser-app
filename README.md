# 🎮 Servidor Web de EmulatorJS con Python y Docker

Este proyecto configura un servidor web ligero en Python, que sirve contenido del emulador [EmulatorJS](https://github.com/EmulatorJS/EmulatorJS) utilizando Docker y `docker-compose`.

## 🚀 Características

- Imagen ligera basada en `python:3.14-rc-alpine`.
- Descarga y descompresión automática de EmulatorJS.
- Servidor HTTP listo en el puerto `8080`.
- Fácil de desplegar con Docker Compose.

## 🛠️ Estructura del Proyecto

```
📁 game/
├── (tus archivos estáticos, opcionales)
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🐳 Uso con Docker Compose

### 1. Clona el repositorio

```bash
git clone https://tu-repo.git
cd tu-repo
```

### 2. Ejecuta el contenedor

```bash
docker-compose up --build
```

Este comando construirá la imagen, descargará EmulatorJS y expondrá el servidor en [http://localhost:8080](http://localhost:8080).

## 🧱 Contenido del Dockerfile

```Dockerfile
FROM python:3.14-rc-alpine

WORKDIR /game

RUN apk add --no-cache curl p7zip && \
    curl -L -o emulatorjs.7z https://github.com/EmulatorJS/EmulatorJS/releases/download/v4.2.1/4.2.1.7z && \
    7z x emulatorjs.7z && \
    rm emulatorjs.7z

COPY . .

EXPOSE 8080

CMD ["python", "-m", "http.server", "8080"]
```

## 🧪 Verifica que funciona

Abre tu navegador y visita:

```
http://localhost:8080
```

Deberías ver los archivos servidos por el contenedor, incluyendo EmulatorJS.

## 🧩 docker-compose.yml

```yaml
version: '3.8'

services:
  emulatorjs-server:
    build: .
    ports:
      - "8080:8080"
    container_name: emulatorjs
```

## 📜 Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).
