from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):
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

            for name in amenities:
                Amenity.objects.create(name=name)

            self.stdout.write(self.style.SUCCESS("■ SUCCESS CREATE ALL AMENITIES!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"■ {e}"))
            self.stdout.write(self.style.ERROR("■ FAIL CREATE AMENITIES"))

