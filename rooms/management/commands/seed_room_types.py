from core.management.commands.custom_command import CustomCommand
from rooms.models import RoomType


class Command(CustomCommand):
    help = "Automatically create room types"

    def handle(self, *args, **options):
        try:
            room_types = ["Hotel room", "Shared room", "Private room", "Entire place"]

            self.stdout.write(self.style.SUCCESS("■ START CREATE ROOM TYPES"))

            for idx, name in enumerate(room_types):
                RoomType.objects.create(name=name)
                self.progress_bar(
                    idx + 1,
                    len(room_types),
                    prefix="■ PROGRESS",
                    suffix="Complete",
                    length=40,
                )

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL ROOM TYPES!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE ROOM TYPES"))
