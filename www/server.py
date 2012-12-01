
import os
import urllib

from tornado import ioloop, web, template
from readability.readability import Document


SOURCE_DIR = os.path.join(os.environ['HOME'], 'git/laterbox')

class MainHandler(web.RequestHandler):
  def get(self):
    file_path = os.path.join(SOURCE_DIR, 'index.html')
    self.write(template.Template(open(file_path).read()).generate())

class AddHandler(web.RequestHandler):
  def post(self):
    url = self.get_argument('url', None)
    html = urllib.urlopen(url).read()
    readable_article = Document(html).summary()
    readable_title = Document(html).short_title()

    self.write(readable_title + readable_article)

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
