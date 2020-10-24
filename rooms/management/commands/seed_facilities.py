from core.management.commands.custom_command import CustomCommand
from rooms.models import Facility


class Command(CustomCommand):
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

            for idx, name in enumerate(facilities):
                Facility.objects.create(name=name)
                self.progress_bar(
                    idx + 1,
                    len(facilities),
                    prefix="■ PROGRESS",
                    suffix="Complete",
                    length=40,
                )

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL FACILITIES!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE FACILITIES"))
