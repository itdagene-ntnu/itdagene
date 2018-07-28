from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from graphene.test import Client
from graphql_relay import to_global_id

from itdagene.app.career.models import Joblisting
from itdagene.app.company.models import Company
from itdagene.core.models import User
from itdagene.graphql.schema import schema


class TestJoblistings(TestCase):
    def setUp(self):
        User.objects.create(is_superuser=True)
        self.company = Company.objects.create()
        self.client = Client(schema)
        self.joblistings_query = '''
        {
          joblistings(first:10){
            edges {
              node {
                id
              }
            }
          }
        }
        '''
        self.node_query = '''
        query ($id: ID!) {
          node(id: $id){
            __typename
            id
          }
        }
        '''
        self.search_query = '''
        query ($query: String!) {
          search(query: $query, types: [JOBLISTING]){
            __typename
            ... on Joblisting {
              id
            }
          }
        }
        '''

    def test_no_joblisting(self):
        executed = self.client.execute(self.joblistings_query)
        self.assertIsNone(executed.get('error'))
        self.assertEqual(executed['data']['joblistings']['edges'], [])

    def test_inactive_joblisting_is_not_in_connection(self):
        Joblisting.objects.create(company=self.company, deadline=timezone.now() - timedelta(days=1))
        executed = self.client.execute(self.joblistings_query)
        self.assertIsNone(executed.get('error'))
        self.assertEqual(executed['data']['joblistings']['edges'], [])

    def test_active_joblisting_is_in_connection(self):
        Joblisting.objects.create(company=self.company, deadline=timezone.now() + timedelta(days=1))
        executed = self.client.execute(self.joblistings_query)
        self.assertIsNone(executed.get('error'))
        self.assertEqual(len(executed['data']['joblistings']['edges']), 1)

    def test_inactive_joblisting_is_node(self):
        """ Ensure old joblisting urls are still valid """
        joblisting = Joblisting.objects.create(
            company=self.company, deadline=timezone.now() - timedelta(days=1)
        )
        global_id = to_global_id("Joblisting", joblisting.pk)
        executed = self.client.execute(self.node_query, variable_values={'id': global_id})

        self.assertIsNone(executed.get('error'))
        self.assertIsNotNone(executed['data']['node'])

        self.assertEqual(executed['data']['node'], {"id": global_id, "__typename": "Joblisting"})

    def test_only_active_is_in_search(self):
        """ Ensure old joblisting urls are still valid """
        title = "Title"
        active = Joblisting.objects.create(
            company=self.company, deadline=timezone.now() + timedelta(days=1), title=title
        )
        Joblisting.objects.create(
            company=self.company, deadline=timezone.now() - timedelta(days=1), title=title
        )
        global_id = to_global_id("Joblisting", active.pk)
        executed = self.client.execute(self.search_query, variable_values={'query': title})

        expected = {
            'data': {
                'search': [{
                    "id": global_id,
                    "__typename": "Joblisting"
                }]
            },
        }

        self.assertIsNone(executed.get('error'))
        self.assertEqual(executed, expected)
