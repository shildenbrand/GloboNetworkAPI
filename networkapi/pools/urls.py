# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'networkapi.pools.views',
    url(r'^pools/$', 'pool_list'),
)