from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.produto import Produto as ProdutoModel
from app.schemas.produto import Produto as ProdutoSchema
from app.schemas.produto import ProdutoCreate, ProdutoUpdate

app = FastAPI()


# Dependência para obter o banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Criar um produto
@app.post("/produtos/", response_model=ProdutoSchema)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = ProdutoModel(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


# Ler todos os produtos
@app.get("/produtos/", response_model=list[ProdutoSchema])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoModel).all()


# Atualizar um produto
@app.put("/produtos/{produto_id}", response_model=ProdutoSchema)
def atualizar_produto(
    produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)
):
    produto_db = (
        db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    )
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in produto.model_dump(exclude_unset=True).items():
        setattr(produto_db, key, value)
    db.commit()
    db.refresh(produto_db)
    return produto_db


# Deletar um produto
@app.delete("/produtos/{produto_id}", response_model=dict)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto_db = (
        db.query(ProdutoModel).filter(ProdutoModel.id == produto_id).first()
    )
    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto_db)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}
