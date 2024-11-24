from sqlalchemy import Column, Integer, String, Float
from .db import Base

class SearchProfile(Base):
    __tablename__ = "search_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    keyword = Column(String, index=True, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    category = Column(String, nullable=True)
