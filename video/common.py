# coding=utf8
import re
import urlparse
import requests
from video.site import Site


def get_content(url, headers=None):
    if headers is None:
        headers = {}
    headers['User-Agent'] = \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
    response = requests.get(url, headers=headers, timeout=10)
    return response.text


def match1(text, pattern):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


url_site_mapping = (
    ('iqiyi.com', Site.SITE_IQIYI),
)


def get_site(url):
    parse_result = urlparse.urlparse(url)
    netloc = parse_result.netloc
    for pattern, site in url_site_mapping:
        if pattern in netloc:
            return site
    return None


def is_url_supported(url):
    site = get_site(url)
    return site is not None


if __name__ == "__main__":
    url = 'http://www.iqiyi.com/v_19rrhfjug0.html'
    print get_site(url)
    print is_url_supported(url)
    html = get_content(url)
    print match1(html, r'data-player-tvid="([^"]+)"')
    print match1(html, r'data-player-videoid="([^"]+)"')
