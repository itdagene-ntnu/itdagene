from django.test import TestCase
from graphene.test import Client
from itdagene.graphql.schema import schema


class TestSchema(TestCase):
    def test_schema_will_compile(self):
        Client(schema)

    def test_schema_ping(self):
        client = Client(schema)
        executed = client.execute("""{ ping }""")
        self.assertEqual(executed, {"data": {"ping": "pong"}})

    def test_introspection_query(self):
        """ Schama introspection should be successful """
        # source https://github.com/graphql/graphiql/blob/master/src/utility/introspectionQueries.js
        query = """
  query IntrospectionQuery {
    __schema {
      queryType { name }
      mutationType { name }
      subscriptionType { name }
      types {
        ...FullType
      }
      directives {
        name
        description
        locations
        args {
          ...InputValue
        }
      }
    }
  }

  fragment FullType on __Type {
    kind
    name
    description
    fields(includeDeprecated: true) {
      name
      description
      args {
        ...InputValue
      }
      type {
        ...TypeRef
      }
      isDeprecated
      deprecationReason
    }
    inputFields {
      ...InputValue
    }
    interfaces {
      ...TypeRef
    }
    enumValues(includeDeprecated: true) {
      name
      description
      isDeprecated
      deprecationReason
    }
    possibleTypes {
      ...TypeRef
    }
  }

  fragment InputValue on __InputValue {
    name
    description
    type { ...TypeRef }
    defaultValue
  }

  fragment TypeRef on __Type {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
  }
"""
        client = Client(schema)
        executed = client.execute(query)
        self.assertIsNone(executed.get("errors"))
        self.assertIsNotNone(executed["data"])
