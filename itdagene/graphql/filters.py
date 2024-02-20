from django_filters import FilterSet, NumberFilter

from itdagene.app.career.models import Joblisting as ItdageneJoblisting


class JoblistingFilter(FilterSet):
    from_year = NumberFilter(field_name="to_year", lookup_expr="gte")
    to_year = NumberFilter(field_name="from_year", lookup_expr="lte")

    class Meta:
        model = ItdageneJoblisting
        fields = [
            "type",
            "company",
            "to_year",
            "from_year",
            "towns",
            "is_summerjob_marathon",
        ]
