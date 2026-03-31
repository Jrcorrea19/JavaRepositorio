from __future__ import annotations

import random
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import case, desc, select
from sqlalchemy.orm import Session

from .classifier import detect_priority, detect_product
from .database import SessionLocal, init_db
from .models import AttentionPriority, Comment, Product, TicketStatus
from .realtime import ConnectionManager
from .schemas import CommentIn, CommentOut, CommentStatusUpdate, ProductOut

app = FastAPI(title="Joyas Misterio Live Assistant", version="0.1.0")
manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SIMULATED_COMMENTS = [
    ("María López", "Mío el anillo luna"),
    ("Carla Benítez", "Precio de collar estrellas"),
    ("Ana Gómez", "Me lo llevo, separo el set dorado"),
    ("Lucía Pérez", "¿Tienen en plateado?"),
    ("Sofía Ruiz", "Quiero el aro corazón"),
]


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    seed_products()


def seed_products() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(Product.id).limit(1)):
            return
        sample_products = [
            Product(sku="ANL-001", name="Anillo Luna", price_ars=18000, stock=5),
            Product(sku="COL-014", name="Collar Estrellas", price_ars=22000, stock=7),
            Product(sku="SET-007", name="Set Dorado", price_ars=30000, stock=3),
            Product(sku="ARO-021", name="Aro Corazón", price_ars=15000, stock=9),
        ]
        db.add_all(sample_products)
        db.commit()
    finally:
        db.close()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.get("/products", response_model=list[ProductOut])
def list_products(search: str | None = Query(default=None), db: Session = Depends(get_db)) -> list[Product]:
    stmt = select(Product)
    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    stmt = stmt.order_by(Product.name.asc())
    return list(db.scalars(stmt).all())


@app.get("/tickets", response_model=list[CommentOut])
def list_tickets(limit: int = 50, db: Session = Depends(get_db)) -> list[Comment]:
    priority_order = case(
        (Comment.priority == AttentionPriority.PURCHASE, 0),
        (Comment.priority == AttentionPriority.PRICE, 1),
        else_=2,
    )
    stmt = (
        select(Comment)
        .order_by(priority_order.asc(), Comment.created_at.asc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


@app.post("/comments", response_model=CommentOut, status_code=201)
async def create_comment(payload: CommentIn, db: Session = Depends(get_db)) -> Comment:
    product_names = list(db.scalars(select(Product.name)).all())
    priority = detect_priority(payload.message)
    product_name = detect_product(payload.message, product_names)

    comment = Comment(
        customer_name=payload.customer_name,
        message=payload.message,
        product_name=product_name,
        priority=priority,
        status=TicketStatus.PENDING,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    await manager.broadcast_json({"event": "new_comment", "data": CommentOut.model_validate(comment).model_dump(mode="json")})
    return comment


@app.patch("/tickets/{ticket_id}/status", response_model=CommentOut)
async def update_ticket_status(
    ticket_id: int,
    payload: CommentStatusUpdate,
    db: Session = Depends(get_db),
) -> Comment:
    comment = db.get(Comment, ticket_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    comment.status = payload.status
    db.commit()
    db.refresh(comment)

    await manager.broadcast_json(
        {"event": "status_updated", "data": CommentOut.model_validate(comment).model_dump(mode="json")}
    )
    return comment


@app.post("/simulate", response_model=CommentOut, status_code=201)
async def simulate_comment(db: Session = Depends(get_db)) -> Comment:
    customer_name, message = random.choice(SIMULATED_COMMENTS)
    payload = CommentIn(customer_name=customer_name, message=message)
    return await create_comment(payload=payload, db=db)


@app.get("/history", response_model=list[CommentOut])
def history(
    limit: int = Query(default=100, le=300),
    db: Session = Depends(get_db),
) -> list[Comment]:
    stmt = select(Comment).order_by(desc(Comment.created_at)).limit(limit)
    return list(db.scalars(stmt).all())


@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
