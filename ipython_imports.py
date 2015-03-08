# coding=utf8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning.settings")

from django.contrib.auth.models import User
from blog.models import *
from utils.markdown_util import *
