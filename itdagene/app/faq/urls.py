from django.urls import re_path

from itdagene.app.faq.views import list_questions, add_question, edit_question, delete_question

urlpatterns = [
    re_path(r"^$", list_questions, name="itdagene.faq.list_questions"),
    re_path(r"^add/$", add_question, name="itdagene.faq.add_question"),
    re_path(r"^(?P<pk>\d+)/edit/$", edit_question, name="itdagene.faq.edit_question"),
    re_path(r"^(?P<pk>\d+)/delete/$", delete_question, name="itdagene.faq.delete_question"),
]
