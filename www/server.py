
import os
import urllib

from tornado import ioloop, web, template
from readability.readability import Document
from sqlalchemy.orm import sessionmaker

import model
from model import page

SOURCE_DIR = os.path.join(os.environ['HOME'], 'git/laterbox')
AWS_ACESS_KEY = 'AKIAJO6GMSYEBEBTGFQA'
AWS_SECRET = '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'
BUCKET_NAME = 's3-apparatus'

class MainHandler(web.RequestHandler):
  def get(self):
    file_path = os.path.join(SOURCE_DIR, 'index.html')
    self.write(template.Template(open(file_path).read()).generate())

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
  ('/add', AddHandler)
]

application = web.Application(handler_list, **settings)
model.start_engine()

if __name__ == "__main__":
  application.listen(8000)
  print 'Running on port 8000'
  ioloop.IOLoop.instance().start()
