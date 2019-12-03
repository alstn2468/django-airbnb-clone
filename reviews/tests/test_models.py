from django.test import TestCase


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running ReviewModelTest

        Fields :
        """
        pass

    def test_review_create_success(self):
        """Review model creation success test
        Check unique field and instance's class name
        """
        pass

    def test_review_create_fail(self):
        """Review model creation failure test
        Duplicate pk index with IntegrityError exception
        """
        pass

    def test_review_get_fields(self):
        """Review model get fields data test
        Check review's all fields except when testing create success test
        """
        pass

    def test_review_str_method(self):
        """Review model str method test
        CHeck str mehtod equal review instance name field
        """
        pass
