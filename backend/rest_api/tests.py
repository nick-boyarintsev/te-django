import unittest

from json import dumps

from django.core.cache import cache
from django.test import Client


class RegistrationTest(unittest.TestCase):
    """Registration REST API unit tests."""

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        self.client = Client()
        self.registration_post_data_201 = [
            {
                'registrationDate': '2010-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "First1",
                    "lastName": "Last1",
                    "email": "test1@test.com",
                }),
            },
            {
                'registrationDate': '2015-02-02T00:00:00.000000+02:00',
                'locale': 'ro',
                'person': dumps({
                    "firstName": "First2",
                    "lastName": "Last2",
                    "email": "test2@test.com",
                }),
            },
            {
                'registrationDate': '2020-03-03T00:00:00.000000+03:00',
                'locale': 'RU',
                'person': dumps({
                    "firstName": "First3",
                    "lastName": "Last3",
                    "email": "test3@test.com",
                }),
            },
        ]
        self.registration_post_data_400 = [
            {},
            {
                'locale': 'en',
                'person': dumps({
                    "firstName": "First",
                    "lastName": "Last",
                    "email": "test@test.com",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'person': dumps({
                    "firstName": "First",
                    "lastName": "Last",
                    "email": "test@test.com",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "lastName": "Last",
                    "email": "test@test.com",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "First",
                    "email": "test@test.com",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "First",
                    "lastName": "Last",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "",
                    "lastName": "Last",
                    "email": "test@test.com",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "First",
                    "lastName": "",
                    "email": "test@test.com",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "First",
                    "lastName": "Last",
                    "email": "failed test",
                }),
            },
            {
                'registrationDate': '2020-01-01T00:00:00.000000+01:00',
                'locale': 'en',
                'person': dumps({
                    "firstName": "",
                    "lastName": "Last",
                    "email": "test@test.com",
                }),
            },
        ]
        self.registration_get_data_200 = [
            '461bb3e0-a02d-493c-8c2e-544a9f776d41',
            '461bb3e0-a02d-493c-8c2e-544a9f776d42',
            '461bb3e0-a02d-493c-8c2e-544a9f776d43',
        ]
        self.registration_get_data_404 = [
            '',
            '461bb3e0-a02d-493c',
            '461bb3e0-a02d-493c-8c2e-544a9f776d43',
        ]

    def setUp(self):
        pass

    def tearDown(self):
        cache.clear()

    def test_registration_post_201(self):
        for data in self.registration_post_data_201:
            response = self.client.post('/api/v1/registrations', dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 201)

    def test_registration_post_400(self):
        for data in self.registration_post_data_400:
            response = self.client.post('/api/v1/registrations', dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_registration_get_200(self):
        body = {
            'registrationDate': '2020-01-01T00:00:00.000000+01:00',
            'locale': 'en',
            'person': dumps({
                "firstName": "",
                "lastName": "Last",
                "email": "test@test.com",
            }),
        }
        for data in self.registration_get_data_200:
            cache.set(data, body, None)
            response = self.client.get('/api/v1/registrations/' + data)
            self.assertEqual(response.status_code, 200)

    def test_registration_get_404(self):
        for data in self.registration_get_data_404:
            response = self.client.get('/api/v1/registrations/' + data)
            self.assertEqual(response.status_code, 404)
