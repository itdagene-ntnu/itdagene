import django_filters
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.app.pages.models import Page as ItdagenePage
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser

from .models import Company, Joblisting, MetaData, Page, User


class JoblistingFilter(django_filters.FilterSet):
    # Do case-insensitive lookups on 'name'
    from_year = django_filters.NumberFilter(field_name="to_year", lookup_expr='gte')
    to_year = django_filters.NumberFilter(field_name="from_year", lookup_expr='lte')

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
    main_collaborator = graphene.Field(
        Company, description="Main collaborator for current years event"
    )

    node = relay.Node.Field()
    nodes = graphene.List(
        relay.Node, required=True, ids=graphene.List(graphene.NonNull(graphene.ID), required=True)
    )

    page = graphene.Field(
        Page, language=graphene.String(default_value="nb"), slug=graphene.NonNull(graphene.String)
    )

    # debug = graphene.Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_nodes(self, info, ids):
        return [relay.Node.get_node_from_global_id(info, node_id) for node_id in ids]

    def resolve_page(self, info, language, slug):
        return ItdagenePage.objects.filter(language=language, slug=slug).first()

    def resolve_main_collaborator(self, info):
        return ItdageneCompany.get_main_collaborator()

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
