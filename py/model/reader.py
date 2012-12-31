from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

import model
import utils

class Reader(model.Base):
  __tablename__ = 'reader'

  id = Column(Integer, primary_key=True)

  email = Column(Unicode(255), nullable=False, unique=True)
  password_hash = Column(Unicode(255), nullable=False)
  firstname = Column(Unicode(255))
  lastname = Column(Unicode(255))

  created_tstamp = Column(DateTime, default=datetime.utcnow)

  article_reader_assoc = relationship('ArticleReader', lazy='joined')

  def __init__(self, email, password_hash):
    self.email = email
    self.password_hash = password_hash

  def to_dict(self):
    return dict(
      firstname = self.firstname,
      lastname = self.lastname,
      email = self.email,
      joined = self.created_tstamp.strftime(utils.DATETIME_FORMAT)
    )

  def add_article(self, session, article):
    assoc = model.ArticleReader()
    assoc.reader_id = self.id
    assoc.article_id = article.id

    session.add(assoc)
    session.commit()
