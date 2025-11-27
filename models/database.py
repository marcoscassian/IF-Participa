from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///ifparticipa.db")
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def criar_tabelas():
    from models.users import Usuario
    from models.propostas import Proposta

    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Pronto!")

if __name__ == "__main__":
    criar_tabelas()
