from fastapi.testclient import TestClient
from frontend.main import app

client = TestClient(app)

def test_busca_com_sucesso():
    response = client.get("/produtos/busca?termo=Capa")
    assert response.status_code == 200
    assert response.json()[0]["nome"] == "Capa para Celular Pro"