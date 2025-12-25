import grpc
import json
from typing import List, Dict, Any
from datetime import datetime

from .grpc_generated import glossary_pb2
from .grpc_generated import glossary_pb2_grpc

class GlossaryClient:
    def __init__(self, host: str = 'localhost', port: int = 50051):
        self.channel = None
        self.stub = None
        self.server_address = f'{host}:{port}'
        self._connect()
    
    def _connect(self):
        """Установка соединения с сервером"""
        try:
            self.channel = grpc.insecure_channel(self.server_address)
            self.stub = glossary_pb2_grpc.GlossaryServiceStub(self.channel)
            print(f" Подключено к серверу {self.server_address}")
        except Exception as e:
            print(f" Ошибка подключения: {e}")
            raise
    
    def disconnect(self):
        """Закрытие соединения"""
        if self.channel:
            self.channel.close()
    
    def get_all_terms(self, category: str = None, search: str = None, 
                     page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Получение всех терминов"""
        try:
            request = glossary_pb2.GetAllTermsRequest(
                category=category if category else "",
                search=search if search else "",
                page=page,
                page_size=page_size
            )
            response = self.stub.GetAllTerms(request)
            
            terms = []
            for term_response in response.terms:
                terms.append(self._proto_to_dict(term_response.term))
            
            return {
                "terms": terms,
                "total_count": response.total_count,
                "page": response.page,
                "total_pages": response.total_pages
            }
            
        except grpc.RpcError as e:
            print(f" Ошибка получения терминов: {e.details()}")
            return {"terms": [], "total_count": 0, "page": 1, "total_pages": 0}
    
    def get_term_by_id(self, term_id: str) -> Dict[str, Any]:
        """Получение термина по ID"""
        try:
            request = glossary_pb2.GetTermByIdRequest(term_id=term_id)
            response = self.stub.GetTermById(request)
            
            if response.term.id:
                return self._proto_to_dict(response.term)
            else:
                print(f" Термин с ID {term_id} не найден")
                return {}
                
        except grpc.RpcError as e:
            print(f" Ошибка: {e.details()}")
            return {}
    
    def search_term(self, keyword: str) -> Dict[str, Any]:
        """Поиск термина по ключевому слову"""
        try:
            request = glossary_pb2.SearchTermRequest(keyword=keyword)
            response = self.stub.SearchTerm(request)
            
            if response.term.id:
                return self._proto_to_dict(response.term)
            else:
                print(f" Термин '{keyword}' не найден")
                return {}
                
        except grpc.RpcError as e:
            print(f" Ошибка: {e.details()}")
            return {}
    
    def create_term(self, term_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание нового термина"""
        try:
            request = glossary_pb2.CreateTermRequest(**term_data)
            response = self.stub.CreateTerm(request)
            
            if response.term.id:
                print(f" Термин '{term_data['term']}' создан")
                return self._proto_to_dict(response.term)
            else:
                print(" Ошибка создания термина")
                return {}
                
        except grpc.RpcError as e:
            print(f" Ошибка: {e.details()}")
            return {}
    
    def update_term(self, term_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление термина"""
        try:
            # Удаляем None значения
            clean_update = {k: v for k, v in update_data.items() if v is not None}
            request = glossary_pb2.UpdateTermRequest(term_id=term_id, **clean_update)
            
            response = self.stub.UpdateTerm(request)
            
            if response.term.id:
                print(f" Термин с ID {term_id} обновлен")
                return self._proto_to_dict(response.term)
            else:
                print(f" Термин с ID {term_id} не найден")
                return {}
                
        except grpc.RpcError as e:
            print(f" Ошибка: {e.details()}")
            return {}
    
    def delete_term(self, term_id: str) -> bool:
        """Удаление термина"""
        try:
            request = glossary_pb2.DeleteTermRequest(term_id=term_id)
            response = self.stub.DeleteTerm(request)
            
            if response.success:
                print(f"Термин с ID {term_id} удален")
                return True
            else:
                print(f" Ошибка удаления: {response.message}")
                return False
                
        except grpc.RpcError as e:
            print(f" Ошибка: {e.details()}")
            return False
    
    def stream_terms(self, category: str = None):
        """Потоковое получение терминов"""
        try:
            request = glossary_pb2.StreamTermsRequest(
                category=category if category else ""
            )
            
            print(" Начало потоковой передачи...")
            for response in self.stub.StreamTerms(request):
                term_dict = self._proto_to_dict(response.term)
                print(f"Получен: {term_dict['term']}")
                yield term_dict
                
        except grpc.RpcError as e:
            print(f"Ошибка потоковой передачи: {e.details()}")
    
    def health_check(self) -> Dict[str, Any]:
        """Проверка здоровья сервиса"""
        try:
            request = glossary_pb2.HealthCheckRequest()
            response = self.stub.HealthCheck(request)
            
            return {
                "status": response.status,
                "timestamp": response.timestamp,
                "version": response.version
            }
            
        except grpc.RpcError as e:
            print(f" Ошибка проверки здоровья: {e.details()}")
            return {"status": "UNKNOWN", "timestamp": "", "version": ""}
    
    def _proto_to_dict(self, term_proto) -> Dict[str, Any]:
        """Преобразование protobuf сообщения в словарь"""
        return {
            "id": term_proto.id,
            "term": term_proto.term,
            "definition": term_proto.definition,
            "category": term_proto.category,
            "examples": term_proto.examples if term_proto.examples else None,
            "related_terms": list(term_proto.related_terms),
            "created_at": term_proto.created_at,
            "updated_at": term_proto.updated_at
        }