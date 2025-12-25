SAMPLE_TERMS = [
    {
        "term": "gRPC",
        "definition": "Высокопроизводительный фреймворк удаленного вызова процедур с открытым исходным кодом, разработанный Google.",
        "category": "RPC",
        "examples": "gRPC использует HTTP/2 и Protocol Buffers для эффективной коммуникации между сервисами.",
        "related_terms": ["protobuf", "RPC", "микросервисы"]
    },
    {
        "term": "Protocol Buffers",
        "definition": "Механизм сериализации структурированных данных от Google, используемый gRPC.",
        "category": "сериализация",
        "examples": """syntax = "proto3";
message Person {
  string name = 1;
  int32 age = 2;
}""",
        "related_terms": ["gRPC", "сериализация", ".proto файлы"]
    },
    {
        "term": "Protobuf",
        "definition": "Сокращение от Protocol Buffers - язык и платформа для сериализации структурированных данных.",
        "category": "сериализация",
        "examples": "Используется для определения структуры сообщений в .proto файлах.",
        "related_terms": ["gRPC", "сериализация"]
    },
    {
        "term": "Сериализация",
        "definition": "Процесс преобразования объекта в поток байтов для передачи или хранения.",
        "category": "программирование",
        "examples": "JSON сериализация, Protobuf сериализация, Pickle в Python",
        "related_terms": ["десериализация", "protobuf", "JSON"]
    },
    {
        "term": "HTTP/2",
        "definition": "Вторая основная версия протокола HTTP, поддерживающая мультиплексирование и сжатие заголовков.",
        "category": "протокол",
        "examples": "Используется gRPC для эффективной двунаправленной связи.",
        "related_terms": ["HTTP", "протокол", "gRPC"]
    },
    {
        "term": "Стабы",
        "definition": "В gRPC - клиентские объекты, которые предоставляют те же методы, что и сервер.",
        "category": "gRPC",
        "examples": "Стаб генерируется автоматически из .proto файла.",
        "related_terms": ["gRPC", "клиент", "сервер"]
    },
    {
        "term": "Серверная реализация",
        "definition": "Код на сервере, который реализует методы, определенные в protobuf-сервисе.",
        "category": "gRPC",
        "examples": "Наследование от сгенерированного класса сервиса и реализация его методов.",
        "related_terms": ["gRPC", "сервис", "protobuf"]
    },
    {
        "term": "Потоковая передача",
        "definition": "Возможность gRPC передавать последовательности сообщений в одном вызове.",
        "category": "gRPC",
        "examples": "Клиентский поток, серверный поток или двунаправленный поток.",
        "related_terms": ["stream", "gRPC", "поток данных"]
    }
]