from django.conf.urls import patterns, include, url
from django.contrib import admin
from Shop import views, cart_views

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
    url(r'^tags/$', views.tags),
    url(r'^tag/(?P<tag>[-_A-Za-z0-9]+)/$',views.with_tag, name='tag_list'),
    url(r'^tag/(?P<tag>[-_A-Za-z0-9]+)/(?P<pIndex>[\d]+)/(?P<pSize>[\d]+)/(?P<orderBy>[-\w]+)/(?P<sortOrder>[-\w]+)/(?P<mode>[-\w]+)/$', views.with_tag, name='tag_list_detail'),
    url(r'^cart/add/(?P<slug>[-\w]+)/(?P<product_id>[\d]+)/$', cart_views.cart_add, name='add_cart'),
    url(r'^cart/checkout/$', cart_views.shopping_cart, name='cart_shopping_cart'),
    url('', views.index, name='index'),
)
