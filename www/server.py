
import os
import urllib

from tornado import ioloop, web, template
from readability.readability import Document

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
    print 'uploaded'

  def uploadToS3(self, title, body):
    import hashlib
    import base64
    from libs.asyncs3 import AWSAuthConnection

    body = body.encode('ascii', 'ignore')
    aws = AWSAuthConnection(AWS_ACESS_KEY, AWS_SECRET, is_secure=False)
    article_dir = base64.b64encode(hashlib.md5(body).digest())+'/'

    aws.put(BUCKET_NAME, article_dir+title, body,
      {'Content-Type' : 'text/html', 'x-amz-acl' : 'public-read'},
      callback=self.s3_callback
    )

  def post(self):
    url = self.get_argument('url', None)
    html = urllib.urlopen(url).read()
    readable_article = Document(html).summary()
    readable_title = Document(html).short_title()

    self.uploadToS3(readable_title, readable_article)

    self.redirect('/')

settings = dict(
  debug=True
)

handler_list = [
  ('/', MainHandler),
  ('/add', AddHandler)
]

application = web.Application(handler_list, **settings)

if __name__ == "__main__":
  application.listen(8000)
  print 'Running on port 8000'
  ioloop.IOLoop.instance().start()
