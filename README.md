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

- **Layered architecture** organizes the application as a series of levels: presentation → application/use case → infrastructure. Each layer calls the next one down.
- **Hexagonal architecture** (ports and adapters) puts the business core at the center and defines explicit boundary contracts. The core depends on abstract ports, and concrete adapters plug into those ports.

### Visual comparison

**Layered architecture**
```
+------------+
|   web.py   |
+------------+
      |
      v
+------------+
|  service.py   |
+------------+
      |
      v
+------------+
| repository.py |
+------------+
```

hexagonal architecture
```
+-----------------------------------------------+
| WEB UI (web_adapter.py)                                |
| input adapter calling the input port          |
+-----------------------------------------------+
      |
      v
+-----------------------------------------------+
| INPUT PORT (ports.py)                                  |
+-----------------------------------------------+
      |
      v
+-----------------------------------------------+
| SERVICE (service.py)                               |
| implements input port + calls the output port |
+-----------------------------------------------+
      |
      v
+-----------------------------------------------+
| OUTPUT PORT      (ports.py)                             |
+-----------------------------------------------+
      |
      v
+-----------------------------------------------+
| REPOSITORY (repository.py)                                  |
| output adapter implements the output port    |
+-----------------------------------------------+
```