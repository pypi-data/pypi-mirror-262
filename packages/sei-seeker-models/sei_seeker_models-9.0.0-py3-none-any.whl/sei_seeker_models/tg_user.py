from sqlalchemy import Column, String, BIGINT, Integer
from sqlalchemy.orm import relationship
from sei_seeker_models.base import Base


class TgUserModel(Base):
    __tablename__ = 'tg_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    user_id = Column(BIGINT, nullable=False, unique=True)

    snipe_jobs = relationship("SnipeJobModel", back_populates="user")
