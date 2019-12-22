from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This is Room application command."

    def add_arguments(self, parser):
        parser.add_argument("--times", help="How many times do you want to tell")

    def handle(self, *args, **options):
        times = int(options.get("times"))

        for time in range(times):
            self.stdout.write(self.style.SUCCESS("Room Command"))
