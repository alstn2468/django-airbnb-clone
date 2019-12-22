from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):
    help = "Automatically create room types"

    def handle(self, *args, **options):
        try:
            room_types = ["Hotel room", "Shared room", "Private room", "Entire place"]

            self.stdout.write(self.style.SUCCESS("■ START CREATE ROOM TYPES"))

            for name in room_types:
                RoomType.objects.create(name=name)

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL ROOM TYPES!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE ROOM TYPES"))

