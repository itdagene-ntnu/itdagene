from typing import List

from django.db.models import Q

from itdagene.app.career.models import Joblisting as ItdageneJoblisting
from itdagene.app.career.models import Town
from itdagene.app.company.models import Company as ItdageneCompany
from itdagene.graphql.object_types import Company, Page
from itdagene.graphql.types import SearchType


MAX_COUNT = 10


def search(query: str, types: List[str]) -> list:
    result = []

    alternatives = (
        (SearchType.COMPANY, query_companies),
        (SearchType.JOBLISTING, query_joblistings),
        (SearchType.COMPANY_WITH_JOBLISTING, query_companies_with_joblisting),
        (SearchType.TOWNS_WITH_JOBLISTING, query_towns_with_joblisting),
        (SearchType.PAGE, query_pages),
    )

    for type_, query_func in alternatives:
        if type_ not in types:
            continue

        result.extend(list(query_func(query, MAX_COUNT)))

    return result


def query_companies_with_joblisting(query: str, count: int):
    return ItdageneCompany.objects.filter(
        pk__in=ItdageneJoblisting.active_objects.values_list("company")
    ).filter(name__icontains=query)[:count]


def query_towns_with_joblisting(query: str, count: int):
    return Town.objects.filter(
        pk__in=ItdageneJoblisting.active_objects.values_list("towns")
    ).filter(name__icontains=query)[:count]


def query_companies(query: str, count: int):
    return Company.get_queryset().filter(name__icontains=query)[:count]


def query_pages(query: str, count: int):
    return Page.get_queryset().filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    )[:count]


def query_joblistings(query: str, count: int):
    return ItdageneJoblisting.active_objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )[:count]
