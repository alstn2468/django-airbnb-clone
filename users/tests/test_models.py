from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def setUp(self):
        """각각의 테스트 케이스 함수가 실행될 때 실행
        테스트 중 객체의 내용이 변경될 가능성이 있는 경우 사용
        """
        pass

    def test_user_create(self):
        user = User.objects.create_user("test")
        self.assertEqual("test", user.username)

