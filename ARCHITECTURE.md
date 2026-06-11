# Diagramas de Arquitectura - Hermes Notifier

Este documento contiene la representacion grafica de la arquitectura modular y los flujos del monitor de notificaciones.

---

## Diagrama de Clases (Estructura Estatica)

Muestra las interfaces abstractas definidas en 'hermes.core' y como se relacionan con sus implementaciones concretas mediante la orquestacion de Monitor y la creacion a traves de fabricas.

```mermaid
classDiagram
    direction TB
    
    class Message {
        +id: str
        +sender: str
        +subject: str
        +body: str
    }

    class Source {
        <<interface>>
        +fetch(query: str, max_results: int) Iterator~Message~*
        +name() str*
    }
    
    class Notifier {
        <<interface>>
        +send(keyword: str, message: Message) void*
    }
    
    class Filter {
        <<interface>>
        +keyword: str*
        +matches(message: Message) bool*
    }
    
    class Storage {
        <<interface>>
        +load() dict[str, set[str]]*
        +save(seen: dict[str, set[str]]) void*
    }

    Source <|.. GmailSource : Implements
    Notifier <|.. TelegramNotifier : Implements
    Filter <|.. KeywordFilter : Implements
    Filter <|.. CompositeFilter : Implements
    Storage <|.. JsonFileStorage : Implements

    class Monitor {
        -source: Source
        -notifiers: list~Notifier~
        -filters: list~Filter~
        -storage: Storage
        -poll_interval: int
        +run() void
        -_tick(seen: dict) void
    }

    Monitor --> Source : Uses
    Monitor --> Notifier : Uses
    Monitor --> Filter : Uses
    Monitor --> Storage : Uses
    Monitor ..> Message : Uses

    class SourceFactory {
        +_registry: dict
        +register(name: str, klass: type) void
        +create(config: Config) Source
    }

    class NotifierFactory {
        +_registry: dict
        +register(name: str, klass: type) void
        +create(config: Config) list~Notifier~
    }

    SourceFactory ..> Source : Creates
    NotifierFactory ..> Notifier : Creates
```

---

## Diagrama de Secuencia (Flujo del Bucle Monitor)

Muestra como interactuan los componentes dinamicamente en cada ciclo de revision.

```mermaid
sequenceDiagram
    autonumber
    participant M as Monitor
    participant S as GmailSource
    participant F as KeywordFilter
    participant N as TelegramNotifier
    participant ST as JsonFileStorage

    loop Cada intervalo de sondeo (poll_interval)
        M->>S: fetch(query=keyword)
        Note over S: Realiza consulta a la API de Gmail
        S-->>M: Iterator[Message]
        
        loop Por cada mensaje encontrado
            Note over M: Verifica si el ID ya fue visto
            alt ID no esta en historial (seen)
                M->>F: matches(message)
                F-->>M: True / False
                
                alt matches es True
                    M->>N: send(keyword, message)
                    Note over N: Envia POST a la API de Telegram
                    M->>M: Agrega ID a la lista local de vistos
                end
            end
        end
        M->>ST: save(seen)
        Note over ST: Escribe diccionario en visto_ids.json
    end
```
