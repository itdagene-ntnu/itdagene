from django_filters import FilterSet, NumberFilter

from itdagene.app.career.models import Joblisting as ItdageneJoblisting


class JoblistingFilter(FilterSet):
    from_grade = NumberFilter(field_name="to_grade", lookup_expr="gte")
    to_grade = NumberFilter(field_name="from_grade", lookup_expr="lte")

    class Meta:
        model = ItdageneJoblisting
        fields = [
            "type",
            "company",
            "to_grade",
            "from_grade",
            "towns",
            "is_summerjob_marathon",
        ]
