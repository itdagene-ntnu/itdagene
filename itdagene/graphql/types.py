import graphene
from graphene import Int, relay


class Metadata(graphene.Interface):
    title = graphene.String(required=True)
    description = graphene.String(required=False)
    sharing_image = graphene.String(required=False)


class CountableConnectionBase(relay.Connection):
    class Meta:
        abstract = True

    total_count = Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()


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
