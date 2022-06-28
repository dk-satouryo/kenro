from datetime import datetime
from database import db
from sqlalchemy import Column, Integer, String, DateTime


class Post(db.Model):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    uid = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, uid, title, content):
        self.uid = uid
        self.title = title
        self.content = content
