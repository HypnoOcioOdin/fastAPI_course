from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import text

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# with engine.connect() as conn:
#     conn.detach()
#     conn.execute(text("DROP TABLE users"))