# db.py (or any other module where you want to define the Base class)
from sqlalchemy.orm import declarative_base

# Define a single Base class for all models
Base = declarative_base()
