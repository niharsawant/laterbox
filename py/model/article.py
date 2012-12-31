from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *
from lib import base62

import model
import utils

class Article(model.Base):
  __tablename__ = 'article'

  id = Column(Integer, primary_key=True)

  url = Column(Unicode(255), nullable=False)
  title = Column(Unicode(255))
  description = Column(String(500))
  md5_hash = Column(Unicode(32), nullable=False, unique=True)

  created_tstamp = Column(DateTime, default=datetime.utcnow)

  article_reader_assoc = relationship('ArticleReader', lazy='joined')

  def to_dict(self):
    return dict(
      id = base62.from_decimal(self.id),
      url = self.url,
      title = self.title,
      description = self.description,
      created_tstamp = self.created_tstamp.strftime(utils.DATETIME_FORMAT)
    )

  def __init__(self, url, md5_hash, title=None, description=None):
    self.url = url
    self.title = title
    self.description = description
    self.md5_hash = md5_hash
