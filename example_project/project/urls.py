from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('secret_santa.urls')),
	url(r'^about/', TemplateView.as_view(template_name='about.html')),
	url(r'^contact/', TemplateView.as_view(template_name='contact.html')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
