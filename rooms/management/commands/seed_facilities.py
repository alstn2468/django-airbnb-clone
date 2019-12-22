from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "Automatically create facilities"

    def handle(self, *args, **options):
        try:
            facilities = [
                "Private entrance",
                "Paid parking on premises",
                "Paid parking off premises",
                "Elevator",
                "Parking",
                "Gym",
            ]

            self.stdout.write(self.style.SUCCESS("■ START CREATE FACILITIES"))

            for name in facilities:
                Facility.objects.create(name=name)

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL FACILITIES!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE FACILITIES"))

