import graphene
from graphene import Int, relay


class OpengraphMetadata(graphene.Interface):
    title = graphene.String(required=True)
    description = graphene.String(required=False)
    sharing_image = graphene.String(required=False)


class CountableConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()


class OrderByJoblistingType(graphene.Enum):
    DEADLINE = "deadline"
    DEADLINE_INVERSE = "-deadline"
    CREATED = "-date_created"
    CREATED_INVERSE = "date_created"
    TYPE = "type"
    TYPE_INVERSE = "-type"
    ID = "pk"
    ID_INVERSE = "-pk"
    COMPANY_NAME = "company__name"
    COMPANY_NAME_INVERSE = "-company__name"


class SearchType(graphene.Enum):
    COMPANY = "COMPANY"
    COMPANY_WITH_JOBLISTING = "COMPANY_WITH_JOBLISTING"
    TOWNS_WITH_JOBLISTING = "TOWNS_WITH_JOBLISTING"
    JOBLISTING = "JOBLISTING"
    PAGE = "PAGE"

    @property
    def description(self):
        if self == SearchType.COMPANY_WITH_JOBLISTING:
            return (
                "Search for companies with one or more joblisting. Useful for filtering"
            )
        return None
