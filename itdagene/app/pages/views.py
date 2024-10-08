from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.pages.forms import PageForm
from itdagene.app.pages.models import Page
from itdagene.core.decorators import staff_required


def view_page(request, lang_code="nb", slug="itdagene"):
    page = cache.get("page" + lang_code + slug)
    if not page:
        try:
            page = Page.objects.get(language=lang_code, slug=slug, active=True)
            cache.set("page" + lang_code + slug, page)
        except (TypeError, Page.DoesNotExist):
            page = get_object_or_404(Page, slug=slug, active=True)
            messages.error = _("The page is not available in your language.")
    if page.need_auth and not request.user.is_authenticated:
        return f"{reverse('itdagene.login')}?next=/{page.slug}/"
    return render(request, "pages/page.html", {"page": page})


@permission_required("pages.add_page")
def add(request):
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            cache.set("page" + page.language + page.slug, page)
            cache.delete("menu")
            return redirect(reverse("itdagene.pages.admin"))
        else:
            return render(request, "pages/form.html", {"form": form})
    form = PageForm()
    return render(request, "pages/form.html", {"form": form, "title": _("Add Page")})


@permission_required("pages.change_page")
def edit(request, slug, lang_code="nb"):
    form = PageForm()
    page = None
    if slug:
        page = get_object_or_404(Page, language=lang_code, slug=slug)
        form = PageForm(instance=page)
        if request.method == "POST":
            form = PageForm(request.POST, instance=page)
            if form.is_valid():
                form.save()
                cache.set("page" + page.language + page.slug, page)
                cache.delete("menu")
                return redirect(reverse("itdagene.pages.admin"))

    return render(
        request,
        "pages/form.html",
        {
            "form": form,
            "page": page,
            "title": _("Edit Page"),
            "description": page.title,  # type: ignore
        },
    )


@permission_required("pages.delete_page")
def delete(request, slug, lang_code="nb"):
    page = get_object_or_404(Page, language=lang_code, slug=slug)
    if request.method == "POST":
        page.delete()
        add_message(request, SUCCESS, _("Page deleted."))
        return redirect(reverse("itdagene.pages.admin"))
    return render(
        request,
        "pages/delete.html",
        {"page": page, "title": _("Delete Page"), "description": page.title},
    )


@staff_required()
def admin(request):
    pages = Page.objects.all().order_by("menu", "active")
    return render(
        request,
        "pages/admin.html",
        {"pages": pages, "title": _("Pages Admin")},
    )
