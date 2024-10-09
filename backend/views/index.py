# models.py
from sqlalchemy import Column, String
from sqlalchemy.orm import Session
from database.sql import Base
import uuid

class Project(Base):
    __tablename__ = 'projects'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    badge = Column(String, nullable=False)
    date = Column(String, nullable=False)
    zip_path = Column(String, nullable=False)
    description = Column(String, nullable=False)


def create_project(db: Session, name: str, badge: str, date: str, zip_path: str, description: str) -> Project:
    db_project = Project(
        id=str(uuid.uuid4()),  # 生成唯一的 UUID
        name=name,
        badge=badge,
        date=date,
        zip_path=zip_path,
        description=description
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project