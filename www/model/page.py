
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

import model

class Page(model.Base):
  __tablename__ = 'page'

  id = Column(Integer, primary_key=True)

  url = Column(Unicode(255), nullable=False)
  title = Column(Unicode(255))
  md5_hash = Column(Unicode(32), nullable=False, unique=True)

  created_tstamp = Column(DateTime, default=datetime.utcnow)
