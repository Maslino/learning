# coding=utf8
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from utils.hash_util import sha1_hex


def verify(request):
    try:
        signature = request.GET['signature']
        timestamp = request.GET['timestamp']
        nonce = request.GET['nonce']
        echostr = request.GET['echostr']
    except Exception as e:
        print e
        return HttpResponseBadRequest()

    token = 'moZcWO98RglCF6V4UbPxbykQ9kDoh9da'
    s = sha1_hex(''.join(sorted([token, timestamp, nonce])))
    if s == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponseForbidden()
