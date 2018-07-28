import django_filters
import graphene
from django.db.models import Q
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.app.pages.models import Page as ItdagenePage
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser

from .graphql_models import Company, Joblisting, MetaData, Page, User


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


class SearchType(graphene.Enum):
    COMPANY = "COMPANY"
    COMPANY_WITH_JOBLISTING = "COMPANY_WITH_JOBLISTING"
    JOBLISTING = "JOBLISTING"
    PAGE = "PAGE"

    @property
    def description(self):
        if self == SearchType.COMPANY_WITH_JOBLISTING:
            return 'Search for companies with one or more joblisting. Useful for filtering'
        return None


class SearchResult(graphene.Union):
    class Meta:
        types = (Joblisting, Company, Page)


class Query(graphene.ObjectType):
    joblistings = DjangoFilterConnectionField(
        Joblisting, filterset_class=JoblistingFilter, max_limit=20, enforce_first_or_last=True
    )
    current_meta_data = graphene.Field(
        graphene.NonNull(MetaData), description="Metadata about the current years event"
    )

    node = relay.Node.Field()
    nodes = graphene.List(
        relay.Node, required=True, ids=graphene.List(graphene.NonNull(graphene.ID), required=True)
    )
    search = graphene.List(
        SearchResult, required=True, query=graphene.String(),
        types=graphene.List(SearchType, required=True),
        description="Search for different types of objects. Will return max 10 of each type."
    )

    page = graphene.Field(
        Page, language=graphene.String(default_value="nb"), slug=graphene.NonNull(graphene.String),
        description="Get info page.\n\n Each page identified with" +
        "a slug can be translated into multiple languages. " +
        "Each entity is identified by an id or the unique together pair (slug, language)"
    )

    ping = graphene.String()

    # debug = graphene.Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_ping(self, *args, **kwargs):
        return "pong"

    def resolve_nodes(self, info, ids):
        return [relay.Node.get_node_from_global_id(info, node_id) for node_id in ids]

    def resolve_search(self, info, query, types):
        result = []
        # TODO move and test these :rip: :rip:
        if SearchType.COMPANY in types:
            result = result + list(Company.get_queryset().filter(name__icontains=query)[:10])

        if SearchType.COMPANY_WITH_JOBLISTING in types:
            result = result + list(
                ItdageneCompany.objects.filter(
                    pk__in=ItdageneJoblisting.objects.values_list('company')
                ).filter(name__icontains=query)[:10]
            )

        if SearchType.PAGE in types:
            result = result + list(
                Page.get_queryset().filter(Q(title__icontains=query)
                                           | Q(content__icontains=query))[:10]
            )

        if SearchType.JOBLISTING in types:
            result = result + list(
                Joblisting.get_queryset()
                .filter(Q(title__icontains=query)
                        | Q(description__icontains=query))[:10]
            )
        return result

    def resolve_page(self, info, language, slug):
        return ItdagenePage.objects.filter(language=language, slug=slug).first()

    def resolve_current_meta_data(self, info):
        return Preference.current_preference()
