
import os
import urllib
import json

from tornado import ioloop, web, template
from readability.readability import Document
from sqlalchemy.orm import sessionmaker
from libs.asyncs3 import AWSAuthConnection

import model
from model import page
from libs import shortner

SOURCE_DIR = os.path.join(os.environ['HOME'], 'git/laterbox')
AWS_ACESS_KEY = 'AKIAJO6GMSYEBEBTGFQA'
AWS_SECRET = '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'
AWS_ARTICLE_DIR = 'articles/'
BUCKET_NAME = 's3-apparatus'
DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'

class MainHandler(web.RequestHandler):
  def get(self):
    file_path = os.path.join(SOURCE_DIR, 'index.html')
    self.write(template.Template(open(file_path).read()).generate())
    self.finish()

class ReadHandler(web.RequestHandler):
  def get(self):
    session = sessionmaker(bind=model.Base.metadata.bind)()
    article_list = []

    for article in session.query(page.Page).all():
      article_list.append(dict(
        uid = shortner.from_decimal(article.id),
        url = article.url,
        title = article.title,
        description = article.description,
        created_tstamp = article.created_tstamp.strftime(DATETIME_FORMAT)
      ))

    self.write(json.dumps({'result': 'SUCCESS', 'articles': article_list}))
    session.close()
    self.finish()

class FetchHandler(web.RequestHandler):
  def s3_download_complete(self, response):

    params = dict(
      uid = self.uid,
      url = self.article.url,
      body = response.body,
      title = self.article.title,
      description = self.article.description,
      created_tstamp = self.article.created_tstamp.strftime(DATETIME_FORMAT)
    )

    self.write(json.dumps({'result': 'SUCCESS', 'article': params}))
    self.session.close()
    self.finish()

  @web.asynchronous
  def get(self):
    self.uid = self.get_argument('q', None)

    self.session = sessionmaker(bind=model.Base.metadata.bind)()
    article_id = shortner.to_decimal(self.uid)
    self.article = self.session.query(page.Page).filter_by(id=article_id).one()

    aws = AWSAuthConnection(AWS_ACESS_KEY, AWS_SECRET, is_secure=False)
    aws.get(BUCKET_NAME, AWS_ARTICLE_DIR+self.article.md5_hash,
      callback=self.s3_download_complete
    )

class AddHandler(web.RequestHandler):
  def s3_upload_complete(self, response):
    from lxml import html

    info = html.document_fromstring(self.article_body).text_content().strip()[:500]
    article = page.Page(self.url, self.article_md5,
      title=self.article_title, description=info)

    self.session.add(article)
    self.session.commit()
    self.session.close()

  def uploadToS3(self):
    import hashlib

    self.article_body = self.article_body.encode('ascii', 'ignore')
    self.article_md5 = hashlib.md5(self.article_body).hexdigest()
    exists = self.session.query(page.Page).filter_by(md5_hash=self.article_md5).count()
    if exists :
      self.finish()
      self.session.close()
      return

    aws = AWSAuthConnection(AWS_ACESS_KEY, AWS_SECRET, is_secure=False)
    aws.put(BUCKET_NAME, AWS_ARTICLE_DIR+self.article_md5, self.article_body,
      {'Content-Type' : 'text/html', 'x-amz-acl' : 'public-read'},
      callback=self.s3_upload_complete
    )

  @web.asynchronous
  def post(self):
    self.session = sessionmaker(bind=model.Base.metadata.bind)()

    url = self.get_argument('url', None)
    exists = self.session.query(page.Page).filter_by(url=url).count()
    if exists :
      self.finish()
      self.session.close()
      return

    doc = urllib.urlopen(url)
    html = doc.read()

    self.url = doc.geturl()
    exists = self.session.query(page.Page).filter_by(url=self.url).count()
    if exists :
      self.finish()
      self.session.close()
      return

    self.article_body = Document(html).summary()
    self.article_title = Document(html).short_title()

    self.uploadToS3()

    self.redirect('/')

settings = dict(
  debug=True
)

handler_list = [
  ('/', MainHandler),
  ('/add', AddHandler),
  ('/read', ReadHandler),
  ('/fetch', FetchHandler)
]

application = web.Application(handler_list, **settings)
model.start_engine()

if __name__ == "__main__":
  application.listen(8000)
  print 'Running on port 8000'
  ioloop.IOLoop.instance().start()
