
import os
import urllib
import json

from tornado import ioloop, web, template, httpclient
from lib.readability.readability import Document
from sqlalchemy.orm import sessionmaker
from lib.asyncs3 import AWSAuthConnection

import utils
from model import *
from lib import shortner

class BaseHandler(web.RequestHandler):
  def get_logged_user(self):
    reader_id = self.get_secure_cookie('__user__')
    session = sessionmaker(bind=Base.metadata.bind)()
    reader = session.query(Reader).filter(Reader.id == reader_id).first()
    session.close()

    return reader

  def log_error(self, e):
    utils.log_error()
    self.error = e
    self.send_error()

  def write_error(self, status_code):
    self.set_header('Content-Type', 'text/plain')
    self.finish('{ "message" : "%s" }' % self.error.message)

class _404Handler(BaseHandler):
  def prepare(self):
    self.error = httpclient.HTTPError(404, 'Page Not Found')
    self.send_error(status_code=404)

class WelcomeHandler(BaseHandler):
  def get(self):
    try:
      file_path = os.path.join(utils.SOURCE_DIR, 'html/welcome.html')
      self.write(template.Template(open(file_path).read()).generate())
      self.finish()
    except Exception, e:
      self.log_error(e)

  def post(self):
    try:
      email = self.get_argument('email', None)
      password = self.get_argument('password', None)
      signup_type = self.get_argument('type', None)

      if not email: raise utils.AppException('empty_email')
      if not password: raise utils.AppException('empty_password')
      if not signup_type: raise utils.AppException('empty_type')

      session = sessionmaker(bind=Base.metadata.bind)()

      import hashlib

      if signup_type == 'new':
        reader = session.query(Reader).filter(Reader.email == email).first()
        if reader: raise utils.AppException('duplicate_found')

        password_hash = hashlib.sha512(password).hexdigest()
        reader = Reader(email, password_hash)
        session.add(reader)
        session.commit()

        self.set_secure_cookie('__user__', str(reader.id))
        self.redirect('/')
      elif signup_type == 'exist':
        reader = session.query(Reader).filter(Reader.email == email).first()
        password_hash = hashlib.sha512(password).hexdigest()

        if reader is None: raise utils.AppException('invalid_email')
        if reader.password_hash != password_hash: raise utils.AppException('invalid_password')

        self.set_secure_cookie('__user__', str(reader.id))
        self.redirect('/')
      else: raise utils.AppException('invalid_type')

    except Exception, e:
      self.log_error(e)
    finally:
      session.close()

class LogoutHandler(BaseHandler):
  def get(self):
    self.clear_all_cookies()
    self.redirect('/welcome')

class MainHandler(BaseHandler):
  def get(self):
    try:
      reader = self.get_logged_user()
      if reader:
        file_path = os.path.join(utils.SOURCE_DIR, 'html/index.html')
        self.write(template.Template(open(file_path).read()).generate())
        self.finish()
      else:
        self.redirect('/welcome')

    except Exception, e:
      self.log_error(e)

class ReadingListHandler(BaseHandler):
  def get(self):
    try:
      reader = self.get_logged_user()
      if not reader:
        raise g.AppException('auth_failed')
      session = sessionmaker(bind=Base.metadata.bind)()

      article_list = []
      for assoc in reader.article_reader_assoc:
        article_list.append(dict(
          id = shortner.from_decimal(assoc.article.id),
          url = assoc.article.url,
          title = assoc.article.title,
          description = assoc.article.description,
          created_tstamp = assoc.article.created_tstamp.strftime(utils.DATETIME_FORMAT)
        ))

      self.write(json.dumps(article_list))
      session.close()
      self.finish()
    except Exception, e:
      self.log_error(e)
      session.close()

class ArticleHandler(BaseHandler):
  def s3_download_complete(self, response):
    try:
      if response.error:
        raise utils.AppException('s3_download_failed')
      params = dict(
        id = self.uid,
        url = self.article.url,
        body = response.body,
        title = self.article.title,
        description = self.article.description,
        created_tstamp = self.article.created_tstamp.strftime(utils.DATETIME_FORMAT)
      )

      self.write(json.dumps(params))
      self.finish()
    except Exception, e:
      self.log_error(e)
    finally:
      self.session.close()

  @web.asynchronous
  def get(self, id):
    try:
      self.uid = id

      self.session = sessionmaker(bind=Base.metadata.bind)()
      article_id = shortner.to_decimal(self.uid)
      self.article = self.session.query(Article).filter_by(id=article_id).one()

      aws = AWSAuthConnection(utils.AWS_ACESS_KEY, utils.AWS_SECRET, is_secure=False)
      aws.get(utils.BUCKET_NAME, utils.AWS_ARTICLE_DIR+self.article.md5_hash,
        callback=self.s3_download_complete
      )
    except Exception, e:
      self.log_error(e)
      self.session.close()

class AddHandler(BaseHandler):
  def s3_upload_complete(self, response):
    try:
      from lxml import html

      info = html.document_fromstring(self.article_body).text_content().strip()[:500]
      article = Article(self.url, self.article_md5,
        title=self.article_title, description=info)
      self.session.add(article)
      self.session.commit()

      self.reader.add_article(self.session, article)
      self.redirect('/')
    except Exception, e:
      self.log_error(e)

  def uploadToS3(self):
    try:
      import hashlib

      self.article_body = self.article_body
      self.article_md5 = hashlib.md5(self.article_body).hexdigest()

      article = self.session.query(Article).filter_by(md5_hash=self.article_md5).first()
      if article :
        self.reader.add_article(self.session, article)
        self.redirect('/')
        return

      aws = AWSAuthConnection(utils.AWS_ACESS_KEY, utils.AWS_SECRET, is_secure=False)
      aws.put(utils.BUCKET_NAME, utils.AWS_ARTICLE_DIR+self.article_md5, self.article_body,
        {'Content-Type' : 'text/html', 'x-amz-acl' : 'public-read'},
        callback=self.s3_upload_complete
      )

    except Exception, e:
      self.log_error(e)

  @web.asynchronous
  def post(self):
    try:
      self.reader = self.get_logged_user()
      if not self.reader:
        raise g.AppException('auth_failed')

      self.session = sessionmaker(bind=Base.metadata.bind)()

      url = self.get_argument('url', None)
      article = self.session.query(Article).filter_by(url=url).first()
      if article :
        self.reader.add_article(self.session, article)
        self.redirect('/')
        return

      doc = urllib.urlopen(url)
      html = doc.read()

      self.url = doc.geturl()
      article = self.session.query(Article).filter_by(url=self.url).first()
      if article :
        self.reader.add_article(self.session, article)
        self.redirect('/')
        return

      self.article_body = Document(html).summary().encode('utf-8')
      self.article_title = Document(html).short_title()

      self.uploadToS3()

    except Exception, e:
      self.log_error(e)

settings = dict(
  debug=True,
  cookie_secret=utils.COOKIE_SECRET
)

handler_list = [
  ('/', MainHandler),
  ('/add', AddHandler),
  ('/article/(.*)', ArticleHandler),
  ('/read', ReadingListHandler),
  ('/welcome', WelcomeHandler),
  ('/logout', LogoutHandler),

  ('/js/(.*)', web.StaticFileHandler, {'path' : os.path.join(utils.SOURCE_DIR, 'js')}),
  ('/css/(.*)', web.StaticFileHandler, {'path' : os.path.join(utils.SOURCE_DIR, 'css')}),
  ('/img/(.*)', web.StaticFileHandler, {'path' : os.path.join(utils.SOURCE_DIR, 'img')}),

  ('/(.*)', _404Handler)
]

application = web.Application(handler_list, **settings)
start_engine()

if __name__ == "__main__":
  application.listen(8000)
  print 'Running on port 8000'
  ioloop.IOLoop.instance().start()
