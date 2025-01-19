from fastapi import APIRouter, Depends, status, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from app.models import Worker, Group
from app.schemas import CreateWorker, UpdateWorker
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=['Worker'], prefix='/workers')

@router.get('/')
async def all_workers(database: Annotated[Session, Depends(get_db)], request: Request):
    workers = database.scalars(select(Worker)).all()
    if workers is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет работников в списке')
    return templates.TemplateResponse('workers.html', {'request': request, 'workers': workers})

@router.get('/{worker_id}')
async def worker_by_id(database: Annotated[Session, Depends(get_db)], worker_id: int):
    worker = database.scalar(select(Worker).where(Worker.id == worker_id))
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден")
    return worker

@router.get('/{worker_id}/groups')
async def groups_by_user_id(database: Annotated[Session, Depends(get_db)], worker_id: int):
    groups = database.scalars(select(Group).where(Group.worker_id == worker_id).all())
    return groups

@router.post('/create')
async def create_worker(database: Annotated[Session, Depends(get_db)], create_worker: CreateWorker):
    create_data = create_worker.model_dump(exclude_unset=True)
    database.execute(insert(Worker).values(create_data))
    database.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Успешно!'}

@router.patch('/{worker_id}')
async def update_worker(database: Annotated[Session, Depends(get_db)], worker_id: int, update_worker: UpdateWorker):
    update_data = update_worker.dict(exclude_unset=True)
    worker = database.scalar(select(Worker).where(Worker.id == worker_id))
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден")
    database.execute(update(Worker).where(Worker.id==worker_id).values(update_data))
    database.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': f'Запись работника {worker.id}({worker.firstname}) успешно обновлена!'}

@router.delete('/{worker_id}')
async def delete_worker(database: Annotated[Session, Depends(get_db)], worker_id: int):
    worker = database.scalar(select(Worker).where(Worker.id == worker_id))
    if worker is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    database.execute(delete(Worker).where(Worker.id == worker_id))
    database.execute(delete(Group).where(Group.worker_id == worker_id))
    database.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Работник успешно удалён!'}