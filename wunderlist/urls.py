from django.conf.urls import patterns, url
from wunderlist import views
# Create your views here.
urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^add_Item/$', views.add_Item, name='add_Item'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<page_name_slug>[\w\-]+)/$', views.page, name='page'),
        url(r'^edit/(?P<person_id>[\w\-]+)/$', views.test, name='edit'),
        url(r'^search/$', views.search, name='search'),
        )
