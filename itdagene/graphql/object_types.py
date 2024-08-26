from typing import Any, Optional

from django.db.models import Q
from graphene import Boolean, Field, Int, List, NonNull, String, Union
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.registry import Registry

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.career.models import Town as ItdageneTown
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.app.company.models import KeyInformation as ItdageneKeyInformation
from itdagene.app.events.models import Event as ItdageneEvent
from itdagene.app.faq.models import Question as ItdageneQuestion
from itdagene.app.pages.models import Page as ItdagenePage
from itdagene.app.stands.models import DigitalStand as ItdageneStand
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser
from itdagene.graphql.types import CountableConnectionBase, OpengraphMetadata
from itdagene.graphql.utils import resize_image


class Town(DjangoObjectType):
    class Meta:
        model = ItdageneTown
        interfaces = (Node,)
        description = "Town entity"
        only_fields = ("id", "name")


class Joblisting(DjangoObjectType):
    towns = NonNull(List(NonNull(Town)))

    class Meta:
        model = ItdageneJoblisting
        connection_class = CountableConnectionBase
        # filter_fields = [
        #     'type',
        #     'to_year',
        #     'from_year',
        # ]
        description = "Joblisting entity"
        only_fields = (
            "id",
            "towns",
            "company",
            "title",
            "type",
            "description",
            "image",
            "deadline",
            "from_year",
            "to_year",
            "url",
            "date_created",
            "slug",
            "video_url",
            "is_summerjob_marathon",
            "is_active",
        )
        interfaces = (Node, OpengraphMetadata)

    def resolve_towns(self, info: Any, **kwargs) -> list:
        return self.towns.all()

    def resolve_sharing_image(self, info: Any, **kwargs) -> Optional[str]:
        if self.company.logo:
            return resize_image(self.company.logo, width=1200, height=630)
        return None

    def resolve_company(self, info, **kwargs):
        return info.context.loaders.Companyloader.load(self.company_id)

    @classmethod
    def get_queryset(cls):
        return ItdageneJoblisting.objects.all()

    @classmethod
    def get_node(cls, context: Any, id: Any):
        try:
            return ItdageneJoblisting.objects.get(pk=id)
        except Exception:
            pass


class Page(DjangoObjectType):
    class Meta:
        model = ItdagenePage
        interfaces = (Node, OpengraphMetadata)
        description = "(info)Page entity"
        only_fields = (
            "slug",
            "title",
            "language",
            "video_file",
            "menu",
            "content",
            "ingress",
            "date_saved",
            "date_created",
        )

    def resolve_description(self, info: Any, **kwargs):
        return self.ingress

    @classmethod
    def get_queryset(cls):
        return ItdagenePage.objects.filter(need_auth=False, active=True)


class User(DjangoObjectType):
    full_name = String()
    role = String()
    linkedin = String()
    photo = Field(String, height=Int(), width=Int())

    class Meta:
        model = ItdageneUser
        interfaces = (Node,)
        description = "User entity"
        only_fields = (
            "id",
            "firstName",
            "lastName",
            "email",
            "year",
            "role",
            "linkedin",
        )

    def resolve_full_name(self, info: Any) -> Optional[str]:
        return self.get_full_name()

    def resolve_role(self, info: Any) -> Optional[str]:
        return self.role()

    def resolve_photo(self, info: Any, **kwargs) -> Optional[str]:
        return resize_image(self.photo, format="JPEG", quality=80, **kwargs)


class Event(DjangoObjectType):
    class Meta:
        model = ItdageneEvent
        description = "Small event type"
        only_fields = (
            "id",
            "title",
            "time_start",
            "time_end",
            "cover_image",
            "description",
            "type",
            "location",
            "company",
            "uses_tickets",
            "max_participants",
            "date",
        )
        interfaces = (Node,)

    @classmethod
    def get_queryset(cls):
        """When fetching all events, we do not want stand events, unless
        they are of the type 'promoted stand event' (7).
        """
        return ItdageneEvent.objects.filter(Q(stand=None) | Q(type=7))


class Question(DjangoObjectType):
    class Meta:
        model = ItdageneQuestion
        description = "A question for the FAQ"
        only_fields = ("question", "answer")
        interfaces = (Node,)

    @classmethod
    def get_queryset(cls):
        return ItdageneQuestion.objects.all()


class Stand(DjangoObjectType):
    events = List(NonNull(Event), description="The stand's associated events")

    class Meta:
        model = ItdageneStand
        description = "A company stand"
        only_fields = (
            "slug",
            "description",
            "livestream_url",
            "qa_url",
            "chat_url",
            "active",
            "company",
        )
        interfaces = (Node,)

    def resolve_company(self, info, **kwargs):
        return info.context.loaders.Companyloader.load(self.company_id)

    def resolve_events(self, info: Any, **kwargs):
        return ItdageneEvent.objects.filter(stand=self)

    @classmethod
    def get_queryset(cls):
        return ItdageneStand.objects.filter(active=True)


class KeyInformation(DjangoObjectType):
    class Meta:
        model = ItdageneKeyInformation
        interfaces = (Node,)
        description = "Key information about a company"
        only_fields = ("id", "name", "value")


class Company(DjangoObjectType):
    logo = Field(
        String,
        height=Int(),
        width=Int(),
        padding=Boolean(),
    )
    key_information = List(
        NonNull(KeyInformation),
        description="Key information about the company.",
    )

    class Meta:
        model = ItdageneCompany
        description = "Company entity"
        only_fields = (
            "id",
            "name",
            "url",
            "logo",
            "description",
            "is_collabrator",
            "joblistings",
        )
        interfaces = (Node,)

    @classmethod
    def get_queryset(cls):
        return ItdageneCompany.get_last_day() | ItdageneCompany.get_first_day()

    @classmethod
    def get_node(cls, context: Any, id):
        try:
            return cls.get_queryset().get(pk=id)
        except Exception:
            pass

    def resolve_logo(self, info: Any, **kwargs) -> Optional[str]:
        return resize_image(self.logo, **kwargs)

    def resolve_key_information(self, info: Any, **kwargs) -> list:
        return ItdageneKeyInformation.objects.filter(company=self)

    def resolve_stand(self, info: Any, **kwargs):
        return Stand.get_queryset().filter(company=self).first()


class MainCollaborator(Company):
    class Meta:
        model = ItdageneCompany
        description = "Main collaborator company entity"
        only_fields = (
            "id",
            "name",
            "url",
            "logo",
            "description",
            "joblistings",
            "intro",
            "video",
            "poster",
        )
        interfaces = (Node,)
        # This has to be added to avoid GraphQL using this definiton for all company references
        registry = Registry()

    intro = String()
    video = String()
    poster = String()

    def resolve_intro(self, info: Any) -> Optional[str]:
        return Preference.current_preference().hsp_intro

    def resolve_video(self, info: Any) -> Optional[str]:
        return Preference.current_preference().hsp_video

    def resolve_poster(self, info: Any) -> Optional[str]:
        return Preference.current_preference().hsp_poster


class MetaData(DjangoObjectType):
    companies_first_day = List(NonNull(Company))
    companies_last_day = List(NonNull(Company))
    collaborators = List(
        NonNull(Company),
        description="List the collaborators, not including the main collaborator",
    )

    main_collaborator = Field(
        MainCollaborator,
        description="Main collaborator for current years event",
    )

    board_members = NonNull(List(NonNull(User)))
    interest_form = String()

    def resolve_main_collaborator(self, info: Any):
        if self.view_hsp:
            return ItdageneCompany.get_main_collaborator()

    def resolve_companies_first_day(self, info: Any):
        if self.view_companies:
            return ItdageneCompany.get_first_day()

    def resolve_companies_last_day(self, info: Any):
        if self.view_companies:
            return ItdageneCompany.get_last_day()

    def resolve_collaborators(self, info: Any):
        if self.view_sp:
            return ItdageneCompany.get_collaborators()
        return None

    def resolve_board_members(self, info: Any):
        return (
            ItdageneUser.objects.filter(year=self.year, is_active=True)
            .all()
            .prefetch_related("groups")
        )

    def resolve_interest_form(self, info: Any) -> Optional[str]:
        if self.show_interest_form:
            return self.interest_form_url
        return None

    class Meta:
        model = Preference
        description = "Metadata about the current years itdagene"
        only_fields = (
            "id",
            "start_date",
            "end_date",
            "year",
            "nr_of_stands",
            "companies_first_day",
            "companies_last_day",
            "collaborators",
            "main_collaborator",
            "board_members",
            "interest_form",
        )
        interfaces = (Node,)


class SearchResult(Union):
    class Meta:
        types = (Joblisting, Company, Page, Town)
