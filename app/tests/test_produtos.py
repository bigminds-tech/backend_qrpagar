import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

# Cliente de teste síncrono para endpoints simples
client = TestClient(app)

# Teste assíncrono usando pytest-asyncio para rotas async
@pytest.mark.asyncio
async def test_criar_produto():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/produtos/", json={
            "nome": "Prato da Segunda",
            "quantidade": "75g",
            "preco": 10.5,
            "desconto": 0.15,
            "categoria": "comida",
            "subcategoria": "entrada",
            "horario_disponibilidade": "07:00 - 22:00"
        })
    assert response.status_code == 200
    assert response.json()["nome"] == "Prato da Segunda"


def test_ler_produto():
    response = client.get("/produtos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_atualizar_produto():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/produtos/1", json={
            "nome": "Prato Atualizado",
            "quantidade": "100g",
            "preco": 12.0,
            "desconto": 0.10,
            "categoria": "comida",
            "subcategoria": "principal",
            "horario_disponibilidade": "08:00 - 20:00"
        })
    assert response.status_code == 200
    assert response.json()["nome"] == "Prato Atualizado"


def test_deletar_produto():
    response = client.delete("/produtos/1")
    assert response.status_code == 204
