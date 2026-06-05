from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp
import os
import uvicorn
from pathlib import Path

app = FastAPI()

# Modelo de datos para recibir la URL
class VideoRequest(BaseModel):
    url: str

@app.post("/api/download")
async def download_video(request: VideoRequest):
    # Detecta automáticamente la carpeta "Descargas" (Downloads) del usuario
    downloads_path = str(Path.home() / "Downloads")
    
    # Plantilla del nombre del archivo: Título del video . extensión
    outtmpl = os.path.join(downloads_path, "%(title)s.%(ext)s")

    # Configuración de yt-dlp para obtener la mejor calidad y forzar MP4
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': outtmpl,
        'merge_output_format': 'mp4',
        'noplaylist': True, # Descarga solo un video, no la playlist entera
        'quiet': False      # Muestra el progreso en la consola de la terminal
    }

    try:
        # Ejecuta la descarga
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([request.url])
        
        return {"status": "success", "message": "¡Video descargado con éxito en tu carpeta de Descargas!"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Montar la carpeta 'static' para mostrar la interfaz web
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# NUEVO: Instrucción para arrancar el servidor desde el propio archivo
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)