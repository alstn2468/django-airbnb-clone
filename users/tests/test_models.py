from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """클래스 전체에서 사용되는 설정을 위해서 테스트 시작 때 한 번만 실행
        테스트가 실행되면서 수정되거나 변경되지 않을 객체들을 생성
        """
        pass

    def setUp(self):
        """각각의 테스트 케이스 함수가 실행될 때 실행
        테스트 중 객체의 내용이 변경될 가능성이 있는 경우 사용
        """
        pass

