import grpc
from concurrent import futures
import time
from datetime import datetime
from typing import Iterator

from .grpc_generated import glossary_pb2
from .grpc_generated import glossary_pb2_grpc
from .database import GlossaryDatabase

class GlossaryServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self):
        self.db = GlossaryDatabase()
    
    def GetAllTerms(self, request: glossary_pb2.GetAllTermsRequest, context) -> glossary_pb2.GetAllTermsResponse:
        """Получение всех терминов с пагинацией и фильтрацией"""
        try:
            # Получение всех терминов с фильтрацией
            terms = self.db.get_all_terms(
                category=request.category if request.category else None,
                search=request.search if request.search else None
            )
            
            # Пагинация
            total_count = len(terms)
            page_size = request.page_size if request.page_size > 0 else 10
            page = request.page if request.page > 0 else 1
            
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_terms = terms[start_idx:end_idx]
            
            # Преобразование терминов в protobuf формат
            term_responses = []
            for term in paginated_terms:
                term_responses.append(self._term_to_proto(term))
            
            return glossary_pb2.GetAllTermsResponse(
                terms=term_responses,
                total_count=total_count,
                page=page,
                total_pages=(total_count + page_size - 1) // page_size
            )
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка получения терминов: {str(e)}")
            return glossary_pb2.GetAllTermsResponse()
    
    def GetTermById(self, request: glossary_pb2.GetTermByIdRequest, context) -> glossary_pb2.TermResponse:
        """Получение термина по ID"""
        try:
            term = self.db.get_term_by_id(request.term_id)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Термин с ID {request.term_id} не найден")
                return glossary_pb2.TermResponse()
            
            return self._term_to_response(term)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка получения термина: {str(e)}")
            return glossary_pb2.TermResponse()
    
    def SearchTerm(self, request: glossary_pb2.SearchTermRequest, context) -> glossary_pb2.TermResponse:
        """Поиск термина по ключевому слову"""
        try:
            term = self.db.get_term_by_name(request.keyword)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Термин '{request.keyword}' не найден")
                return glossary_pb2.TermResponse()
            
            return self._term_to_response(term)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка поиска термина: {str(e)}")
            return glossary_pb2.TermResponse()
    
    def CreateTerm(self, request: glossary_pb2.CreateTermRequest, context) -> glossary_pb2.TermResponse:
        """Создание нового термина"""
        try:
            # Подготовка данных
            term_data = {
                "term": request.term,
                "definition": request.definition,
                "category": request.category if request.category else "general",
                "examples": request.examples if request.examples else None,
                "related_terms": list(request.related_terms)
            }
            
            # Создание термина
            term = self.db.create_term(term_data)
            if not term:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details(f"Термин '{request.term}' уже существует")
                return glossary_pb2.TermResponse()
            
            return self._term_to_response(term)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка создания термина: {str(e)}")
            return glossary_pb2.TermResponse()
    
    def UpdateTerm(self, request: glossary_pb2.UpdateTermRequest, context) -> glossary_pb2.TermResponse:
        """Обновление существующего термина"""
        try:
            # Подготовка данных для обновления
            update_data = {}
            if request.term:
                update_data["term"] = request.term
            if request.definition:
                update_data["definition"] = request.definition
            if request.category:
                update_data["category"] = request.category
            if request.examples:
                update_data["examples"] = request.examples
            if request.related_terms:
                update_data["related_terms"] = list(request.related_terms)
            
            # Обновление термина
            term = self.db.update_term(request.term_id, update_data)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Термин с ID {request.term_id} не найден")
                return glossary_pb2.TermResponse()
            
            return self._term_to_response(term)
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка обновления термина: {str(e)}")
            return glossary_pb2.TermResponse()
    
    def DeleteTerm(self, request: glossary_pb2.DeleteTermRequest, context) -> glossary_pb2.DeleteTermResponse:
        """Удаление термина"""
        try:
            success = self.db.delete_term(request.term_id)
            if not success:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Термин с ID {request.term_id} не найден")
                return glossary_pb2.DeleteTermResponse(success=False, message="Термин не найден")
            
            return glossary_pb2.DeleteTermResponse(
                success=True,
                message=f"Термин с ID {request.term_id} успешно удален"
            )
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка удаления термина: {str(e)}")
            return glossary_pb2.DeleteTermResponse(success=False, message=str(e))
    
    def StreamTerms(self, request: glossary_pb2.StreamTermsRequest, context) -> Iterator[glossary_pb2.TermResponse]:
        """Потоковая передача терминов"""
        try:
            terms = self.db.get_all_terms(
                category=request.category if request.category else None
            )
            
            for term in terms:
                if context.is_active():
                    yield self._term_to_response(term)
                    time.sleep(0.1)  # Небольшая задержка для демонстрации
                else:
                    break
                    
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ошибка потоковой передачи: {str(e)}")
    
    def HealthCheck(self, request: glossary_pb2.HealthCheckRequest, context) -> glossary_pb2.HealthCheckResponse:
        """Проверка здоровья сервиса"""
        return glossary_pb2.HealthCheckResponse(
            status="SERVING",
            timestamp=datetime.now().isoformat(),
            version="1.0.0"
        )
    
    def _term_to_proto(self, term) -> glossary_pb2.Term:
        """Преобразование объекта Term в protobuf сообщение"""
        return glossary_pb2.Term(
            id=term.id,
            term=term.term,
            definition=term.definition,
            category=term.category,
            examples=term.examples if term.examples else "",
            related_terms=term.related_terms,
            created_at=term.created_at,
            updated_at=term.updated_at
        )
    
    def _term_to_response(self, term) -> glossary_pb2.TermResponse:
        """Создание TermResponse из объекта Term"""
        return glossary_pb2.TermResponse(term=self._term_to_proto(term))