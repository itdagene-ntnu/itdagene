from django.template import Library

from itdagene.app.company.forms import CompanyPackageForm


register = Library()


@register.inclusion_tag("company/templatetags/package_form.html")
def package_form(company) -> dict:
    form = CompanyPackageForm(instance=company)
    return {"form": form}
