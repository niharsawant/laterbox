
import os
import traceback
import sys

SOURCE_DIR = os.path.join(os.environ['HOME'], 'git/laterbox')
AWS_ACESS_KEY = 'AKIAJO6GMSYEBEBTGFQA'
AWS_SECRET = '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'
AWS_ARTICLE_DIR = 'articles/'
BUCKET_NAME = 's3-apparatus'
DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'
COOKIE_SECRET = 'd8f94e3118edd9a54304a07b900bae79868d2033c030d81a60d03ee117b329f7'

def log_error():
  type_, value_, traceback_ = sys.exc_info()
  ex = traceback.format_exception(type_, value_, traceback_)
  for line in ex:
    print line

class AppException(Exception):
  def __init__(self, message):
    self.message = message
