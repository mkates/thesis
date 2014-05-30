from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thesis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','account.views.signin'),
    url(r'^signin/','account.views.signin'),
    url(r'^logout/','account.views.logout_view'),
    url(r'^loginrequest','account.views.loginrequest'),
    url(r'^accounts/login/', 'account.views.signin'),
    url(r'^visual/', 'visualize.views.visual'),
    url(r'^loadpossession/', 'visualize.views.loadpossession'),
    url(r'^celticplays/', 'playanalyze.views.celticplays'),
    url(r'^possessions/', 'playanalyze.views.possessions'),
    url(r'^run/', 'playanalyze.views.run')
)
