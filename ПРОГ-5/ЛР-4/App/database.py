import json
from typing import Dict, Any
from datetime import datetime
import uuid
from pathlib import Path

glossary_db = {} # Имитация базы данных в памяти
db_file = Path("glossary.json")

def init_db():
    
    global glossary_db
    
    from app.glossary_data import initial_glossary  # Загрузка начальных данных
    
    for term_data in initial_glossary:
        term_id = str(uuid.uuid4())
        glossary_db[term_id] = {
            "id": term_id,
            **term_data,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    
    if db_file.exists():
        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                glossary_db.update(saved_data)
                print(f"Загружено {len(saved_data)} терминов из файла")
        except Exception as e:
            print(f"Ошибка загрузки из файла: {e}")
    
    print(f"База данных инициализирована. Терминов: {len(glossary_db)}")

def save_to_file():
    """Сохранение в файл"""
    try:
        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump(glossary_db, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def close_db():
    """Закрытие соединения с БД"""
    save_to_file()
    print("База данных сохранена")

def get_all_terms() -> list[Dict[str, Any]]:
    return list(glossary_db.values())

def get_term(term_id: str) -> Optional[Dict[str, Any]]:
    return glossary_db.get(term_id)

def search_term(keyword: str) -> Optional[Dict[str, Any]]:
    keyword_lower = keyword.lower()
    for term in glossary_db.values():
        if term["term"].lower() == keyword_lower:
            return term
    return None

def create_term(term_data: Dict[str, Any]) -> Dict[str, Any]:
    term_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    term = {
        "id": term_id,
        **term_data,
        "created_at": now,
        "updated_at": now
    }
    
    glossary_db[term_id] = term
    save_to_file()
    return term

def update_term(term_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if term_id not in glossary_db:
        return None
    
    term = glossary_db[term_id]
    for key, value in update_data.items():
        if value is not None:
            term[key] = value
    
    term["updated_at"] = datetime.now().isoformat()
    glossary_db[term_id] = term
    save_to_file()
    return term

def delete_term(term_id: str) -> bool:
    if term_id in glossary_db:
        del glossary_db[term_id]
        save_to_file()
        return True
    return False