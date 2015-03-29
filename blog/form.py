# coding=utf8
from django import forms
from video.common import is_url_supported


class QRCodeForm(forms.Form):
    url = forms.URLField(label=u'请输入网址')


class VideoResolveForm(forms.Form):
    url = forms.URLField(label=u'请输入视频网站播放页地址')

    def clean_url(self):
        url = self.cleaned_data['url']
        if not is_url_supported(url):
            raise forms.ValidationError(u'暂不支持该视频地址')
        return url
