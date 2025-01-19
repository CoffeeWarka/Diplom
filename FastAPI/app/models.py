from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Worker(Base):
    __tablename__ = 'workers'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    salary = Column(Integer)

    group = relationship('Group', backref='workers')


class Group(Base):
    __tablename__ = 'groups'
    __table_args__ = {'keep_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    occupation = Column(String)
    curator = Column(String)
    bonus = Column(Boolean)
    since = Column(Integer)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=True, index=True)