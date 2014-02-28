from django.conf.urls import patterns, url

from ..views import ProfileList

urlpatterns = patterns(
    '',
    url(
        regex='^$',
        view=ProfileList.as_view(),
        name='list'
    ),
    url(
        regex='^(?P<pk>\d+)/$',
        view='itdagene.core.profiles.views.profile_detail',
        name='detail'
    )
)