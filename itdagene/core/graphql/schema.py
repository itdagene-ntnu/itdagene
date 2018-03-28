import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser


class Joblisting(DjangoObjectType):
    """ Simple joblisting """

    class Meta:
        model = ItdageneJoblisting
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

    @classmethod
    def get_node(cls, context, id):
        try:
            Joblisting.objects.filter(is_active=True).get(pk=id)
        except Exception:
            return None


class User(DjangoObjectType):
    class Meta:
        model = ItdageneUser
        interfaces = (relay.Node, )


class Company(DjangoObjectType):
    class Meta:
        model = ItdageneCompany
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
    def get_node(cls, context, id):
        queryset = ItdageneCompany.get_last_day() | ItdageneCompany.get_first_day()
        try:
            return queryset.get(pk=id)
        except Exception:
            return None

    def resolve_joblistings(self, info):
        return self.joblistings.filter(is_active=True)


class MetaData(DjangoObjectType):
    class Meta:
        model = Preference
        only_fields = (
            'id',
            'start_date',
            'end_date',
            'year',
            'nr_of_stands',
        )
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    # board_members = graphene.List(User)
    current_meta_data = graphene.Field(graphene.NonNull(MetaData))

    companies_first_day = graphene.NonNull(graphene.List(graphene.NonNull(Company)))
    companies_last_day = graphene.NonNull(graphene.List(graphene.NonNull(Company)))
    company = relay.Node.Field(Company)

    joblistings = relay.Node.Field(Joblisting)

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
