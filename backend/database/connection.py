from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
# from database.models import Menu, OrderHistory 


url = 'sqlite:///al-maidah3.sqlite'

engine = create_engine(url, json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False, default=str))
# SessionLocal = async_sessionmaker(autocommit=False, bind=engine)

# create engine for db connection

# sessionmaker returns a customized class from which we create sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

# create the base class for models to inherit
Base = declarative_base()

# Menu.metadata.create_all(engine)
# OrderHistory.metadata.create_all(engine)

# Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()