from django.urls import re_path

from itdagene.app.faq.views import list_questions, add, edit

urlpatterns = [
    re_path(r"^$", list_questions, name="itdagene.faq.list_questions"),
    re_path(r"^add/$", add, name="itdagene.faq.add"),
    re_path(r"^(?P<pk>\d+)/edit/$", edit, name="itdagene.faq.edit"),
]
