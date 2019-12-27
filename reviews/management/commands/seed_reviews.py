from core.management.commands.custom_command import CustomCommand
from django_seed import Seed
from random import randint, choice
from reviews.models import Review
from rooms.models import Room
from users.models import User


class Command(CustomCommand):
    help = "Automatically create reviews"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="Number of reviews to create")

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE REVIEWS"))

            users = User.objects.all()
            rooms = Room.objects.all()

            for idx, room in enumerate(rooms):
                seeder = Seed.seeder()
                seeder.add_entity(
                    Review,
                    number,
                    {
                        "accuracy": randint(0, 6),
                        "communication": randint(0, 6),
                        "cleanliness": randint(0, 6),
                        "location": randint(0, 6),
                        "check_in": randint(0, 6),
                        "value": randint(0, 6),
                        "room": room,
                        "user": choice(users),
                    },
                )

                self.progress_bar(
                    idx + 1,
                    len(rooms),
                    prefix="■ PROGRESS",
                    suffix="Complete",
                    length=40,
                )

                seeder.execute()

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL REVIEWS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE REVIEWS"))
