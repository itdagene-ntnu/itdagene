from django.conf import settings
from graphql import GraphQLError

from itdagene.graphql.loaders import Loaders


class LoaderMiddleware:
    def resolve(self, next, root, info, **args):
        if not hasattr(info.context, 'loaders'):
            info.context.loaders = Loaders()
        return next(root, info, **args)


class ResolveLimitMiddleware:
    def resolve(self, next, root, info, **args):
        if not hasattr(info.context, 'count'):
            info.context.count = 1
        info.context.count = info.context.count + 1
        print(info.__dir__())
        if (info.context.count > settings.GRAPHENE_RESOLVER_LIMIT):
            raise GraphQLError('That email already exists')
        print(info.context.count)
        return next(root, info, **args)
