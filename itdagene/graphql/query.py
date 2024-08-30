from typing import Any, Optional

from django.utils.timezone import now
from graphene import ID, Boolean, Field, Int, List, NonNull, ObjectType, String
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField

from itdagene.core.models import Preference
from itdagene.graphql.filters import JoblistingFilter
from itdagene.graphql.object_types import (
    Event,
    Joblisting,
    MetaData,
    Page,
    Photo,
    Question,
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
        max_limit: int,
        enforce_first_or_last: bool,
        filterset_class,
        filtering_args,
        root,
        info,
        **args,
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
            **args,
        )


class Query(ObjectType):
    node = Node.Field(description="Get node by ID")
    nodes = List(
        Node,
        required=True,
        ids=List(NonNull(ID), required=True),
        description="Get nodes by IDs",
    )
    search = List(
        SearchResult,
        required=True,
        query=String(),
        types=List(SearchType, required=True),
        description="Search for different types of objects. Will return max 10 of each type.",
    )
    joblisting = Field(
        Joblisting,
        slug=NonNull(String),
        description="Get a joblisting by its slug.",
    )

    joblistings = OrderedDjangoFilterConnectionField(
        Joblisting,
        filterset_class=JoblistingFilter,
        orderBy=List(of_type=OrderByJoblistingType),
        max_limit=100,
        enforce_first_or_last=True,
        description="List and paginate joblistings",
        on="active_objects",
    )
    current_meta_data = Field(
        NonNull(MetaData), description="Metadata about the current years event"
    )

    page = Field(
        Page,
        language=String(default_value="nb"),
        slug=NonNull(String),
        video_file=String(default_value=None),
        description=(
            "Get info page.\n\n Each page identified with a slug can be "
            "translated into multiple languages. Each entity is identified by "
            "an id or the unique together pair (slug, language)"
        ),
    )
    pages = List(
        Page,
        language=String(default_value="nb"),
        slugs=List(NonNull(String), default_value=None),
        infopage=Boolean(),
        description=(
            "Get info page.\n\n Each page identified with a slug can be "
            "translated into multiple languages. Each entity is identified by "
            "an id or the unique together pair (slug, language). If slugs are "
            "left empty, it will return all pages"
        ),
    )

    questions = List(Question, description="Get all questions")

    photos = List(NonNull(Photo), description="Get all photos")

    stands = List(
        NonNull(Stand),
        shuffle=Boolean(
            required=False,
            default_value=None,
            description="Randomize the order of the the stands (optional argument)",
        ),
        description="Get all stands",
    )
    stand = Field(
        Stand,
        slug=NonNull(String),
        description="Get a stand by slug.",
    )

    events = List(NonNull(Event), description="All the events")
    ping = String(description="ping -> pong")
    resolve_count = Int(description="Resolve count")

    # debug = Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_ping(self, *args, **kwargs) -> str:
        return "pong"

    def resolve_nodes(self, info: str, ids: list) -> list:
        return [Node.get_node_from_global_id(info, node_id) for node_id in ids]

    def resolve_search(self, info: Any, query: str, types: list) -> list:
        return _search(query, types)

    def resolve_joblisting(self, info: Any, slug: str):
        return Joblisting.get_queryset().get(slug=slug)

    def resolve_page(self, info: Any, language: str, slug: str):
        return Page.get_queryset().get(language=language, slug=slug)

    def resolve_pages(
        self,
        info: Any,
        language: str,
        slugs: Optional[list] = None,
        infopage: Optional[bool] = None,
    ) -> list:
        if slugs is None:
            if infopage is None:
                return list(Page.get_queryset().filter(language=language))
            return list(
                Page.get_queryset().filter(language=language, is_infopage=infopage)
            )
        return list(Page.get_queryset().filter(language=language, slug__in=slugs))

    def resolve_questions(self, info: Any) -> list:
        return Question.get_queryset().all()

    def resolve_photos(self, info: Any) -> list:
        return Photo.get_queryset()

    def resolve_current_meta_data(self, info: Any):
        return Preference.current_preference()

    def resolve_resolve_count(self, info, **kwargs):
        return info.context.count

    def resolve_events(self, info: Any):
        return Event.get_queryset().filter(date__year=now().year, is_internal=False)

    def resolve_stand(self, info: Any, slug: str):
        return Stand.get_queryset().get(slug=slug)

    def resolve_stands(self, info: Any, shuffle: bool = False):
        if shuffle:
            return Stand.get_queryset().order_by("?")
        return Stand.get_queryset()
