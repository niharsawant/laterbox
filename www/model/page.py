
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

import model

class Page(model.Base):
  __tablename__ = 'page'

  id = Column(Integer, primary_key=True)

  url = Column(Unicode(255), nullable=False)
  title = Column(Unicode(255))
  description = Column(String(500))
  md5_hash = Column(Unicode(32), nullable=False, unique=True)

  created_tstamp = Column(DateTime, default=datetime.utcnow)

  def __init__(self, url, md5_hash, title=None, description=None):
    self.url = url
    self.title = title
    self.description = description
    self.md5_hash = md5_hash
