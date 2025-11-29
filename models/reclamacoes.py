from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Reclamacao(Base):
    __tablename__ = "reclamacoes"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(Text, nullable=False)

    autor_id = Column(Integer, ForeignKey("usuarios.id"))
    autor = relationship("Usuario", back_populates="reclamacoes")
