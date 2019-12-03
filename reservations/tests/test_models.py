from django.test import TestCase
from django.db import IntegrityError
from reservations.models import Reservation
from users.models import User
from rooms.models import Room
from datetime import datetime
from unittest import mock
import pytz


class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running ReservationModelTest

        Fields :
            id         : 1
            status     : STATUS_CONFIRMED (confirmed)
            check_in   : 2019.12.02
            check_out  : 2019.12.04
            guest      : test_user
            room       : test_room
            created_at : 2019.11.30.00.00.00
            updated_at : 2019.12.01.00.00.00
        """
        user = User.objects.create_user("test_user")
        room = Room.objects.create(
            name="test_room",
            description="Test Description 1",
            country="KR",
            city="Seoul",
            price=100,
            address="Test Address",
            guests=4,
            beds=2,
            bedrooms=1,
            baths=1,
            check_in=datetime(2019, 1, 1, 9, 30),
            check_out=datetime(2019, 1, 2, 10, 30),
            instant_book=True,
            host=user,
        )
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            Reservation.objects.create(
                status=Reservation.STATUS_CONFIRMED,
                check_in=datetime(2019, 12, 2),
                check_out=datetime(2019, 12, 4),
                guest=user,
                room=room,
            )

    def test_reservation_create_success(self):
        """Reservation model creation success test
        Check unique field and instance's class name
        """
        reservation = Reservation.objects.get(id=1)
        self.assertEqual("Reservation", reservation.__class__.__name__)
        self.assertEqual("test_user", reservation.guest.username)
        self.assertEqual("test_room", reservation.room.name)

    def test_reservation_create_fail(self):
        """Reservation model creation failure test
        Reservation model's all fields can't contain NULL, IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            Reservation.objects.create()

    def test_reservation_get_fields(self):
        """Reservation model get fields data test
        Check reservation's all fields except when testing create success test
        """
        reservation = Reservation.objects.get(id=1)
        self.assertEqual(reservation.status, Reservation.STATUS_CONFIRMED)
        self.assertEqual(reservation.check_in, datetime(2019, 12, 2).date())
        self.assertEqual(reservation.check_out, datetime(2019, 12, 4).date())

    def test_reservation_str_method(self):
        """Reservation model str method test
        Check str mehtod equal __str__ method return format
        """
        reservation = Reservation.objects.get(id=1)
        self.assertEqual("test_room - 2019-12-02", str(reservation))

    def test_reservation_time_stamp_created_at(self):
        """TimeStamp model created_at test
        Check Test Review 1's created_at field is datetime (2019.11.30)
        """
        reservation = Reservation.objects.get(id=1)
        mocked = datetime(2019, 11, 30, 0, 0, 0, tzinfo=pytz.utc)
        self.assertEqual(reservation.created_at, mocked)

    def test_reservation_time_stamp_updated_at(self):
        """TimeStamp model updated_at test
        Get Test Review 1 objects and update Test Review 1 object
        Check Test Review 1's updated_at field is datetime (2019.12.01)
        """
        reservation = Reservation.objects.get(id=1)
        mocked = datetime(2019, 12, 1, 0, 0, 0, tzinfo=pytz.utc)

        with mock.patch("django.utils.timezone.now", mock.Mock(return_value=mocked)):
            reservation.status = Reservation.STATUS_PENDING
            reservation.save()
            self.assertEqual(reservation.updated_at, mocked)
