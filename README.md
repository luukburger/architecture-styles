# Minimal Layered vs Hexagonal Example

This repository contains two minimal Python implementations of the same order entry flow:

- `layered/` — classic layered architecture
- `hexagonal/` — hexagonal architecture (ports and adapters)

## Use case
A single HTML form lets a user:

- choose one of 5 products
- enter a quantity
- submit an order
- save the order to a local JSON file

## Run the examples

### Layered version

```bash
cd layered
python main.py
```

Open `http://localhost:8000/` in your browser.

### Hexagonal version

```bash
cd hexagonal
python main.py
```

Open `http://localhost:8001/` in your browser.

## Comparing the architectures

### Brief theory

- **Layered architecture** organizes the application as a series of levels: presentation → application → infrastructure. Each layer calls the next one down.
- **Hexagonal architecture** (ports and adapters) puts the application at the center and defines interfaces (ports) at the boundaries of the application. Presentation and infrastructure then plug into these interfaces as adapters.

### Visual comparison

**Layered architecture**
```
+------------------------------+
|        WEB UI (web.py)       |
+------------------------------+
               |
               v
+------------------------------+
|     SERVICE (service.py)     |
+------------------------------+
               |
               v
+------------------------------+
|  REPOSITORY (repository.py)  |
+------------------------------+
```

**Hexagonal architecture**
```
+----------------------------------------------------+
|              WEB UI (web_adapter.py)               |
|       input adapter calling the input port         |
+----------------------------------------------------+
                         |
                         v
+----------------------------------------------------+
|               INPUT PORT (ports.py)                |
|                abstract interface                  |
+----------------------------------------------------+
                         |
                         v
+----------------------------------------------------+
|               SERVICE (service.py)                 |
|    implements input port + calls the output port   |
+----------------------------------------------------+
                         |
                         v
+----------------------------------------------------+
|              OUTPUT PORT (ports.py)                |
|                abstract interface                  |
+----------------------------------------------------+
                         |
                         v
+----------------------------------------------------+
|        REPOSITORY (repository_adapter.py)          |
|      output adapter implements the output port     |
+----------------------------------------------------+
```

### Code comparison

The code is nearly identical in both architectures—the same business logic, validation, and persistence. The key difference is **how dependencies are managed**:

**WEB UI**
- **Layered**: Constructor receives `order_service` directly, uses it as a concrete object.
- **Hexagonal**: Constructor receives `order_port` typed as `OrderInputPort`, an abstract interface. The handler doesn't know (or care) if it's a service, mock, or anything else that implements the port.

**SERVICE**
- **Layered**: Plain class `OrderService`, depends on a `repository` object passed via constructor.
- **Hexagonal**: `OrderService` inherits from `OrderInputPort` and declares the repository dependency as `OrderRepositoryPort` type. This makes the contract explicit: "I am an input port" and "I depend on something that is a repository port."

**REPOSITORY**
- **Layered**: `JsonFileOrderRepository` is a standalone class with no base requirements. It can be used anywhere the code expects it.
- **Hexagonal**: `JsonFileOrderRepository` inherits from `OrderRepositoryPort` and implements its interface. This makes it a concrete adapter that fulfills a port contract.

### Summary

Layered is straightforward and pragmatic—it relies on duck typing and direct dependencies. Hexagonal makes boundaries explicit through abstract ports, making it easier to swap implementations, write tests with mocks, and understand the system's contract at a glance.