import argparse
import json
from typing import List, Dict, Any
from .main import GlossaryClient

def print_term(term: Dict[str, Any]):
    """Красивый вывод термина"""
    if not term:
        print(" Термин не найден")
        return
    
    print(f"\n Термин: {term.get('term', 'N/A')}")
    print(f"  ID: {term.get('id', 'N/A')}")
    print(f"  Категория: {term.get('category', 'N/A')}")
    print(f"  Определение: {term.get('definition', 'N/A')}")
    
    if term.get('examples'):
        print(f"  Примеры:\n    {term.get('examples')}")
    
    if term.get('related_terms'):
        print(f"  Связанные термины: {', '.join(term.get('related_terms', []))}")
    
    print(f"  Создан: {term.get('created_at', 'N/A')}")
    print(f"  Обновлен: {term.get('updated_at', 'N/A')}")

def main():
    parser = argparse.ArgumentParser(description='CLI клиент для глоссария gRPC')
    subparsers = parser.add_subparsers(dest='command', help='Команды')
    
    # Команда: получить все термины
    parser_all = subparsers.add_parser('list', help='Получить все термины')
    parser_all.add_argument('--category', '-c', help='Фильтр по категории')
    parser_all.add_argument('--search', '-s', help='Поисковый запрос')
    parser_all.add_argument('--page', '-p', type=int, default=1, help='Номер страницы')
    parser_all.add_argument('--page-size', '-ps', type=int, default=10, help='Размер страницы')
    parser_all.add_argument('--json', '-j', action='store_true', help='Вывод в формате JSON')
    
    # Команда: поиск термина
    parser_search = subparsers.add_parser('search', help='Поиск термина')
    parser_search.add_argument('keyword', help='Ключевое слово для поиска')
    parser_search.add_argument('--json', '-j', action='store_true', help='Вывод в формате JSON')
    
    # Команда: получить термин по ID
    parser_get = subparsers.add_parser('get', help='Получить термин по ID')
    parser_get.add_argument('term_id', help='ID термина')
    parser_get.add_argument('--json', '-j', action='store_true', help='Вывод в формате JSON')
    
    # Команда: создать термин
    parser_create = subparsers.add_parser('create', help='Создать новый термин')
    parser_create.add_argument('--term', '-t', required=True, help='Название термина')
    parser_create.add_argument('--definition', '-d', required=True, help='Определение')
    parser_create.add_argument('--category', '-c', default='general', help='Категория')
    parser_create.add_argument('--examples', '-e', help='Примеры использования')
    parser_create.add_argument('--related', '-r', nargs='+', default=[], help='Связанные термины')
    parser_create.add_argument('--json', '-j', action='store_true', help='Вывод в формате JSON')
    
    # Команда: обновить термин
    parser_update = subparsers.add_parser('update', help='Обновить термин')
    parser_update.add_argument('term_id', help='ID термина для обновления')
    parser_update.add_argument('--term', '-t', help='Новое название термина')
    parser_update.add_argument('--definition', '-d', help='Новое определение')
    parser_update.add_argument('--category', '-c', help='Новая категория')
    parser_update.add_argument('--examples', '-e', help='Новые примеры')
    parser_update.add_argument('--related', '-r', nargs='+', help='Новые связанные термины')
    parser_update.add_argument('--json', '-j', action='store_true', help='Вывод в формате JSON')
    
    # Команда: удалить термин
    parser_delete = subparsers.add_parser('delete', help='Удалить термин')
    parser_delete.add_argument('term_id', help='ID термина для удаления')
    
    # Команда: потоковая передача
    parser_stream = subparsers.add_parser('stream', help='Потоковая передача терминов')
    parser_stream.add_argument('--category', '-c', help='Фильтр по категории')
    
    # Команда: проверка здоровья
    subparsers.add_parser('health', help='Проверка здоровья сервиса')
    
    args = parser.parse_args()
    
    # Подключение к серверу
    client = GlossaryClient()
    
    try:
        if args.command == 'list':
            result = client.get_all_terms(
                category=args.category,
                search=args.search,
                page=args.page,
                page_size=args.page_size
            )
            
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f" Найдено терминов: {result['total_count']}")
                print(f" Страница {result['page']} из {result['total_pages']}")
                print("-" * 50)
                
                for i, term in enumerate(result['terms'], 1):
                    print(f"{i}. {term['term']} ({term['category']})")
                    print(f"   {term['definition'][:100]}...")
                    print()
        
        elif args.command == 'search':
            term = client.search_term(args.keyword)
            if args.json:
                print(json.dumps(term, ensure_ascii=False, indent=2))
            else:
                print_term(term)
        
        elif args.command == 'get':
            term = client.get_term_by_id(args.term_id)
            if args.json:
                print(json.dumps(term, ensure_ascii=False, indent=2))
            else:
                print_term(term)
        
        elif args.command == 'create':
            term_data = {
                "term": args.term,
                "definition": args.definition,
                "category": args.category,
                "examples": args.examples if args.examples else "",
                "related_terms": args.related
            }
            
            term = client.create_term(term_data)
            if args.json:
                print(json.dumps(term, ensure_ascii=False, indent=2))
            else:
                print_term(term)
        
        elif args.command == 'update':
            update_data = {}
            if args.term:
                update_data["term"] = args.term
            if args.definition:
                update_data["definition"] = args.definition
            if args.category:
                update_data["category"] = args.category
            if args.examples:
                update_data["examples"] = args.examples
            if args.related:
                update_data["related_terms"] = args.related
            
            term = client.update_term(args.term_id, update_data)
            if args.json:
                print(json.dumps(term, ensure_ascii=False, indent=2))
            else:
                print_term(term)
        
        elif args.command == 'delete':
            success = client.delete_term(args.term_id)
            if success:
                print(" Термин успешно удален")
            else:
                print(" Ошибка удаления термина")
        
        elif args.command == 'stream':
            count = 0
            for term in client.stream_terms(category=args.category):
                count += 1
                if count > 20:  # Ограничение для демонстрации
                    print(" Достигнуто максимальное количество терминов")
                    break
            
            print(f"\n Получено терминов: {count}")
        
        elif args.command == 'health':
            health = client.health_check()
            print(f" Статус: {health['status']}")
            print(f" Время: {health['timestamp']}")
            print(f" Версия: {health['version']}")
        
        else:
            parser.print_help()
    
    finally:
        client.disconnect()

if __name__ == '__main__':
    main()