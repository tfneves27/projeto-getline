from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import db_produtos_mock, db_banners_mock

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    preco_original: float
    imagem_url: str

class Banner(BaseModel):
    id: int
    imagem_url: str

@app.get("/produtos", response_model=List[Produto])
async def get_produtos():
    return db_produtos_mock

@app.get("/produtos/busca")
async def buscar_produtos(termo: str | None = None):
    if termo is None or termo.strip() == "":
        return db_produtos_mock

    resultados = []
    termos_busca = termo.lower().split(",") 

    for produto in db_produtos_mock:
        nome_produto = produto["nome"].lower()
        
        match = False
        for t in termos_busca:
            if t.strip() in nome_produto:
                match = True
                break
        
        if match:
            resultados.append(produto)
            
    return resultados

@app.get("/banners", response_model=List[Banner])
async def get_banners():
    return db_banners_mock