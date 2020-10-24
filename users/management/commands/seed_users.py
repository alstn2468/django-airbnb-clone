from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    help = "Automatically create users"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="Number of users to create")

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE USERS"))

            seeder = Seed.seeder()
            seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
            seeder.execute()

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL USERS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE USERS"))
