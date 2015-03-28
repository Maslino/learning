# coding=utf8
from django import forms


class QRCodeForm(forms.Form):
    url = forms.URLField(label=u'请输入网址')
