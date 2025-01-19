from fastapi import FastAPI, APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from app.models import Group, Worker
from app.schemas import CreateGroup, CreateWorker, UpdateWorker, UpdateGroup

router = APIRouter(tags=['Group'], prefix='/groups')

@router.get('/all_groups')
async def all_groups(database: Annotated[Session, Depends(get_db)]):
    groups = database.scalars(select(Group)).all()
    if groups is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет групп в списке'
        )
    return groups

@router.get('/{group_id}')
async def group_by_id(database: Annotated[Session, Depends(get_db)], group_id: int):
    group = database.scalar(select(Group).where(Group.id == group_id))
    if Group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена"
        )
    return group

@router.post('/create')
async def create_group(database: Annotated[Session, Depends(get_db)], create_group: CreateGroup, worker_id: int):
    create_data = create_group.model_dump(exclude_unset=True)
    worker = database.scalar(select(Worker).where(Worker.id == worker_id))
    if worker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Работник не найден"
        )
    database.execute(insert(Group).values(create_data))
    database.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': f'Группа успешно создана!'}

@router.put('/{group_id}')
async def update_group(database: Annotated[Session, Depends(get_db)], group_id: int, update_group: UpdateGroup):
    update_data = update_group.dict(exclude_unset=True)
    group = database.scalar(select(Group).where(Group.id == group_id))
    if group is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
    database.execute(update(Group).where(Group.id == group_id).values(update_data))
    database.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': f'Группа {group.title} успешно обновлена!'}

@router.delete('/{group_id}')
async def delete_group(database: Annotated[Session, Depends(get_db)], group_id: int):
    group = database.scalar(select(Group).where(Group.id == group_id))
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Группа не найдена"
        )
    database.execute(delete(Group).where(Group.id == group_id))
    database.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Группа успешно удалена!'}
