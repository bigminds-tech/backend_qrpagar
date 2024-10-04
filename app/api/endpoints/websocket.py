import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.utils.websocket_manager import manager

router = APIRouter()

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
                logger.info(f"Mensagem recebida: {data}")
            except WebSocketDisconnect:
                logger.info("Cliente desconectado")
                break
            except Exception as e:
                logger.error(f"Erro ao receber mensagem: {e}")
                await websocket.send_text(f"Erro: {e}")
    except Exception as e:
        logger.error(f"Erro no WebSocket: {e}")
    finally:
        manager.disconnect(websocket)
        logger.info("Conexão WebSocket encerrada")
