from sqlalchemy.orm import Session
from models import Category, Bug

import schemas

def create_bug(db: Session, schema: schemas.BugCreate):
    bug = Bug(**schema.model_dump())
    db.add(bug)
    db.commit()
    db.refresh(bug)
    return bug

def get_bugs(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Bug).offset(skip).limit(limit).all()

def get_bug(db: Session, bug_id: int):
    return db.query(Bug).filter_by(id=bug_id).first()

def update_bug(db: Session, bug_id: int, bug_data: schemas.BugUpdate | dict):
    bug = db.query(Bug).filter_by(id=bug_id).first()
    bug_data = bug_data if isinstance(bug_data, dict) else bug_data.model_dump()
    if bug:
        for key, value in bug_data.items():
            if hasattr(bug, key):
                setattr(bug, key, value)
        db.commit()
        db.refresh(bug)
        return bug
    return None

def delete_bug(db: Session, bug_id: int):
    bug = db.query(Bug).filter_by(id=bug_id).first()
    if bug:
        db.delete(bug)
        db.commit()
        return True
    return False


def create_category(db: Session, schema: schemas.CategoryCreate):
    category = Category(**schema.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter_by(id=category_id).first()

def update_category(db: Session, category_id: int, category_data: schemas.CategoryUpdate | dict):
    category = db.query(Category).filter_by(id=category_id).first()
    category_data = category_data if isinstance(category_data, dict) else category_data.model_dump()
    if category:
        for key, value in category_data.items():
            if hasattr(category, key):
                setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter_by(id=category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False