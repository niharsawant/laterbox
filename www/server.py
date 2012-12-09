
import os
import urllib
import json

from tornado import ioloop, web, template
from lib.readability.readability import Document
from sqlalchemy.orm import sessionmaker
from lib.asyncs3 import AWSAuthConnection

import g
from model import *
from lib import shortner

class MainHandler(web.RequestHandler):
  def get(self):
    try:
      file_path = os.path.join(g.SOURCE_DIR, 'index.html')
      self.write(template.Template(open(file_path).read()).generate())
    except Exception, e:
      g.log_error()
      self.write(json.dumps({'result' : 'unknown_error'}))
    finally:
      self.finish()

class ReadingListHandler(web.RequestHandler):
  def get(self):
    try:
      session = sessionmaker(bind=Base.metadata.bind)()
      article_list = []
      for article in session.query(Page).all():
        article_list.append(dict(
          id = shortner.from_decimal(article.id),
          url = article.url,
          title = article.title,
          description = article.description,
          created_tstamp = article.created_tstamp.strftime(g.DATETIME_FORMAT)
        ))

      self.write(json.dumps(article_list))
      session.close()
      self.finish()
    except Exception, e:
      session.close()
      self.error = e
      self.send_error()

  def write_error(self, status_code):
    g.log_error()
    self.set_header('Content-Type', 'text/plain')
    self.finish('{ "message" : "%s" }' % self.error.message)

class ArticleHandler(web.RequestHandler):
  def s3_download_complete(self, response):
    try:
      if response.error:
        raise g.AppException('s3_download_failed')
      params = dict(
        id = self.uid,
        url = self.article.url,
        body = response.body,
        title = self.article.title,
        description = self.article.description,
        created_tstamp = self.article.created_tstamp.strftime(g.DATETIME_FORMAT)
      )

      self.write(json.dumps(params))
    except Exception, e:
      g.log_error()
      self.write(json.dumps({'result' : 'unknown_error'}))
    finally:
      self.session.close()
      self.finish()

  @web.asynchronous
  def get(self, id):
    try:
      self.uid = id

      self.session = sessionmaker(bind=Base.metadata.bind)()
      article_id = shortner.to_decimal(self.uid)
      self.article = self.session.query(Page).filter_by(id=article_id).one()

      aws = AWSAuthConnection(g.AWS_ACESS_KEY, g.AWS_SECRET, is_secure=False)
      aws.get(g.BUCKET_NAME, g.AWS_ARTICLE_DIR+self.article.md5_hash,
        callback=self.s3_download_complete
      )
    except Exception, e:
      g.log_error()
      self.write(json.dumps({'result' : 'unknown_error'}))

class AddHandler(web.RequestHandler):
  def s3_upload_complete(self, response):
    try:
      from lxml import html

      info = html.document_fromstring(self.article_body).text_content().strip()[:500]
      article = Page(self.url, self.article_md5,
        title=self.article_title, description=info)

      self.session.add(article)
      self.session.commit()
    except Exception, e:
      g.log_error()
      self.write(json.dumps({'result' : 'unknown_error'}))
    finally:
      self.session.close()

  def uploadToS3(self):
    try:
      import hashlib

      self.article_body = self.article_body
      self.article_md5 = hashlib.md5(self.article_body).hexdigest()

      exists = self.session.query(Page).filter_by(md5_hash=self.article_md5).count()
      if exists :
        raise g.AppException('article_already_exists')

      aws = AWSAuthConnection(g.AWS_ACESS_KEY, g.AWS_SECRET, is_secure=False)
      aws.put(g.BUCKET_NAME, g.AWS_ARTICLE_DIR+self.article_md5, self.article_body,
        {'Content-Type' : 'text/html', 'x-amz-acl' : 'public-read'},
        callback=self.s3_upload_complete
      )
    except g.AppException, e:
      g.log_error()
      self.write(json.dumps({'result' : e.message}))
      self.session.close()
      self.finish()
    except Exception, e:
      g.log_error()
      self.write(json.dumps({'result' : 'unknown_error'}))
      self.session.close()

  @web.asynchronous
  def post(self):
    try:
      self.session = sessionmaker(bind=Base.metadata.bind)()

      url = self.get_argument('url', None)
      exists = self.session.query(Page).filter_by(url=url).count()
      if exists :
        raise g.AppException('article_already_exists')

      doc = urllib.urlopen(url)
      html = doc.read()

      self.url = doc.geturl()
      exists = self.session.query(Page).filter_by(url=self.url).count()
      if exists :
        raise g.AppException('article_already_exists')

      self.article_body = Document(html).summary().encode('utf-8')
      self.article_title = Document(html).short_title()

      self.uploadToS3()

      self.redirect('/')

    except g.AppException, e:
      g.log_error()
      self.write(json.dumps({'result' : e.message}))
      self.session.close()
      self.finish()
    except Exception, e:
      g.log_error()
      self.write(json.dumps({'result' : 'unknown_error'}))
      self.session.close()
      self.finish()

settings = dict(
  debug=True
)

handler_list = [
  ('/', MainHandler),
  ('/add', AddHandler),
  ('/article/([^_].*)', ArticleHandler),
  ('/read', ReadingListHandler),

  ('/js/(.*)', web.StaticFileHandler, {'path' : os.path.join(g.SOURCE_DIR, 'js')}),
  ('/css/(.*)', web.StaticFileHandler, {'path' : os.path.join(g.SOURCE_DIR, 'css')})
]

application = web.Application(handler_list, **settings)
start_engine()

if __name__ == "__main__":
  application.listen(8000)
  print 'Running on port 8000'
  ioloop.IOLoop.instance().start()
