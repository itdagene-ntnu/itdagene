import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.career.models import Town as ItdageneTown
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.app.events.models import Event as ItdageneEvent
from itdagene.app.pages.models import Page as ItdagenePage
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser
from itdagene.graphql.types import CountableConnectionBase, OpengraphMetadata
from itdagene.graphql.utils import resize_image


class Town(DjangoObjectType):
    class Meta:
        model = ItdageneTown
        interfaces = (relay.Node, )
        description = "Town entity"
        only_fields = ('id', 'name')


class Joblisting(DjangoObjectType):
    towns = graphene.NonNull(graphene.List(graphene.NonNull(Town)))

    class Meta:
        model = ItdageneJoblisting
        connection_class = CountableConnectionBase
        #        filter_fields = [
        #            'type',
        #            'to_year',
        #            'from_year',
        #        ]
        description = "Joblisting entity"
        only_fields = (
            'id',
            'towns',
            'company',
            'title',
            'type',
            'description',
            'image',
            'deadline',
            'from_year',
            'to_year',
            'url',
            'date_created',
        )
        interfaces = (relay.Node, OpengraphMetadata)

    def resolve_towns(self, info, **kwargs):
        return self.towns.all()

    def resolve_sharing_image(self, info, **kwargs):
        if not self.company.logo:
            return None
        return resize_image(self.company.logo, width=1200, height=630)

    def resolve_company(self, info, **kwargs):
        return info.context.loaders.Companyloader.load(self.company_id)

    @classmethod
    def get_queryset(cls):
        return ItdageneJoblisting.objects.all()

    @classmethod
    def get_node(cls, context, id):
        try:
            return ItdageneJoblisting.objects.get(pk=id)
        except Exception as e:
            print(e)
            return None


class Page(DjangoObjectType):
    class Meta:
        model = ItdagenePage
        interfaces = (relay.Node, OpengraphMetadata)
        description = "(info)Page entity"
        only_fields = (
            'slug',
            'title',
            'language',
            'menu',
            'content',
            'ingress',
            'date_saved',
            'date_created',
        )

    def resolve_description(self, info, **kwargs):
        return self.ingress

    @classmethod
    def get_queryset(cls):
        return ItdagenePage.objects.filter(need_auth=False)


class User(DjangoObjectType):
    full_name = graphene.String()
    role = graphene.String()
    photo = graphene.Field(graphene.String, height=graphene.Int(), width=graphene.Int())

    class Meta:
        model = ItdageneUser
        interfaces = (relay.Node, )
        description = "User entity"
        only_fields = ('id', 'firstName', 'lastName', 'email', 'year', 'role')

    def resolve_full_name(self, info):
        return self.get_full_name()

    def resolve_role(self, info):
        return self.role()

    def resolve_photo(self, info, **kwargs):
        return resize_image(self.photo, format="JPEG", quality=80, **kwargs)


class Company(DjangoObjectType):
    logo = graphene.Field(graphene.String, height=graphene.Int(), width=graphene.Int())

    class Meta:
        model = ItdageneCompany
        description = "Company entity"
        only_fields = (
            'id',
            'name',
            'url',
            'logo',
            'description',
            'is_collabrator',
            'joblistings',
        )
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls):
        return ItdageneCompany.get_last_day() | ItdageneCompany.get_first_day()

    @classmethod
    def get_node(cls, context, id):
        try:
            return cls.get_queryset().get(pk=id)
        except Exception as e:
            print(e)
            return None

    def resolve_logo(self, info, **kwargs):
        return resize_image(self.logo, **kwargs)


class Event(DjangoObjectType):
    class Meta:
        model = ItdageneEvent
        description = "Small event type"
        only_fields = (
            'id',
            'title',
            'time_start',
            'time_end',
            'description',
            'type',
            'location',
            'company',
            'uses_tickets',
            'max_participants',
            'date',
        )
        interfaces = (relay.Node, )


class MetaData(DjangoObjectType):

    companies_first_day = graphene.List(graphene.NonNull(Company))
    companies_last_day = graphene.List(graphene.NonNull(Company))
    collaborators = graphene.List(
        graphene.NonNull(Company),
        description="List the collaborators, not including the main collaborator"
    )

    main_collaborator = graphene.Field(
        Company, description="Main collaborator for current years event"
    )

    board_members = graphene.NonNull(graphene.List(graphene.NonNull(User)))

    def resolve_main_collaborator(self, info):
        if self.view_hsp:
            return ItdageneCompany.get_main_collaborator()

    def resolve_companies_first_day(self, info):
        if self.view_companies:
            return ItdageneCompany.get_first_day()

    def resolve_companies_last_day(self, info):
        if self.view_companies:
            return ItdageneCompany.get_last_day()

    def resolve_collaborators(self, info):
        if self.view_sp:
            return ItdageneCompany.objects.filter(package__name="Samarbeidspartner")

    def resolve_board_members(self, info):
        return ItdageneUser.objects.filter(year=self.year).all().prefetch_related('groups')

    class Meta:
        model = Preference
        description = "Metadata about the current years itdagene"
        only_fields = (
            'id',
            'start_date',
            'end_date',
            'year',
            'nr_of_stands',
            'companies_first_day'
            'companies_last_day',
            'collaborators',
            'main_collaborator',
            'board_members',
        )
        interfaces = (relay.Node, )


class SearchResult(graphene.Union):
    class Meta:
        types = (Joblisting, Company, Page, Town)