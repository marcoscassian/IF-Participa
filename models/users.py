from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
from flask_login import UserMixin

class Usuario(Base, UserMixin):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(200), nullable=False)

    sugestoes = relationship("Sugestao", back_populates="autor")

