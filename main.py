from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
from tensorflow_hub_art_project import makeArt
from pathlib import Path

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/results", StaticFiles(directory="results"), name="results")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/predict/")
async def predict(content: UploadFile = File(...), style: UploadFile = File(...)):
    content_path = "uploads/" + content.filename
    style_path = "uploads/" + style.filename

    with open(content_path, "wb") as buffer:
        shutil.copyfileobj(content.file, buffer)

    with open(style_path, "wb") as buffer:
        shutil.copyfileobj(style.file, buffer)

    makeArt(content_path, style_path, "output.jpg")

    return templates.TemplateResponse("result.html", {"request": {}, "content_path": content_path, "style_path": style_path, "output_path": "output.jpg"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
