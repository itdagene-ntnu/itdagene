from typing import Optional

from graphene import Enum, Int, Interface, String
from graphene.relay import Connection


class OpengraphMetadata(Interface):
    title = String(required=True)
    description = String(required=False)
    sharing_image = String(required=False)


class CountableConnectionBase(Connection):
    class Meta:
        abstract = True

    total_count = Int()

    def resolve_total_count(self, info, **kwargs) -> Optional[int]:
        return self.iterable.count()


class OrderByJoblistingType(Enum):
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


class SearchType(Enum):
    COMPANY = "COMPANY"
    COMPANY_WITH_JOBLISTING = "COMPANY_WITH_JOBLISTING"
    TOWNS_WITH_JOBLISTING = "TOWNS_WITH_JOBLISTING"
    JOBLISTING = "JOBLISTING"
    PAGE = "PAGE"

    @property
    def description(self) -> Optional[str]:
        if self != SearchType.COMPANY_WITH_JOBLISTING:
            return None
        return (
            "Search for companies with one or more joblisting. Useful for " "filtering"
        )
