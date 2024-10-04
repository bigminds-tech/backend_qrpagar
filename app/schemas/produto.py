from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str
    quantidade: Optional[str] = None
    imagem: Optional[str] = None
    preco: float
    desconto: Optional[float] = 0.0
    categoria: Optional[str] = None
    subcategoria: Optional[str] = None
    horario_disponibilidade: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoInDBBase(ProdutoBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True

class Produto(ProdutoInDBBase):
    pass
