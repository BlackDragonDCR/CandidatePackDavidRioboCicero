# LogMeal Take-Home Project — David Riobo Cicero

## Requisitos previos

- Python 3.11 o superior
- Docker (opcional, si se quiere ejecutar con contenedores)

## Ejecución del proyecto

### Opción 1: Ejecución local (sin Docker)

1. **Backend**
ejecutar en una terminal:
cd backend
pip install -r requirements.txt
py app.py
(El servidor estará disponible en http://localhost:8000)

2. **Frontend**
ejecutar en otra terminal:
cd frontend
py -m http.server 3000
(La interfaz estará disponible en http://localhost:3000)

### Opción 2: Ejecución con Docker
instalar docker a través del sitio oficial para la version de sistema correcta
correr Docker
ejecutar en una terminal: "docker compose up --build"
acceder a "http://localhost:3000" usando un browser
(para detener los contenedores se puede usar "docker compose down" en la terminal en la que se inició o usando ctrl+C)

## Propriedades del proyecto

### Endpoints disponibles

POST /api/upload_image - Subir una imagen
GET	/api/list_images - Listar todas las imágenes subidas
POST /api/analyse_image - Analizar imagen
POST /api/share_image - Generar enlace temporal (10 minutos)
GET	/s/{token} - Página pública con la imagen compartida
GET	/uploads/{filename} - Servir el archivo de imagen

### Frontend
la interfaz permite:
- subir imagenes
- ver listado con miniatura, id de imagen y mas opciones
- ver miniaturas listadas en tamaño completo
- compartir imagenes junto de su analisis con un enlace generado que expira despues de 10 minutos
- analizar imagenes en la pagina

el analisis incluye: 
- ancho y alto de la imagen
- formato de imagen
- tamaño en kilobytes
- modo de color

### Sobre Docker
El archivo docker-compose.yml levanta dos servicios:
- backend: Python + Flask en el puerto 8000
- frontend: Nginx sirviendo archivos estáticos en el puerto 3000

Los datos subidos se almacenan en backend/data/uploads y persisten entre ejecuciones gracias al volumen montado.

### Decisiones Tecnicas
- Backend: Flask con almacenamiento en disco (archivos JSON para metadatos y tokens)
- Frontend: HTML/CSS/JS vanilla (sin frameworks)
- Tokens: Se generan con uuid + hashlib.sha256, expiran a los 10 minutos
- Análisis de imágenes: Librería Pillow (PIL)