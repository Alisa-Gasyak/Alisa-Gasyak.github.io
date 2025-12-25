import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class Term:
    id: str
    term: str
    definition: str
    category: str = "general"
    examples: Optional[str] = None
    related_terms: List[str] = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.related_terms is None:
            self.related_terms = []
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class GlossaryDatabase:
    def __init__(self, data_file: str = "glossary_data.json"):
        self.data_file = Path(data_file)
        self.terms: Dict[str, Term] = {}
        self.term_index: Dict[str, str] = {}  # term_name -> term_id
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for term_data in data:
                        term = Term(**term_data)
                        self.terms[term.id] = term
                        self.term_index[term.term.lower()] = term.id
                print(f"📚 Загружено {len(self.terms)} терминов из файла")
            except Exception as e:
                print(f"⚠️ Ошибка загрузки данных: {e}")
                self.initialize_with_sample_data()
        else:
            self.initialize_with_sample_data()
    
    def initialize_with_sample_data(self):
        """Инициализация с примерными данными"""
        from .glossary_data import SAMPLE_TERMS
        
        for term_data in SAMPLE_TERMS:
            term_id = self.generate_id(term_data["term"])
            term = Term(
                id=term_id,
                **term_data,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
            self.terms[term_id] = term
            self.term_index[term.term.lower()] = term_id
        
        self.save_data()
        print(f"📚 Инициализировано {len(self.terms)} терминов")
    
    def generate_id(self, term_name: str) -> str:
        """Генерация ID на основе имени термина"""
        term_hash = hashlib.md5(term_name.lower().encode()).hexdigest()[:8]
        return f"term_{term_hash}"
    
    def save_data(self):
        """Сохранение данных в файл"""
        try:
            data = [term.to_dict() for term in self.terms.values()]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Ошибка сохранения данных: {e}")
    
    def get_all_terms(self, category: Optional[str] = None, 
                     search: Optional[str] = None) -> List[Term]:
        """Получение всех терминов с фильтрацией"""
        filtered_terms = list(self.terms.values())
        
        if category:
            filtered_terms = [t for t in filtered_terms 
                            if t.category.lower() == category.lower()]
        
        if search:
            search_lower = search.lower()
            filtered_terms = [
                t for t in filtered_terms
                if (search_lower in t.term.lower() or 
                    search_lower in t.definition.lower() or
                    (t.examples and search_lower in t.examples.lower()))
            ]
        
        return filtered_terms
    
    def get_term_by_id(self, term_id: str) -> Optional[Term]:
        """Получение термина по ID"""
        return self.terms.get(term_id)
    
    def get_term_by_name(self, term_name: str) -> Optional[Term]:
        """Получение термина по имени"""
        term_id = self.term_index.get(term_name.lower())
        if term_id:
            return self.terms.get(term_id)
        return None
    
    def create_term(self, term_data: Dict[str, Any]) -> Optional[Term]:
        """Создание нового термина"""
        # Проверка на существующий термин
        existing = self.get_term_by_name(term_data["term"])
        if existing:
            return None
        
        term_id = self.generate_id(term_data["term"])
        now = datetime.now().isoformat()
        
        term = Term(
            id=term_id,
            **term_data,
            created_at=now,
            updated_at=now
        )
        
        self.terms[term_id] = term
        self.term_index[term.term.lower()] = term_id
        self.save_data()
        
        return term
    
    def update_term(self, term_id: str, update_data: Dict[str, Any]) -> Optional[Term]:
        """Обновление термина"""
        term = self.terms.get(term_id)
        if not term:
            return None
        
        # Обновление полей
        for key, value in update_data.items():
            if value is not None:
                setattr(term, key, value)
        
        # Если обновили имя термина, обновляем индекс
        if 'term' in update_data and update_data['term']:
            old_key = term.term.lower()
            new_key = update_data['term'].lower()
            
            if old_key in self.term_index:
                del self.term_index[old_key]
            self.term_index[new_key] = term_id
        
        term.updated_at = datetime.now().isoformat()
        self.save_data()
        
        return term
    
    def delete_term(self, term_id: str) -> bool:
        """Удаление термина"""
        term = self.terms.get(term_id)
        if not term:
            return False
        
        # Удаление из индекса
        if term.term.lower() in self.term_index:
            del self.term_index[term.term.lower()]
        
        # Удаление из основного хранилища
        del self.terms[term_id]
        self.save_data()
        
        return True