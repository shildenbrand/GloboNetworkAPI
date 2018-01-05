# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf.urls import patterns, url
from networkapi.api_tests import views as tests_views
from networkapi.api_tests import facade as tests_facade


urlpatterns = patterns('',
    url(r'^tests/authentication/$', tests_views.AuthenticationTestView.as_view()),
    url(r'^tests/cache/$', tests_views.CacheTestView.as_view()),
    url(r'^tests/db/$', tests_views.CacheTestView.as_view()),
    url(r'^tests/foreman/$', tests_views.ForemanTestView.as_view()),
    url(r'^tests/queue/$', tests_views.CacheTestView.as_view()),

)

