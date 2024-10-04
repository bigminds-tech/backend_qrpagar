from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.endpoints import produtos, websocket
from fastapi.middleware.cors import CORSMiddleware

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gerenciador de Produtos",
    description="API para gerenciar produtos de um estabelecimento com atualizações em tempo real.",
    version="1.0.0"
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
