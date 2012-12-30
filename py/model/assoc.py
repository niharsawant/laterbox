from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *

import model

class ArticleReader(model.Base):
  __tablename__ = 'article_reader_assoc'

  id = Column(Integer, primary_key=True)

  reader_id = Column(Integer, ForeignKey('reader.id'), primary_key=True)
  article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)

  created_tstamp = Column(DateTime, default=datetime.utcnow)

  article = relationship('Article', lazy='joined', uselist=False)
  reader = relationship('Reader', lazy='joined', uselist=False)
