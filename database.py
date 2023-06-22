from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database_url = 'sqlite:///./blog.db'

database_url = 'mysql+mysqlconnector://root:root@localhost:3306/usertest'

# engine = create_engine(database_url, connect_args={'check_same_thread': False})

engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
