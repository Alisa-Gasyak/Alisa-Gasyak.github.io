import grpc
from concurrent import futures
import signal
import sys
import logging
from pathlib import Path

# Добавление пути для импорта сгенерированного кода
sys.path.append(str(Path(__file__).parent))

from .grpc_generated import glossary_pb2_grpc
from .service import GlossaryServicer

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GlossaryServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 50051):
        self.host = host
        self.port = port
        self.server = None
        self.shutdown_flag = False
    
    def serve(self):
        """Запуск gRPC сервера"""
        # Создание сервера с пулом потоков
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        
        # Регистрация сервиса
        glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(
            GlossaryServicer(), self.server
        )
        
        # Добавление порта
        server_address = f'{self.host}:{self.port}'
        self.server.add_insecure_port(server_address)
        
        # Настройка обработчиков сигналов
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Запуск сервера
        logger.info(f"🚀 Запуск gRPC сервера на {server_address}")
        self.server.start()
        
        try:
            # Ожидание завершения
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Получен сигнал прерывания")
        finally:
            self.stop()
    
    def stop(self):
        """Остановка сервера"""
        if self.server:
            logger.info("Остановка сервера...")
            self.server.stop(grace=5)
            self.server = None
            logger.info("Сервер остановлен")
    
    def _signal_handler(self, signum, frame):
        """Обработчик сигналов для graceful shutdown"""
        logger.info(f"Получен сигнал {signum}")
        self.stop()
        sys.exit(0)

def main():
    """Основная функция запуска сервера"""
    server = GlossaryServer()
    server.serve()

if __name__ == '__main__':
    main()