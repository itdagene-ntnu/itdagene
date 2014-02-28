from django.conf.urls import patterns, url

from ..views import ProfileList

urlpatterns = patterns(
    '',
    url(
        regex='^$',
        view=ProfileList.as_view(),
        name='list'
    )
)