import graphene
from django.conf import settings
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser


class Joblisting(DjangoObjectType):
    class Meta:
        model = ItdageneJoblisting
        description = "Joblisting entity"
        only_fields = (
            'id',
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
            'date_saved',
        )
        interfaces = (relay.Node, )


class User(DjangoObjectType):
    full_name = graphene.String()
    role = graphene.String()

    class Meta:
        model = ItdageneUser
        interfaces = (relay.Node, )
        description = "User entity"
        only_fields = ('id', 'firstName', 'lastName', 'email', 'photo', 'year', 'role')

    def resolve_full_name(self, info):
        return self.get_full_name()

    def resolve_role(self, info):
        return self.role()


class Company(DjangoObjectType):
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


class MetaData(DjangoObjectType):
    class Meta:
        model = Preference
        description = "Metadata about the current years itdagene"
        only_fields = (
            'id',
            'start_date',
            'end_date',
            'year',
            'nr_of_stands',
        )
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    board_members = graphene.NonNull(graphene.List(graphene.NonNull(User)))
    current_meta_data = graphene.Field(graphene.NonNull(MetaData))

    companies_first_day = graphene.NonNull(graphene.List(graphene.NonNull(Company)))
    companies_last_day = graphene.NonNull(graphene.List(graphene.NonNull(Company)))

    joblisting = relay.Node.Field(Joblisting)
    company = relay.Node.Field(Company)
    debug = graphene.Field(DjangoDebug, name='__debug') if settings.DEBUG else None

    def resolve_board_members(self, info):
        year = Preference.current_preference().year
        return ItdageneUser.objects.filter(year=year).all()

    def resolve_current_meta_data(self, info):
        return Preference.current_preference()

    def resolve_companies_first_day(self, info):
        return ItdageneCompany.get_first_day()

    def resolve_companies_last_day(self, info):
        return ItdageneCompany.get_last_day()


schema = graphene.Schema(query=Query)
