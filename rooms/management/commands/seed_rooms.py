from core.management.commands.custom_command import CustomCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from random import choice, randint
from rooms.models import Room, RoomType, Photo, Amenity, Facility, HouseRule
from users.models import User


class Command(CustomCommand):
    help = "Automatically create rooms"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="Number of rooms to create")

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE ROOMS"))

            users = User.objects.all()
            room_types = RoomType.objects.all()
            amenities = Amenity.objects.all()
            facilities = Facility.objects.all()
            house_rules = HouseRule.objects.all()

            seeder = Seed.seeder()
            seeder.add_entity(
                Room,
                number,
                {
                    "name": seeder.faker.address(),
                    "host": choice(users),
                    "room_type": choice(room_types),
                    "price": randint(1, 300),
                    "guests": randint(1, 10),
                    "beds": randint(1, 5),
                    "bedrooms": randint(1, 5),
                    "baths": randint(1, 5),
                },
            )
            clean_pk_list = flatten(list(seeder.execute().values()))

            for idx, pk in enumerate(clean_pk_list):
                room = Room.objects.get(pk=pk)
                BOOLEAN = [True, False]
                self.progress_bar(
                    idx + 1, number, prefix="■ PROGRESS", suffix="Complete", length=40
                )

                for i in range(randint(7, 27)):
                    Photo.objects.create(
                        caption=seeder.faker.sentence(),
                        file=f"room_photos/{randint(1, 31)}.webp",
                        room=room,
                    )

                for amenity in amenities:
                    if choice(BOOLEAN):
                        room.amenities.add(amenity)

                for facility in facilities:
                    if choice(BOOLEAN):
                        room.facilities.add(facility)

                for house_rule in house_rules:
                    if choice(BOOLEAN):
                        room.house_rules.add(house_rule)

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL ROOMS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE ROOMS"))
