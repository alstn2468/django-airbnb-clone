from core.management.commands.custom_command import CustomCommand
from django_seed import Seed
from datetime import datetime, timedelta
from random import randint, choice
from rooms.models import Room
from users.models import User
from reservations.models import Reservation


class Command(CustomCommand):
    help = "Automatically create reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="Number of reservations to create"
        )

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE RESERVATIONS"))

            users = User.objects.all()
            rooms = Room.objects.all()

            seeder = Seed.seeder()
            seeder.add_entity(
                Reservation,
                number,
                {
                    "status": lambda x: choice(
                        [
                            Reservation.STATUS_CANCELED,
                            Reservation.STATUS_CONFIRMED,
                            Reservation.STATUS_PENDING,
                        ]
                    ),
                    "guest": lambda x: choice(users),
                    "room": lambda x: choice(rooms),
                    "check_in": lambda x: datetime.now(),
                    "check_out": lambda x: datetime.now()
                    + timedelta(days=randint(3, 25)),
                },
            )
            seeder.execute()

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL RESERVATIONS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE RESERVATIONS"))
