from fastapi import FastAPI
from pydantic import BaseModel
from database import db_produtos_mock, db_promocoes_mock
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    imagem_url: str

class BannerPromocao(BaseModel):
    id: int
    imagem_url: str

origins = ["*"]

def ler_banco():
    with open("database.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/produtos", response_model=List[Produto])
async def get_produtos():
    return db_produtos_mock

@app.get("/promocoes", response_model=List[BannerPromocao])
async def get_promocoes():
    return db_promocoes_mock

@app.get("/produtos/busca")
async def buscar_produtos(termo: str | None = None):
    if termo is None:
        return[]
    resultados = []
    for produto in db_produtos_mock:
        # Checar se o 'termo' (em minúsculo) está no 'nome' do produto (em minúsculo)
        if termo.lower() in produto["nome"].lower():
            resultados.append(produto)
    return resultados