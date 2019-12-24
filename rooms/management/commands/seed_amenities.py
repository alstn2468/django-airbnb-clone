from core.management.commands.custom_command import CustomCommand
from rooms.models import Amenity


class Command(CustomCommand):
    help = "Automatically create amenities"

    def handle(self, *args, **options):
        try:
            amenities = [
                "Air conditioning",
                "Alarm Clock",
                "Balcony",
                "Bathroom",
                "Bathtub",
                "Bed Linen",
                "Boating",
                "Cable TV",
                "Carbon monoxide detectors",
                "Chairs",
                "Children Area",
                "Coffee Maker in Room",
                "Cooking hob",
                "Cookware & Kitchen Utensils",
                "Dishwasher",
                "Double bed",
                "En suite bathroom",
                "Free Parking",
                "Free Wireless Internet",
                "Freezer",
                "Fridge / Freezer",
                "Golf",
                "Hair Dryer",
                "Heating",
                "Hot tub",
                "Indoor Pool",
                "Ironing Board",
                "Microwave",
                "Outdoor Pool",
                "Outdoor Tennis",
                "Oven",
                "Queen size bed",
                "Restaurant",
                "Shopping Mall",
                "Shower",
                "Smoke detectors",
                "Sofa",
                "Stereo",
                "Swimming pool",
                "Toilet",
                "Towels",
                "TV",
            ]

            self.stdout.write(self.style.SUCCESS("■ START CREATE AMENITIES"))

            for idx, name in enumerate(amenities):
                Amenity.objects.create(name=name)
                self.progress_bar(
                    idx + 1,
                    len(amenities),
                    prefix="■ PROGRESS",
                    suffix="Complete",
                    length=40,
                )

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL AMENITIES!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE AMENITIES"))

