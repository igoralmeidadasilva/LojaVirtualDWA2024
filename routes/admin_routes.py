from fastapi import APIRouter, Path, Query, Response
from fastapi.responses import JSONResponse

from dtos.alterar_produto_dto import AlterarProdutoDTO
from dtos.id_produto_dto import IdProdutoDTO
from dtos.inserir_produto_dto import InserirProdutoDTO
from dtos.problem_details_dto import ProblemDetailsDto
from models.produto_model import Produto
from repositories.produto_repo import ProdutoRepo


router = APIRouter(prefix="/manager")


@router.get("/obter_produtos")
async def obter_produtos():
    produtos = ProdutoRepo.obter_todos()
    return produtos

@router.post("/inserir_produto", status_code=201)
async def inserir_produto(inputDto: InserirProdutoDTO) -> Produto:
    novo_produto = Produto(None, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    novo_produto = ProdutoRepo.inserir(novo_produto)
    return novo_produto

@router.post("/excluir_prouto", status_code=204)
async def excluir_produto(inputDto: IdProdutoDTO) -> bool:
    if ProdutoRepo.excluir(inputDto.id_produto): return None
    pb = ProblemDetailsDto("int", f"O produto com id {inputDto.id_produto} não foi encontrado","value_not_found", ["body", "id_produto"])
    return JSONResponse(pb.to_dict(), status_code=404)

@router.get("/obter_produto/{id_produto}")
async def obter_produto(id_produto: int = Path(..., title="Id do Produto", ge=1)) -> bool:
    produto = ProdutoRepo.obter_um(id_produto)
    if produto: return produto
    pb = ProblemDetailsDto("int", f"O produto com id {id_produto} não foi encontrado","value_not_found", ["body", "id_produto"])
    return JSONResponse(pb.to_dict(), status_code=404)

@router.post("/alterar_prouto", status_code=204)
async def alterar_produto(inputDto: AlterarProdutoDTO) -> bool:
    produto = Produto(inputDto.id, inputDto.nome, inputDto.preco, inputDto.descricao, inputDto.estoque)
    if ProdutoRepo.alterar(produto): return None
    pb = ProblemDetailsDto("int", f"O produto com id {inputDto.id_produto} não foi encontrado","value_not_found", ["body", "id_produto"])
    return JSONResponse(pb.to_dict(), status_code=404)
