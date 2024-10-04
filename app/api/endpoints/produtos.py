from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import controller, schemas
from app.api.dependencies import get_db
from app.utils.websocket_manager import manager

router = APIRouter()

@router.post("/", response_model=schemas.produto.Produto)
async def criar_produto(produto: schemas.produto.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = controller.produto.create_produto(db=db, produto=produto)
    await manager.broadcast(f"Produto {db_produto.nome} criado!")
    return db_produto

@router.get("/", response_model=List[schemas.produto.Produto])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = controller.produto.get_produtos(db, skip=skip, limit=limit)
    return produtos

@router.get("/{produto_id}", response_model=schemas.produto.Produto)
def ler_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = controller.produto.get_produto(db, produto_id=produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.put("/{produto_id}", response_model=schemas.produto.Produto)
async def atualizar_produto(produto_id: int, produto: schemas.produto.ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = controller.produto.update_produto(db=db, produto=produto, produto_id=produto_id)
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await manager.broadcast(f"Produto {db_produto.nome} atualizado!")
    return db_produto

@router.delete("/{produto_id}", response_model=schemas.produto.Produto)
async def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = controller.produto.delete_produto(db=db, produto_id=produto_id)
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    await manager.broadcast(f"Produto {db_produto.nome} deletado!")
    return db_produto
