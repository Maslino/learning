# coding=utf8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning.settings")
# if following two lines omitted, django 1.7 error:
# AppRegistryNotReady: Models aren't loaded yet
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.contrib.auth.models import User
from blog.models import *
from utils.markdown_util import *
