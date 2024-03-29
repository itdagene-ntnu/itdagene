from django.conf import settings
from graphql import GraphQLError

from itdagene.graphql.loaders import Loaders


class LoaderMiddleware:
    def resolve(self, next_, root, info, **args):
        if not hasattr(info.context, "loaders"):
            info.context.loaders = Loaders()
        return next_(root, info, **args)


class ResolveLimitMiddleware:
    def resolve(self, next_, root, info, **args):
        if not hasattr(info.context, "count"):
            info.context.count = 1  # ? Should be 0?
        info.context.count += 1
        if info.context.count > settings.GRAPHENE_RESOLVER_LIMIT:
            raise GraphQLError("query too big :/")
        return next_(root, info, **args)
