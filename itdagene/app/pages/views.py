from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponsePermanentRedirect
from itdagene.app.pages.forms import PageForm
from itdagene.app.pages.models import Page
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

def view_page (request, lang_code='nb', slug='itdagene'):
    page = cache.get('page' + lang_code + slug)
    if not page:
        try:
            page = Page.objects.get(language=lang_code, slug=slug, active=True)
            cache.set('page' + lang_code + slug, page)
        except(TypeError, Page.DoesNotExist):
            page = get_object_or_404(Page, slug=slug, active=True)
            messages.error = _('The page is not available in your language.')
    if page.need_auth and not request.user.is_authenticated():
        return HttpResponsePermanentRedirect('/accounts/login/?next=/' + page.slug + '/')
    return render(request,'pages/page.html', {'page': page,})

@permission_required('pages.change_page')
def add(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            cache.set('page' + page.language + page.slug, page)
            cache.delete('menu')
            return redirect(reverse('app.pages.views.view_page', args=[page.slug]))
        else:
            return render(request, 'pages/form.html',
                             {'form': form})
    return edit(request, None)

@permission_required('pages.change_page')
def edit (request, slug, lang_code='nb'):
    form = PageForm()
    page = None
    if slug:
        page = get_object_or_404(Page, language=lang_code, slug=slug)
        form = PageForm(instance=page)
        if request.method == 'POST':
            form = PageForm(request.POST, instance=page)
            if form.is_valid():
                form.save()
                cache.set('page' + page.language + page.slug, page)
                cache.delete('menu')
                return redirect(reverse('app.pages.views.view_page',args=[page.slug]))

    return render(request, 'pages/form.html',
                             {'form': form,
                              'page': page})

@permission_required('pages.change_page')
def admin (request):
    pages = Page.objects.all().order_by('menu', 'active')

    return render(request, 'pages/admin.html',
                             {'pages': pages})