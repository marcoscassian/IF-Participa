from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

DATABASE_URL = "sqlite:///ifparticipa.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = scoped_session(sessionmaker(bind=engine))

db_session = SessionLocal

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def criar_tabelas():
    Base.metadata.create_all(bind=engine)
