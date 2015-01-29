from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from blog.models import *
from utils.markdown_util import MarkdownUtil


def index(request):
    posts = Post.objects.all()
    return render_to_response('index.html', locals())


def post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        md_content = MarkdownUtil.convert(post.content)
    except ObjectDoesNotExist:
        raise Http404
    return render_to_response('post.html', locals())
