from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate


def get_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()


def get_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Produto).offset(skip).limit(limit).all()


def create_produto(db: Session, produto: ProdutoCreate):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def update_produto(db: Session, produto: ProdutoUpdate, produto_id: int):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        for key, value in produto.model_dump(exclude_unset=True).items():
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
    return db_produto


def delete_produto(db: Session, produto_id: int):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
    return db_produto
