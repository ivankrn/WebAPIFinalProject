from typing import List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

import schemas
from sqlalchemy.orm import Session
from database import get_db
from database_control import (
    create_category, get_categories, get_category, update_category, delete_category,
    create_bug, get_bugs, get_bug, update_bug, delete_bug
)

router_websocket = APIRouter()
router_bugs = APIRouter(prefix='/bugs', tags=['bug'])
router_categories = APIRouter(prefix='/categories', tags=['category'])

class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_message_to(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)



manager = ConnectionManager()


async def notify_users(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{nickname}")
async def websocket_endpoint(websocket: WebSocket, nickname: str):
    await manager.connect(websocket)
    await manager.broadcast(f"Клиент {nickname} присоединился.")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Клиент {nickname} прислал сообщение: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Клиент #{nickname} отсоединился.")


@router_bugs.post("/", response_model=schemas.Bug)
async def create_bug_route(schema: schemas.BugCreate, db: Session = Depends(get_db)):
    bug = create_bug(db, schema)
    await notify_users(f"Добавлен баг: {bug.name}")
    return bug

@router_bugs.get("/", response_model=List[schemas.Bug])
async def read_bugs(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    bugs = get_bugs(db, skip=skip, limit=limit)
    return bugs

@router_bugs.get("/{bug_id}", response_model=schemas.Bug)
async def read_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = get_bug(db, bug_id)
    if bug:
        return bug
    raise HTTPException(status_code=404, detail="Баг не найден")

@router_bugs.patch("/{bug_id}")
async def update_bug_route(bug_id: int, schema: schemas.BugUpdate, db: Session = Depends(get_db)):
    new_bug = update_bug(db, bug_id, schema)
    if new_bug:
        await notify_users(f"Баг обновлен: {new_bug.name}")
        return new_bug
    raise HTTPException(status_code=404, detail="Баг не найден")

@router_bugs.delete("/{bug_id}")
async def delete_bug_route(bug_id: int, db: Session = Depends(get_db)):
    bug = delete_bug(db, bug_id)
    if bug:
        await notify_users(f"Удален баг с id: {bug_id}")
        return {"message": "Баг удален"}
    raise HTTPException(status_code=404, detail="Баг не найден")


@router_categories.post("/", response_model=schemas.Category)
async def create_category_route(category_data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = create_category(db, category_data)
    await notify_users(f"Добавлена новая категория багов: {category.name}")
    return category

@router_categories.get("/", response_model=List[schemas.Category])
async def read_categories(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    categories = get_categories(db, skip=skip, limit=limit)
    return categories

@router_categories.get("/{category_id}", response_model=schemas.Category)
async def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    if category:
        return category
    raise HTTPException(status_code=404, detail="Категория не найдена")

@router_categories.patch("/{category_id}", response_model=schemas.Category)
async def update_category_route(category_id: int, category_data: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    new_category = update_category(db, category_id, category_data)
    if new_category:
        await notify_users(f"Категория багов обновлена: {new_category.name}")
        return new_category
    raise HTTPException(status_code=404, detail="Категория не найдена")

@router_categories.delete("/{category_id}")
async def delete_category_route(category_id: int, db: Session = Depends(get_db)):
    category = delete_category(db, category_id)
    if category:
        await notify_users(f"Удалена категория с id: {category_id}")
        return {"message": "Категория удалена"}
    raise HTTPException(status_code=404, detail="Категория не найдена")
