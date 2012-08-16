from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

from apps.leader_board.views import Home, LeaderBoard, Flag, Challenges

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^leader_board/', LeaderBoard.as_view(), name='leader_board'),
    url(r'^challanges/', Challenges.as_view(), name='challanges'),
    url(r'^flag/', Flag.as_view(), name='submit_flag')
)
