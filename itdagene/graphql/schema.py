import graphene

from itdagene.graphql.query import Query

schema = graphene.Schema(query=Query)
