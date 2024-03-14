from sqlalchemy import Column, String, Integer, Float, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from sei_seeker_models.base import Base

class SnipeJobModel(Base):
    __tablename__ = 'snipe_job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    status = Column(String)
    collection = Column(String)
    user_id = Column(BIGINT, ForeignKey('tg_user.user_id'))
    collection_id = Column(Integer, ForeignKey('collection.id'))

    collection = relationship("CollectionModel", back_populates="snipe_jobs")
    user = relationship("TgUserModel", back_populates="snipe_jobs")

