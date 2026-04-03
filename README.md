# Joyas Misterio · MVP Asistente para Vivos de Facebook

MVP funcional para operación rápida de ventas en vivo.

> ⚡ Si te perdiste con dónde pegar cada archivo, abrí primero **START_HERE.md** (guía paso a paso para principiantes).

## A) Idea general del sistema
Un **panel web operativo en tiempo real** para que dos personas puedan:
- ver comentarios entrantes,
- detectar intención de compra automáticamente,
- priorizar atención (compra > precio > consulta),
- cambiar estado del pedido con botones grandes.

## B) Arquitectura completa (versión MVP)
- **Frontend (JavaScript + HTML/CSS):** tablero en tiempo real para operador.
- **Backend (Python/FastAPI):** API REST + WebSocket para sincronización instantánea.
- **Persistencia (SQLite + SQLAlchemy):** tickets/comentarios y catálogo de productos.
- **Clasificador simple por reglas:** palabras clave + coincidencia por nombre de producto.
- **Modo simulación:** endpoint que genera comentarios de prueba.

### Diseño preparado para escalar
Separado por capas:
1. `classifier.py` (lógica de intención)
2. `models.py` (dominio)
3. `main.py` (orquestación/API)
4. `frontend/app.js` (UX operativa)

Cuando integres Meta, reemplazás/extendés solo la capa de ingesta de comentarios.

## C) Carpetas y archivos del proyecto
```text
backend/
  requirements.txt
  app/
    __init__.py
    main.py
    database.py
    models.py
    schemas.py
    classifier.py
    realtime.py
frontend/
  index.html
  styles.css
  app.js
README.md
```

## D) Tecnologías exactas
- **Backend:** Python 3.11+, FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **Frontend:** HTML5, CSS3, JavaScript vanilla
- **Base de datos:** SQLite
- **Realtime:** WebSocket nativo de FastAPI

## E) Flujo de datos paso a paso
1. Llega comentario (manual o simulado).
2. Backend clasifica prioridad por palabras clave.
3. Backend detecta producto (match por nombre).
4. Guarda ticket en SQLite con estado `pending`.
5. Publica evento por WebSocket.
6. Frontend refresca cola priorizada.
7. Operador pulsa botón rápido: `responded`, `reserved` o `sold`.
8. Backend actualiza estado y vuelve a emitir evento realtime.

## F) MVP mínimo viable (lo que ya cubre)
- Cola priorizada en vivo.
- Buscador/listado de productos.
- Detección automática (`mío`, `me lo llevo`, `precio`, `separo`, nombre de producto).
- Ficha rápida por clienta.
- Botones rápidos de estado.
- Historial visible.
- Modo simulación sin Facebook.

## G) Código inicial completo
Ya incluido en `backend/` y `frontend/`.

## H) Explicación simple de cada archivo
- `backend/app/main.py`: API principal, endpoints, WebSocket, simulación.
- `backend/app/models.py`: tablas `Product` y `Comment` + enums.
- `backend/app/database.py`: engine SQLite y sesión.
- `backend/app/schemas.py`: contratos de entrada/salida.
- `backend/app/classifier.py`: reglas de prioridad e identificación de producto.
- `backend/app/realtime.py`: manager de conexiones WebSocket.
- `frontend/index.html`: layout operativo.
- `frontend/styles.css`: UI clara, grande y rápida.
- `frontend/app.js`: consumo API, websocket, render y acciones rápidas.

## I) Qué hacer primero, segundo y tercero
1. **Primero:** correr MVP local y validar flujo operativo en simulación.
2. **Segundo:** ajustar keywords reales de tu audiencia argentina.
3. **Tercero:** conectar ingesta real de comentarios de Meta (cuando habilites app/permisos).

## J) Cómo probarlo localmente
### 1. Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend (servidor estático)
En otra terminal:
```bash
cd frontend
python -m http.server 5500
```

Abrí: `http://localhost:5500`

## K) Cómo adaptar luego a comentarios reales de Facebook
> Importante: la API de Meta depende de permisos, revisión de app y flujo oficial vigente.
> Sin esos permisos no se puede confirmar acceso completo a comentarios en producción.

Estrategia recomendada:
1. Crear módulo nuevo `backend/app/meta_ingest.py`.
2. Implementar webhook de Meta (Graph API) para recibir comentarios.
3. Normalizar payload recibido a `CommentIn`.
4. Reusar `create_comment()` para clasificación + guardado + realtime.
5. Añadir tabla de idempotencia (`external_comment_id`) para no duplicar.

## L) Recomendaciones para escalar
1. Migrar SQLite -> PostgreSQL al crecer volumen.
2. Meter cola asíncrona (Redis + worker) para NLP más avanzado.
3. Añadir autenticación simple por roles (operadora/admin).
4. Guardar respuestas enviadas para métricas de conversión.
5. Incorporar scoring semántico (modelo ML) manteniendo fallback por reglas.
6. Crear tests automáticos de clasificación y APIs críticas.

---

## Endpoints principales
- `GET /health`
- `GET /products?search=...`
- `GET /tickets`
- `POST /comments`
- `PATCH /tickets/{id}/status`
- `POST /simulate`
- `GET /history`
- `WS /ws/live`

## Nota de producto
Este MVP está optimizado para **velocidad operativa durante vivo** y para que puedas aprender construyéndolo en pasos profesionales.
