from sqlalchemy import Column, Integer, String

from task_manager.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(150))
    status = Column(String(20))
