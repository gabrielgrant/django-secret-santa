from django.conf.urls.defaults import patterns, include, url

from .views import ChooseView

urlpatterns = patterns('',
	url(r'^$', ChooseView.as_view(), name='secret_santa_choose'),
)
