from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Base.metadata = MetaData()

import page
Page = page.Page
import reader
Reader = reader.Reader

def start_engine():
  engine = create_engine('mysql://www:password@localhost/laterbox_db', echo=False)
  Base.metadata.bind = engine
