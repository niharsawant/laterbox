
import os
import traceback
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('config.cfg', 'r'))

SOURCE_DIR = os.path.join(os.environ['HOME'], config.get('ENV', 'src_dir'))
AWS_ACESS_KEY = config.get('KEYS', 'aws')
AWS_SECRET = config.get('SECRETS', 'aws')
COOKIE_SECRET = config.get('SECRETS', 'cookie')
AWS_ARTICLE_DIR = config.get('S3', 'article_dir')
BUCKET_NAME = config.get('S3', 'bucket_name')
DATETIME_FORMAT = '%m/%d/%Y %H:%M:%S'

def log_error():
  type_, value_, traceback_ = sys.exc_info()
  ex = traceback.format_exception(type_, value_, traceback_)
  for line in ex:
    print line

class AppException(Exception):
  def __init__(self, message):
    self.message = message
