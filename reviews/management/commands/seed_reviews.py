from core.management.commands.custom_command import CustomCommand
from django_seed import Seed
from random import randint
from reviews.models import Review
from rooms.models import Room


class Command(CustomCommand):
    help = "Automatically create reviews"

    def add_arguments(self, parser):
        parser.add_argument("--number", default=1, help="Number of reviews to create")

    def handle(self, *args, **options):
        try:
            number = int(options.get("number"))

            self.stdout.write(self.style.SUCCESS("■ START CREATE REVIEWS"))

            for i in range(100):
                self.stdout.write("%{}".format(i), ending="\r")
                self.stdout.flush()
                time.sleep(0.01)

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL REVIEWS!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE REVIEWS"))

