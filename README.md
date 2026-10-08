# OpenAPI

API REST hecha con **FastAPI** que expone un CRUD de productos y un endpoint que conecta con un **LLM a través de OpenCode**.

Proyecto de aprendizaje basado en el video de *Hola Mundo*: ["Tienes que aprender FastAPI ahora, es increíble!"](https://www.youtube.com/watch?v=WrnFtgGLO38)

---

## Stack

- **FastAPI** — framework web con soporte async
- **Pydantic** — validación de datos y schemas
- **Uvicorn** — servidor ASGI
- **httpx** — cliente async para llamar al LLM

## Qué incluye

- CRUD completo de productos (en memoria, sin base de datos)
- Endpoint `/llm/ask` que le manda un prompt al LLM de OpenCode y devuelve la respuesta
- **Documentación interactiva automática** en `/docs` (Swagger) y `/redoc`

---

## Instalación

```bash
git clone https://github.com/devGabLen/OpenAPI.git
cd OpenAPI

python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn main:app --reload
```

La API queda en **http://127.0.0.1:8000**

---

## Endpoints

### Productos

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/products/` | Lista productos (`?limit=10`) |
| `GET` | `/products/{id}` | Devuelve un producto |
| `POST` | `/products/` | Crea un producto (201) |
| `DELETE` | `/products/{id}` | Borra un producto |

`name` (mín. 3 caracteres), `price` (> 0) y `stock` (≥ 0) son obligatorios. `description` es opcional.

```bash
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Teclado", "price": 15000, "stock": 5}'
```

> Los productos se guardan **en memoria**: al reiniciar el server se pierden.

### LLM

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/llm/ask` | Envía un prompt al LLM y devuelve la respuesta |

```bash
curl -X POST http://127.0.0.1:8000/llm/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explica qué es FastAPI en una oración"}'
```

```json
{ "answer": "FastAPI es un framework web moderno y rápido para construir APIs con Python..." }
```

### Documentación

| Ruta | Qué hay |
|---|---|
| `/docs` | Swagger UI (probador interactivo) |
| `/redoc` | ReDoc |

---

## Requisito del endpoint `/llm/ask`

Este endpoint no tiene su propia API key: **usa el LLM que ya tenés configurado en OpenCode**, a través del servicio local de OpenCode.

- Tenés que tener **OpenCode instalado y corriendo** en la máquina donde corre la API.
- El server lee la URL y credencial del servicio desde `~/.local/state/opencode/service.json`.
- El puerto cambia cada vez que se reinicia OpenCode, así que se resuelve en cada request.
- Si no hay servicio disponible, el endpoint responde `503`.

> **Modelo:** por defecto usa `opencode/mimo-v2.6-flash-free`. Está definido en la constante `MODEL` de `routers/llm.py` — cambialo ahí si querés otro.

---

## Estructura

```
openapi/
├── main.py              # App FastAPI, monta los routers
├── schemas.py           # Modelos Pydantic (Product)
├── storage.py           # Almacenamiento en memoria
├── requirements.txt
└── routers/
    ├── products.py      # CRUD de productos
    └── llm.py           # Conexión al LLM de OpenCode
```

---

## Licencia

Proyecto de estudio. Créditos del video original a [Hola Mundo](https://www.youtube.com/watch?v=WrnFtgGLO38).
