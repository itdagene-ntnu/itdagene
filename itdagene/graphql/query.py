import graphene
from django.utils.timezone import now
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from itdagene.core.models import Preference
from itdagene.graphql.filters import JoblistingFilter
from itdagene.graphql.object_types import (
    Event,
    Joblisting,
    MetaData,
    Page,
    SearchResult,
    Stand,
)
from itdagene.graphql.search import search as _search
from itdagene.graphql.types import OrderByJoblistingType, SearchType


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        max_limit,
        enforce_first_or_last,
        filterset_class,
        filtering_args,
        root,
        info,
        **args
    ):
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = filterset_class(
            data=filter_kwargs,
            queryset=default_manager.get_queryset(),
            request=info.context,
        ).qs
        order = args.get("orderBy", None)
        if order:
            qs = qs.order_by(*order)
        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver,
            connection,
            qs,
            max_limit,
            enforce_first_or_last,
            root,
            info,
            **args
        )


class Query(graphene.ObjectType):
    node = relay.Node.Field(description="Get node by ID")
    nodes = graphene.List(
        relay.Node,
        required=True,
        ids=graphene.List(graphene.NonNull(graphene.ID), required=True),
        description="Get nodes by IDs",
    )
    search = graphene.List(
        SearchResult,
        required=True,
        query=graphene.String(),
        types=graphene.List(SearchType, required=True),
        description="Search for different types of objects. Will return max 10 of each type.",
    )
    joblisting = graphene.Field(
        Joblisting,
        slug=graphene.NonNull(graphene.String),
        description="Get a joblisting by its slug.",
    )

    joblistings = OrderedDjangoFilterConnectionField(
        Joblisting,
        filterset_class=JoblistingFilter,
        orderBy=graphene.List(of_type=OrderByJoblistingType),
        max_limit=100,
        enforce_first_or_last=True,
        description="List and paginate joblistings",
        on="active_objects",
    )
    current_meta_data = graphene.Field(
        graphene.NonNull(MetaData), description="Metadata about the current years event"
    )

    page = graphene.Field(
        Page,
        language=graphene.String(default_value="nb"),
        slug=graphene.NonNull(graphene.String),
        description="Get info page.\n\n Each page identified with"
        + "a slug can be translated into multiple languages. "
        + "Each entity is identified by an id or the unique together pair (slug, language)",
    )
    pages = graphene.List(
        Page,
        language=graphene.String(default_value="nb"),
        slugs=graphene.List(graphene.NonNull(graphene.String), default_value=None),
        infopage=graphene.Boolean(),
        description="Get info page.\n\n Each page identified with "
        + "a slug can be translated into multiple languages. "
        + "Each entity is identified by an id or the unique together pair (slug, language). "
        + "If slugs are left empty, it will return all pages",
    )

    stands = graphene.List(
        graphene.NonNull(Stand),
        shuffle=graphene.Boolean(
            required=False,
            default_value=None,
            description="Randomize the order of the the stands (optional argument)",
        ),
        description="Get all stands",
    )
    stand = graphene.Field(
        Stand,
        slug=graphene.NonNull(graphene.String),
        description="Get a stand by slug.",
    )

    events = graphene.List(graphene.NonNull(Event), description="All the events")
    ping = graphene.String(description="ping -> pong")
    resolve_count = graphene.Int(description="Resovle count")

    # debug = graphene.Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_ping(self, *args, **kwargs):
        return "pong"

    def resolve_nodes(self, info, ids):
        return [relay.Node.get_node_from_global_id(info, node_id) for node_id in ids]

    def resolve_search(self, info, query, types):
        return _search(query, types)

    def resolve_joblisting(self, info, slug):
        return Joblisting.get_queryset().get(slug=slug)

    def resolve_page(self, info, language, slug):
        return Page.get_queryset().get(language=language, slug=slug)

    def resolve_pages(self, info, language, slugs=None, infopage=None):
        if slugs is None:
            if infopage is None:
                return list(Page.get_queryset().filter(language=language))
            return list(
                Page.get_queryset().filter(language=language, is_infopage=infopage)
            )
        return list(Page.get_queryset().filter(language=language, slug__in=slugs))

    def resolve_current_meta_data(self, info):
        return Preference.current_preference()

    def resolve_resolve_count(self, info, **kwargs):
        return info.context.count

    def resolve_events(self, info):
        return Event.get_queryset().filter(date__year=now().year, is_internal=False)

    def resolve_stand(self, info, slug):
        return Stand.get_queryset().get(slug=slug)

    def resolve_stands(self, info, shuffle=False):
        if shuffle:
            return Stand.get_queryset().order_by("?")
        return Stand.get_queryset()
