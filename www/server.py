
import os
import urllib
import json

from tornado import ioloop, web, template
from readability.readability import Document
from sqlalchemy.orm import sessionmaker

import model
from model import page
from libs import shortner

SOURCE_DIR = os.path.join(os.environ['HOME'], 'git/laterbox')
AWS_ACESS_KEY = 'AKIAJO6GMSYEBEBTGFQA'
AWS_SECRET = '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'
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
  def get(self):
    uid = self.get_argument('q', None)

    session = sessionmaker(bind=model.Base.metadata.bind)()
    article_id = shortner.to_decimal(uid)
    article = session.query(page.Page).filter_by(id=article_id).one()

    params = dict(
      uid = uid,
      url = article.url,
      title = article.title,
      description = article.description,
      created_tstamp = article.created_tstamp.strftime(DATETIME_FORMAT)
    )

    self.write(json.dumps({'result': 'SUCCESS', 'article': params}))
    session.close()
    self.finish()

class AddHandler(web.RequestHandler):
  def s3_callback(self, params):
    from lxml import html

    session = sessionmaker(bind=model.Base.metadata.bind)()

    info = html.document_fromstring(self.article_body).text_content().strip()[:500]
    article = page.Page(self.url, self.article_md5,
      title=self.article_title, description=info)

    session.add(article)
    session.commit()
    session.close()

  def uploadToS3(self):
    import hashlib
    import base64
    from libs.asyncs3 import AWSAuthConnection

    self.article_body = self.article_body.encode('ascii', 'ignore')
    self.article_md5 = hashlib.md5(self.article_body).hexdigest()
    aws = AWSAuthConnection(AWS_ACESS_KEY, AWS_SECRET, is_secure=False)
    article_dir = base64.b64encode(self.article_md5)+'/'

    aws.put(BUCKET_NAME, article_dir+self.article_title, self.article_body,
      {'Content-Type' : 'text/html', 'x-amz-acl' : 'public-read'},
      callback=self.s3_callback
    )

  def post(self):
    self.url = self.get_argument('url', None)
    html = urllib.urlopen(self.url).read()

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
