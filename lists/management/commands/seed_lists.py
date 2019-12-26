from django.contrib.admin.utils import flatten
from core.management.commands.custom_command import CustomCommand
from django_seed import Seed
from random import randint, choice
from rooms.models import Room
from users.models import User
from lists.models import List


class Command(CustomCommand):
    help = "Automatically create lists"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="Number of lists to create")

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE LISTS"))

            users = User.objects.all()
            rooms = Room.objects.all()

            seeder = Seed.seeder()
            seeder.add_entity(
                List, number, {"user": lambda x: choice(users)},
            )

            clean_pk_list = flatten(list(seeder.execute().values()))

            for idx, pk in enumerate(clean_pk_list):
                self.progress_bar(
                    idx + 1,
                    len(clean_pk_list),
                    prefix="■ PROGRESS",
                    suffix="Complete",
                    length=40,
                )
                list_model = List.objects.get(pk=pk)
                rooms = rooms[randint(0, 5) : randint(6, len(rooms))]
                list_model.rooms.add(*rooms)

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL LISTS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE LISTS"))
