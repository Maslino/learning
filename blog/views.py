from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from blog.models import *
from utils.markdown_util import MarkdownUtil


def post_index(request):
    posts = Post.objects.order_by('-created')
    quote = Quote.random_get()
    return render_to_response('post_index.html', locals())


def post(request, slug):
    print slug
    try:
        current_post = Post.objects.get(slug=slug)
        next_post = current_post.next_post
        prev_post = current_post.prev_post
        md = MarkdownUtil(current_post.content)
    except ObjectDoesNotExist as e:
        print e
        raise Http404
    return render_to_response('post.html', locals())


def tag(request, slug):
    try:
        current_tag = Tag.objects.get(slug=slug)
        posts = current_tag.related_posts
    except ObjectDoesNotExist as e:
        print e
        raise Http404
    return render_to_response('tag.html', locals())


def tag_index(request):
    tags = Tag.objects.order_by('-created')
    return render_to_response('tag_index.html', locals())
