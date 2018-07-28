import graphene
from django.conf import settings
from graphene import Int, relay
from graphene_django import DjangoObjectType
from sorl.thumbnail import get_thumbnail

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.app.pages.models import Page as ItdagenePage
from itdagene.core.models import Preference
from itdagene.core.models import User as ItdageneUser


def resize_image(image, **kwargs):
    if not image:
        return None
    height = kwargs.get('height')
    width = kwargs.get('width')
    if not height and not width:
        return settings.HOST_URL + image.url

    geometry = f'{width}x{height}'
    if width and not height:
        geometry = f'{width}'

    format = kwargs.get('format', "PNG")
    padding = kwargs.get('padding', True)
    quality = kwargs.get('quality', 99)

    return settings.HOST_URL + get_thumbnail(
        image, geometry, format=format, padding=padding, quality=quality, transparency=True,
        padding_color=(255, 255, 255, 0)
    ).url


class Metadata(graphene.Interface):
    title = graphene.String(required=True)
    description = graphene.String(required=False)
    sharing_image = graphene.String(required=False)


# TODO FIX this. Currently not working with filtering... :(
class CountableConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()


class Joblisting(DjangoObjectType):
    towns = graphene.NonNull(graphene.List(graphene.NonNull(graphene.String)))

    class Meta:
        model = ItdageneJoblisting
        # connection_class = CountableConnectionBase
        filter_fields = [
            'type',
            'to_year',
            'from_year',
        ]
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
        interfaces = (relay.Node, Metadata)

    def resolve_towns(self, info, **kwargs):
        return self.towns.all()

    def resolve_sharing_image(self, info, **kwargs):
        if not self.company.logo:
            return None
        return resize_image(self.company.logo, width=1200, height=630)

    @classmethod
    def get_queryset(cls):
        return []

    @classmethod
    def get_node(cls, context, id):
        try:
            return ItdageneJoblisting.all_objects.all().get(pk=id)
        except Exception as e:
            print(e)
            return None


class Page(DjangoObjectType):
    class Meta:
        model = ItdagenePage
        interfaces = (relay.Node, Metadata)
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
