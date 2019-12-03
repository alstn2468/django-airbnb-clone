from django.test import TestCase
from django.db import IntegrityError
from conversations.models import Conversation, Message
from users.models import User
from datetime import datetime
from unittest import mock
import pytz


class ConversationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running ConversationModelTest

        Fields:
            id           : 1
            participants : <User [test_user_1, test_user_2, ... test_user_10]>
            created_at   : 2019.11.30.00.00.00
            updated_at   : 2019.12.01.00.00.00
        """
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Conversation.objects.create()

    def test_conversation_create_success(self):
        """Conversation model creation success test
        Check instance's class name
        """
        conversation = Conversation.objects.get(id=1)
        self.assertEqual("Conversation", conversation.__class__.__name__)

    def test_conversation_participants_blank(self):
        """Conversation model rooms field blank test
        Check conversation's participants field exists return False
        """
        conversation = Conversation.objects.get(id=1)
        self.assertFalse(conversation.participants.exists())

    def test_conversation_participants_set(self):
        """Conversation model participants field set test
        Check conversation's participants field exists return True
        Check conversation's participants field count equal 10
        Check conversation's all user query set name equal username
        """
        conversation = Conversation.objects.get(id=1)

        for i in range(1, 11):
            user = User.objects.create_user(f"test_user_{i}")
            conversation.participants.add(user)

        self.assertTrue(conversation.participants.exists())
        self.assertEqual(conversation.participants.count(), 10)

    def test_conversation_str_method(self):
        """Conversation model str method test
        Check str method equal __str__ method return format
        """
        conversation = Conversation.objects.get(id=1)
        self.assertEqual("2019-11-30 00:00:00+00:00", str(conversation))

    def test_conversation_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test List 1's created_at field is datetime (2019.11.30)
        """
        conversation = Conversation.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(conversation.created_at, mocked)

    def test_conversation_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test Conversation 1 objects and update Test Conversation 1 object
        Check Test Conversation 1's updated_at field is datetime (2019.12.01)
        """
        conversation = Conversation.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            conversation.save()
            self.assertEqual(conversation.updated_at, mocked)


class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running MessageModelTest

        Fields:
            id           : 1
            user         : test_user_10
            conversation : <Participants [test_user_1, ... ,test_user_10]>
            created_at   : 2019.11.30.00.00.00
            updated_at   : 2019.12.01.00.00.00
        """
        conversation = Conversation.objects.create()
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)

        for i in range(1, 11):
            user = User.objects.create_user(f"test_user_{i}")
            conversation.participants.add(user)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Message.objects.create(
                message="Test Message 1", user=user, conversation=conversation
            )

    def test_message_create_success(self):
        """Message model creation success test
        Check unique field and instance's class name
        """
        message = Message.objects.get(id=1)
        self.assertEqual("Message", message.__class__.__name__)
        self.assertEqual("test_user_10", message.user.username)

    def test_message_create_fail(self):
        """Message model creation failure test
        Message model must contain all fields
        """
        with self.assertRaises(IntegrityError):
            Message.objects.create()

    def test_message_get_message_fields(self):
        """Message model get message fields data test
        Check message model's message field equal Test Message 1
        """
        message = Message.objects.get(id=1)
        self.assertEqual("Test Message 1", message.message)

    def test_message_get_conversation_fields(self):
        """Message model get fields data test
        Check all fields except when testing create success test
        """
        message = Message.objects.get(id=1)
        self.assertTrue(message.conversation.participants.exists())
        self.assertEqual(message.conversation.participants.count(), 10)

        for idx, user in enumerate(message.conversation.participants.all()):
            self.assertEqual(f"test_user_{idx + 1}", user.username)

    def test_message_str_method(self):
        """Message model str method test
        Check str method equal __str__ method return format
        """
        message = Message.objects.get(id=1)
        self.assertEqual("test_user_10 says: Test Message 1", str(message))

    def test_message_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test Message 1's created_at field is datetime (2019.11.30)
        """
        message = Message.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(message.created_at, mocked)

    def test_message_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test Message 1 objects and update Test Message 1 object
        Check Test Message 1's updated_at field is datetime (2019.12.01)
        """
        message = Message.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            message.message = "Update Message 1"
            message.save()
            self.assertEqual("Update Message 1", message.message)
            self.assertEqual(message.updated_at, mocked)
