import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.pages.models import Page as ItdagenePage
from itdagene.core.models import Preference
from itdagene.graphql.filters import JoblistingFilter
from itdagene.graphql.object_types import Joblisting, MetaData, Page, SearchResult
from itdagene.graphql.search import search as _search
from itdagene.graphql.types import SearchType


class Query(graphene.ObjectType):
    node = relay.Node.Field(description="Get node by ID")
    nodes = graphene.List(
        relay.Node, required=True, ids=graphene.List(graphene.NonNull(graphene.ID), required=True),
        description="Get nodes by IDs"
    )
    search = graphene.List(
        SearchResult, required=True, query=graphene.String(),
        types=graphene.List(SearchType, required=True),
        description="Search for different types of objects. Will return max 10 of each type."
    )
    joblistings = DjangoFilterConnectionField(
        Joblisting, filterset_class=JoblistingFilter, max_limit=20, enforce_first_or_last=True,
        description="List and paginate joblistings", on='active_objects'
    )
    current_meta_data = graphene.Field(
        graphene.NonNull(MetaData), description="Metadata about the current years event"
    )

    page = graphene.Field(
        Page, language=graphene.String(default_value="nb"), slug=graphene.NonNull(graphene.String),
        description="Get info page.\n\n Each page identified with" +
        "a slug can be translated into multiple languages. " +
        "Each entity is identified by an id or the unique together pair (slug, language)"
    )

    ping = graphene.String(description="ping -> pong")

    # debug = graphene.Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_ping(self, *args, **kwargs):
        return "pong"

    def resolve_nodes(self, info, ids):
        return [relay.Node.get_node_from_global_id(info, node_id) for node_id in ids]

    def resolve_search(self, info, query, types):
        return _search(query, types)

    def resolve_page(self, info, language, slug):
        return ItdagenePage.objects.filter(language=language, slug=slug).first()

    def resolve_current_meta_data(self, info):
        return Preference.current_preference()
