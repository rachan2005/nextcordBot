# bot/models/user_settings.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserSettings(Base):
    __tablename__ = 'user_settings'

    user_id = Column(Integer, primary_key=True, index=True)
    favorite_color = Column(String, nullable=True)
    timezone = Column(String, nullable=True)
    # Add more fields as needed

    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id}, favorite_color={self.favorite_color}, timezone={self.timezone})>"
