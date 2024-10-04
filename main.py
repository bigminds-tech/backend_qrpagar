import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import produtos, websocket
from app.db.base import Base
from app.db.session import engine

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gerenciador de Produtos",
    description="API para gerenciar produtos de um estabelecimento com atualizações em tempo real.",  # noqa :E501
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou defina domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir os routers
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(websocket.router, prefix="/websocket", tags=["WebSocket"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
