from sqlalchemy import Column, Integer, String
from .database import Base

class Sugestao(Base):
    __tablename__ = "sugestoes"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(255), nullable=False)
