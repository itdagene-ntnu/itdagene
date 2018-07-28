from django.test import TestCase
from graphene.test import Client

from itdagene.graphql.schema import schema


class TestSchema(TestCase):
    def test_schema_will_compile(self):
        Client(schema)

    def test_schema_ping(self):
        client = Client(schema)
        executed = client.execute('''{ ping }''')
        assert executed == {'data': {'ping': 'pong'}}
