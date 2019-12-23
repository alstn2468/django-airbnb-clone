from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from random import choice, randint
from rooms.models import Room, RoomType, Photo
from users.models import User


class Command(BaseCommand):
    help = "Automatically create rooms"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="Number of rooms to create")

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE ROOMS"))

            users = User.objects.all()
            room_types = RoomType.objects.all()

            seeder = Seed.seeder()
            seeder.add_entity(
                Room,
                number,
                {
                    "name": lambda x: seeder.faker.address(),
                    "host": lambda x: choice(users),
                    "room_type": lambda x: choice(room_types),
                    "price": lambda x: randint(1, 300),
                    "guests": lambda x: randint(1, 10),
                    "beds": lambda x: randint(1, 5),
                    "bedrooms": lambda x: randint(1, 5),
                    "baths": lambda x: randint(1, 5),
                },
            )
            clean_pk_list = flatten(list(seeder.execute().values()))

            for pk in clean_pk_list:
                room = Room.objects.get(pk=pk)

                for i in range(randint(7, 14)):
                    Photo.objects.create(
                        caption=seeder.faker.sentence(),
                        file=f"room_photos/{randint(1, 31)}.webp",
                        room=room,
                    )

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL ROOMS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE ROOMS"))

