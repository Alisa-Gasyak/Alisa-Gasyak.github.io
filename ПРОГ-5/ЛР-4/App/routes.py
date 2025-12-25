from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.models import TermCreate, TermUpdate, TermResponse
from app.database import (
    get_all_terms, get_term, search_term,
    create_term, update_term, delete_term
)

router = APIRouter(tags=["glossary"])

@router.get("/terms", response_model=List[TermResponse])
async def get_all_terms_endpoint(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    search: Optional[str] = Query(None, description="Поиск по термину или определению")
):
    """Получить все термины"""
    terms = get_all_terms()
    
    if category:
        terms = [t for t in terms if t.get("category", "").lower() == category.lower()]
    
    if search:
        search_lower = search.lower()
        terms = [
            t for t in terms 
            if search_lower in t["term"].lower() 
            or search_lower in t["definition"].lower()
        ]
    
    return terms

@router.get("/terms/{term_id}", response_model=TermResponse)
async def get_term_by_id(term_id: str):
    """Получить термин по ID"""
    term = get_term(term_id)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ID {term_id} не найден"
        )
    return term

@router.get("/terms/search/{keyword}", response_model=TermResponse)
async def search_term_by_keyword(keyword: str):
    """Найти термин по ключевому слову (названию термина)"""
    term = search_term(keyword)
    if not term:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин '{keyword}' не найден"
        )
    return term

@router.post("/terms", response_model=TermResponse, status_code=status.HTTP_201_CREATED)
async def create_new_term(term: TermCreate):
    """Добавить новый термин"""
    existing = search_term(term.term)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Термин '{term.term}' уже существует"
        )
    
    new_term = create_term(term.dict())
    return new_term

@router.put("/terms/{term_id}", response_model=TermResponse)
async def update_existing_term(term_id: str, term_update: TermUpdate):
    """Обновить существующий термин"""
    updated = update_term(term_id, term_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ID {term_id} не найден"
        )
    return updated

@router.delete("/terms/{term_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_term(term_id: str):
    success = delete_term(term_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Термин с ID {term_id} не найден"
        )