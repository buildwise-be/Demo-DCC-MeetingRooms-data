from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Create a single Base instance
Base = declarative_base()

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="db",
    port="5432",
    database="postgres"
)

# Create engine
engine = create_engine(url, echo=False)

# Create sessionmaker
Session = sessionmaker(bind=engine)