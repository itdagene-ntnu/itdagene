from datetime import date, datetime
from random import shuffle
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.shortcuts import render as django_render
from django.template import loader
from django.template.context import RequestContext, Context
from django.utils import translation
from itdagene.app.career.models import Joblisting
from itdagene.app.company.models import Company, Package
from itdagene.app.events.models import Event
from itdagene.app.feedback.models import Issue
from itdagene.app.meetings.models import Meeting
from itdagene.app.news.models import Announcement
from itdagene.app.pages.models import Page
from itdagene.app.venue.models import Stand
from itdagene.core.models import Preference
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.core.mail import send_mail
from itdagene.core.profiles.models import Profile


def render(request, template, values={}, error=None, info=None, public=False, *args, **kwargs):
    """
    a shortcut that adds the blocks that appear on every page and then calls render_to_response
    it also force public template on not-board-users
    """
    return django_render(request, template, values)

def send_language_specific_mail(subject, user_list, template, context={},
                                connection=None):
    for recipient in user_list:
        translation.activate(recipient.profile.language)
        t = loader.get_template(template)
        c = Context(context)
        msg = EmailMessage(subject=_(subject),
            body=t.render(c),
            from_email=settings.FROM_ADDRESS,
            to=(recipient.email,),
            connection=connection
        )
        msg.content_subtype = "html"
        msg.send()


def add_message(self, request, message, message_class='info'):
    #request.session['message'] = {'class': message_class, 'value': message}
    pass


class Frontpage:
    @classmethod
    def internal_menu(cls, u):
        return [
                {'title': _('Home'),
                 'url': reverse('frontpage'),
                 'icon': 'asterisk_orange',
                 'visible': True},

                {'title': _('Pages'),
                 'url': reverse('pages'),
                 'icon': 'page_gear',
                 'children': 'pages/submenu.html',
                 'visible': u.has_permission(u, 'VIEW', Page)},

                {'title': _('Add announcement'),
                 'url': reverse('create_announcement'),
                 'icon': 'page_gear',
                 'children': None,
                 'visible': u.has_permission(u, 'CREATE', Announcement)},

                {'title': _('Companies'),
                 'url': reverse('companies'),
                 'icon': 'factory',
                 'children': 'company/submenu.html',
                 'visible': u.has_permission('VIEW', Company)},

                {'title': _('Packages'),
                 'url': reverse('packages'),
                 'icon': 'package',
                 'children': 'company/packages/submenu.html',
                 'visible': u.has_permission('VIEW', Package)},

                {'title': _('Venue'),
                 'url': reverse('venue'),
                 'icon': 'map',
                 'children': None,
                 'visible': u.has_permission('VIEW', Stand)},

                {'title': _('Joblistings'),
                 'url': reverse('joblistings'),
                 'icon': 'calendar_copy',
                 'children': 'career/submenu.html',
                 'visible': u.has_permission('VIEW', Joblisting)},


                {'title': _('Events'),
                 'url': reverse('events'),
                 'icon': 'events',
                 'children': 'events/submenu.html',
                 'visible': u.has_permission('VIEW', Event)},

                {'title': _('Meetings'),
                 'url': reverse('meetings'),
                 'icon': 'calendar_view_day',
                 'children': 'meetings/submenu.html',
                 'visible': u.has_permission('VIEW', Meeting)},

                {'title': _('Issues'),
                 'url': reverse('issues'),
                 'icon': 'file_manager',
                 'children': 'feedback/submenu.html',
                 'visible': u.has_permission('VIEW', Issue)},

                {'title': _('People'),
                 'url': reverse('profiles'),
                 'icon': 'user_red',
                 'children': 'core/profiles/submenu.html',
                 'visible': u.has_perm('profiles')},

                {'title': _('Admin'),
                 'url': reverse('admin'),
                 'icon': 'administrator',
                 'children': 'adm/submenu.html',
                 'visible': u.is_staff},

                {'title': 'Django admin',
                 'url': '/dadmin/',
                 'icon': 'application_cascade',
                 'visible': u.is_staff},
        ]

    @classmethod
    def public_joblistings(cls):
        joblistings = cache.get('frontpagejoblistings')
        if not joblistings:
            joblistings = list(Joblisting.objects.filter(company__mp=True, deadline__gt=datetime.now()).select_related('company'))
            joblistings += list(Joblisting.objects.filter(company__mp=True, deadline=None).select_related('company'))
            joblistings += list(Joblisting.objects.filter(company__partner=True, deadline__gt=datetime.now()).select_related('company'))
            joblistings += list(Joblisting.objects.filter(company__partner=True, deadline=None).select_related('company'))
            shuffle(joblistings)
            joblistings += list(Joblisting.objects.filter(deadline__gt=date.today(), company__mp=False, company__partner=False).select_related(
                'company').order_by('?'))
            joblistings += list(
                Joblisting.objects.filter(deadline=None, company__mp=False).select_related('company').order_by('?'))
            joblistings = joblistings[:10]
            cache.set('frontpagejoblistings', joblistings, 300)
        return joblistings
