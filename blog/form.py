# coding=utf8
from django import forms
from video.common import is_url_supported


class QRCodeForm(forms.Form):
    url = forms.URLField(label=u'请输入网址', help_text=u'比如http://curvelearning.net')


class VideoResolveForm(forms.Form):
    url = forms.URLField(label=u'请输入视频网站播放页地址', help_text=u'比如http://www.iqiyi.com/v_19rrnm5guk.html')

    def clean_url(self):
        url = self.cleaned_data['url']
        if not is_url_supported(url):
            raise forms.ValidationError(u'暂不支持该视频地址')
        return url
