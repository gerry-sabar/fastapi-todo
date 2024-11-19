from sqlalchemy.orm import Session
from datetime import datetime

import models,schemas


def get_todos(db: Session, skip:int=0, limit: int=100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def delete_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).delete()


def update_todo(db: Session, update_todo: models.Todo, todo_id: int):
    todo = get_todo(db, todo_id)
    if todo is not None:        
        todo.title = update_todo.title if update_todo.title != None else todo.title
        todo.status = update_todo.status if update_todo.status != None else todo.status
        todo.updated_at = datetime.now()
        db.commit()
        db.refresh(todo)        
        return todo
    else:
        return None


def create_todo(db: Session, todo:schemas.Todo):
    db_todo = models.Todo(title=todo.title,
                          status=todo.status,
                          created_at=datetime.now(),
                          updated_at=datetime.now())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# NOTE :
# - To perform CRUD need to add object instance to the database session.
# - do commit changes
# - do refresh your instance to contain new data from the database.