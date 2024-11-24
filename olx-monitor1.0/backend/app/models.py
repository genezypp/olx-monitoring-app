from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class SearchProfile(Base):
    __tablename__ = "search_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # Pole `name` jest wymagane
    keyword = Column(String, index=True, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    category = Column(String, nullable=True)

    # Relacja z modelem Listing
    listings = relationship(
        "Listing",
        back_populates="profile",
        cascade="all, delete-orphan"  # Automatyczne usuwanie powi¹zanych og³oszeñ
    )


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)  # Tytu³ og³oszenia jest wymagany
    price = Column(Float, nullable=True)
    link = Column(Text, unique=True, nullable=False)  # Unikalny link jest wymagany
    location = Column(String, nullable=True)
    category = Column(String, nullable=True)
    profile_id = Column(Integer, ForeignKey("search_profiles.id", ondelete="CASCADE"))  # Usuwanie kaskadowe

    # Relacja zwrotna do modelu SearchProfile
    profile = relationship("SearchProfile", back_populates="listings")
