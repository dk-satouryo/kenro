from datetime import datetime
from database import db
from sqlalchemy import Column, String, DateTime


class Post(db.Model):
    __tablename__ = "posts"

    user_id = Column(String(255), primary_key=True, nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content
