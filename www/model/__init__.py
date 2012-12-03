from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata = MetaData()

def start_engine():
  engine = create_engine('mysql://sampadm:secret@localhost/laterbox_db', echo=True)
  Base.metadata.bind = engine
