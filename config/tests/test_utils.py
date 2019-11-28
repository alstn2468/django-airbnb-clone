from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from config.utils import get_secret
import json


class GetSecretTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        with open("secrets.json") as f:
            secrets = json.loads(f.read())

    def test_get_secret_success(self):
        TEST_DATA = get_secret("TEST_DATA")
        self.assertEqual("TEST", TEST_DATA)

    def test_get_secret_fail(self):
        with self.assertRaises(ImproperlyConfigured):
            NO_KEY = get_secret("NO_KEY")

