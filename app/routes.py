from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")
LAST_PANELS = []

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request, "panels": None})

@router.post("/")
@router.post("/generate")
def create_comic(
    request: Request,
    story: str = Form(...),
    character: str = Form(""),
    setting: str = Form(""),
    art_style: str = Form("")
):
    global LAST_PANELS
    from app.services.image_generator import generate_comic_panels_data

    full_prompt = f"{story}. Main character {character}, setting {setting}, art style {art_style}"
    panels = generate_comic_panels_data(full_prompt)
    LAST_PANELS = panels

    return templates.TemplateResponse(request, "index.html", {
        "request": request,
        "panels": panels,
        "story": story,
        "character": character
    })

@router.get("/download-pdf")
def download_pdf():
    from app.services.exporters import save_pdf
    output_path = "generated/ComicCraft_Comic.pdf"
    if not LAST_PANELS:
        return {"error": "First generate a comic!"}
    save_pdf(LAST_PANELS, output_path)
    return FileResponse(output_path, filename="ComicCraft_Comic.pdf", media_type="application/pdf")