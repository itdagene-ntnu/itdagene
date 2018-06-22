import django_filters
import graphene
from django.conf import settings
from graphene import relay
from graphene_django.debug import DjangoDebug
from graphene_django.filter import DjangoFilterConnectionField

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser

from .models import Company, Joblisting, MetaData, User


class JoblistingFilter(django_filters.FilterSet):
    class Meta:
        model = ItdageneJoblisting
        fields = [
            'type',
            'company',
            'to_year',
            'from_year',
        ]


class Query(graphene.ObjectType):
    board_members = graphene.NonNull(graphene.List(graphene.NonNull(User)))
    joblistings = DjangoFilterConnectionField(
        Joblisting, filterset_class=JoblistingFilter, max_limit=20, enforce_first_or_last=True
    )
    current_meta_data = graphene.Field(
        graphene.NonNull(MetaData), description="Metadata about the current years event"
    )

    companies_first_day = graphene.NonNull(graphene.List(graphene.NonNull(Company)))
    companies_last_day = graphene.NonNull(graphene.List(graphene.NonNull(Company)))
    collaborators = graphene.NonNull(
        graphene.List(graphene.NonNull(Company)),
        description="List the collaborators, not including the main collaborator"
    )

    node = relay.Node.Field()
    nodes = graphene.List(
        relay.Node, required=True, ids=graphene.List(graphene.NonNull(graphene.ID), required=True)
    )

    # debug = graphene.Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_nodes(self, info, ids):
        return [relay.Node.get_node_from_global_id(info, node_id) for node_id in ids]

    def resolve_board_members(self, info):
        year = Preference.current_preference().year
        return ItdageneUser.objects.filter(year=year).all()

    def resolve_current_meta_data(self, info):
        return Preference.current_preference()

    def resolve_companies_first_day(self, info):
        return ItdageneCompany.get_first_day()

    def resolve_companies_last_day(self, info):
        return ItdageneCompany.get_last_day()

    def resolve_collaborators(self, info):
        return ItdageneCompany.objects.filter(package__name="Samarbeidspartner")
