# -*- coding:utf-8 -*-
import urllib

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from coffin import template
from loginza.conf import settings

register = template.Library()

allowed_providers_def = {
    'google': u'Google Accounts',
    'yandex': u'Yandex',
    'mailruapi': u'Mail.ru API',
    'mailru': u'Mail.ru',
    'vkontakte': u'Вконтакте',
    'facebook': u'Facebook',
    'twitter': u'Twitter',
    'loginza': u'Loginza',
    'myopenid': u'MyOpenID',
    'webmoney': u'WebMoney',
    'rambler': u'Rambler',
    'flickr': u'Flickr',
    'lastfm': u'Last.fm',
    'verisign': u'Verisign',
    'aol': u'AOL',
    'steam': u'Steam',
    'openid': u'OpenID'
}

allowed_providers = {}
for key, value in allowed_providers_def.items():
    allowed_providers[key] = settings.PROVIDER_TITLES.get(key, value)

def _return_path(request, path=None):
    if path is not None and path not in settings.AMNESIA_PATHS:
        request.session['loginza_return_path'] = path
    return request.session.get('loginza_return_path', '/')

def _absolute_url(url):
    return 'http://%s%s' % (Site.objects.get_current().domain, url)

def return_url():
    return urllib.quote(_absolute_url(reverse('loginza.views.return_callback')), '')

def _providers_set(providers):
    providers_set = []

    providers_list = providers if providers else settings.DEFAULT_PROVIDERS_SET
    if providers_list is not None:
        providers = providers_list.split(',')
        for provider in providers:
            if provider in allowed_providers:
                providers_set.append(provider)

    return providers_set

def format_providers(providers, provider):
    params = []

    providers_set = _providers_set(providers)
    if len(providers_set) > 0:
        params.append('providers_set=' + ','.join(providers_set))

    provider = provider if provider else settings.DEFAULT_PROVIDER
    if provider in allowed_providers:
        params.append('provider=' + provider)

    return ('&'.join(params) + '&') if len(params) > 0 else ''

@register.object()
def loginza_iframe(providers="", provider="", lang=""):
    if not lang:
        lang = settings.DEFAULT_LANGUAGE

    return """<script src="http://loginza.ru/js/widget.js" type="text/javascript"></script>
<iframe src="http://loginza.ru/api/widget?overlay=loginza&%(providers)slang=%(lang)s&token_url=%(return-url)s"
style="width:359px;height:300px;" scrolling="no" frameborder="no"></iframe>""" % {
        'return-url': return_url(),
        'lang': lang,
        'providers': format_providers(providers, provider)
    }
