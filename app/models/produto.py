from sqlalchemy import Column, DateTime, Float, Integer, String, func

from app.db.base import Base


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    quantidade = Column(String, nullable=True)
    imagem = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
    desconto = Column(Float, default=0.0)
    categoria = Column(String, nullable=True)
    subcategoria = Column(String, nullable=True)
    horario_disponibilidade = Column(String, nullable=True)
    criado_em = Column(DateTime, default=func.now())
    atualizado_em = Column(DateTime, default=func.now(), onupdate=func.now())
