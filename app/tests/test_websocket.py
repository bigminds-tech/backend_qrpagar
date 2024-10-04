import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_websocket():
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Teste")
        data = websocket.receive_text()
        assert data == "Produto atualizado!"
