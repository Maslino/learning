# coding=utf-8
import StringIO
from contextlib import closing
import os
import socket
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import RequestContext
from django.conf import settings
import qrcode
import requests
from blog.models import *
from blog.form import *
from utils.markdown_util import MarkdownUtil
from utils.hash_util import *
from video.iqiyi import get_real_addresses
from video.exceptions import *


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

        links = Link.objects.all()
        tags = Tag.objects.all()

        recent_posts = Post.objects.order_by('-created')[:5]
        hot_posts = Post.objects.order_by('-visited')[:5]
    except ObjectDoesNotExist as e:
        print e
        raise Http404

    current_post.visited += 1
    current_post.save()
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


def leave_message(request):
    return render_to_response('message.html')


def generate_qrcode(request):
    if request.method == "POST":
        form = QRCodeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            img = qrcode.make(url, border=1)
            # save as png
            output = StringIO.StringIO()
            img.save(output, "png")
            content = output.getvalue()
            output.close()
            # save content to disk
            img_name = md5_hex(url) + '.png'
            img_path = os.path.join(settings.QRCODE_ROOT, img_name)
            with closing(open(img_path, 'wb')) as f:
                f.write(content)
            img_url = settings.QRCODE_URL + img_name
    else:
        form = QRCodeForm()
    return render_to_response('tools/qrcode.html', locals(), context_instance=RequestContext(request))


def video_resolve(request):
    if request.method == "POST":
        form = VideoResolveForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                result = get_real_addresses(url)
            except VIPNotSupported as e:
                error = unicode(e)
            except requests.RequestException as e:
                traceback.print_exc()
                error = u'请求视频网站服务器出现异常'
            except Exception as e:
                traceback.print_exc()
                error = u'解析视频地址失败'
    else:
        form = VideoResolveForm()
    return render_to_response('tools/video_resolve.html', locals(), context_instance=RequestContext(request))


def webp_check(request):
    """
    检测浏览器对WebP的支持
    :param request:
    :return:
    """
    return render_to_response('tools/webp_check.html', locals())


def link_index(request):
    links = Link.objects.order_by('-created')
    return render_to_response('links.html', locals())
