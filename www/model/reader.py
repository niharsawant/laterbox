from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

import model

class Reader(model.Base):
  __tablename__ = 'reader'

  id = Column(Integer, primary_key=True)

  email = Column(Unicode(255), nullable=False, unique=True)
  password_hash = Column(Unicode(255), nullable=False)
  firstname = Column(Unicode(255))
  lastname = Column(Unicode(255))

  created_tstamp = Column(DateTime, default=datetime.utcnow)

  def __init__(self, email, password_hash):
    self.email = email
    self.password_hash = password_hash
