from django.conf import settings
from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView


class DocumentationContextTemplateView(TemplateView):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(DocumentationContextTemplateView,
                        self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


urlpatterns = patterns('itdagene.app.documentation',
                       url(r'^$', DocumentationContextTemplateView.as_view(
                           template_name='documentation/overview.html',
                           extra_context={
                               "title": _('Overview'),
                               'description': settings.SITE['project_name']
                           }),
                           name='overview'), )
