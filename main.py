from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from database import engine
import uvicorn
from datetime import datetime

from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class HeroisCreate(BaseModel):
    nome: str
    superpoder: str
    raca: str

app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    herois = db.query(models.Herois).filter(models.Herois.ativo == True).order_by(models.Herois.id.desc())

    return templates.TemplateResponse("index.html", {"request": request, "herois": herois})

@app.post("/add")
async def add(request: Request,nome: str = Form(...),superpoder: str = Form(...),raca: str = Form(...),ativo: bool = Form(True),db: Session = Depends(get_db)):

    # Crie uma instância do modelo Herois com a data atual
    heroi = models.Herois(nome=nome, superpoder=superpoder, raca=raca, ativo=ativo)

    # Adicione o herói ao banco de dados e faça o commit
    db.add(heroi)
    db.commit()

    # Redirecione para a página inicial
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})

@app.get("/edit/{heroi_id}")
async def edit(request: Request, heroi_id: int, db: Session = Depends(get_db)):
    heroi = db.query(models.Herois).filter(models.Herois.id == heroi_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "heroi": heroi})

@app.post("/update/{heroi_id}")
async def update(request: Request, heroi_id: int, nome: str = Form(...), superpoder: str = Form(...), raca: str = Form(...), db: Session = Depends(get_db)):
    heroi = db.query(models.Herois).filter(models.Herois.id == heroi_id).first()
    heroi.nome = nome
    heroi.superpoder = superpoder
    heroi.raca = raca
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/historico")
async def historico(request: Request, db: Session = Depends(get_db)):
    herois = db.query(models.Herois).filter(models.Herois.ativo == False).order_by(models.Herois.id.desc())

    return templates.TemplateResponse("historico.html", {"request": request, "herois": herois})

@app.get("/delete/{heroi_id}")
async def delete(request: Request, heroi_id: int, db: Session = Depends(get_db)):
    heroi = db.query(models.Herois).filter(models.Herois.id == heroi_id).first()
        # Marque o herói como inativo
    heroi.ativo = False
    db.commit()

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/deleteBD/{heroi_id}")
async def delete(request: Request, heroi_id: int, db: Session = Depends(get_db)):
    heroi = db.query(models.Herois).filter(models.Herois.id == heroi_id).first()
    db.delete(heroi)
    db.commit()

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8888)
