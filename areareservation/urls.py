from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('reservations.views',
    # Examples:
    url(r'^$', 'index'),
    # url(r'^areareservation/', include('areareservation.foo.urls')),
    url(r'^reservations/$', 'index'),
    url(r'^sites/(?P<site_id>.+)/$', 'sitedetails'),
    url(r'^reservations/(?P<reservation_id>\d+)/$', 'detail'),
    url(r'^reservations/new/(?P<site_id>.+)/$', 'newreservation'),
    url(r'^reservations/delete/(?P<reservation_id>.+)/$', 'deletereservation'),
    url(r'^reservations/addcomment/(?P<reservation_id>.+)/$', 'addcomment'),
    url(r'^reservations/setstatus/(?P<reservation_id>.+)/(?P<newstatus>.+)$', 'setstatus'),
    url(r'^reservations/(?P<site_id>.+)/create/$', 'createreservation'),
    url(r'^reservations/personnel/(?P<site_id>.+)/$', 'personnel'),
)
urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
