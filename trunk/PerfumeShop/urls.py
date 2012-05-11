from django.conf.urls import patterns, include, url
from django.contrib import admin
from Shop import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^index/$', views.index),
    url(r'^category/(?P<slug>[-\w]+)/$', views.product_list, name='product_list'),
    url(r'^category/(?P<slug>[-\w]+)/(?P<pIndex>[\d]+)/(?P<pSize>[\d]+)/(?P<orderBy>[-\w]+)/(?P<sortOrder>[-\w]+)/(?P<mode>[-\w]+)/$', views.product_list, name='product_list_detail'),
    url(r'^product/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^search/result/$', views.search_result, name='search_result'),
    url(r'^search/result/(?P<pIndex>[\d]+)/(?P<pSize>[\d]+)/(?P<orderBy>[-\w]+)/(?P<sortOrder>[-\w]+)/(?P<mode>[-\w]+)/$', views.search_result, name='search_result_detail'),
    url('', views.index, name='index'),
)
