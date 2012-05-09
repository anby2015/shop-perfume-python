from django.conf.urls import patterns, include, url
from django.contrib import admin
from Shop import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^index/$', views.index),
    url(r'^category/(?P<slug>[-\w]+)/$', views.product_list, name='product_list'),
    url(r'^category/(?P<slug>[-\w]+)/(?P<pIndex>[\d]+)/(?P<pSize>[\d]+)/(?P<orderBy>[-\w]+)/(?P<sortOrder>[-\w]+)/(?P<mode>[-\w]+)/$', views.product_list, name='product_list_paging'),
#    url(r'^product/$', 'object_list',
#         {'queryset' : Product.objects.all()}),
#    url(r'^product/(?P<slug>[-\w]+)/$', 'object_detail',{'queryset' : Product.objects.all()}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url('', views.index, name='index'),
)
