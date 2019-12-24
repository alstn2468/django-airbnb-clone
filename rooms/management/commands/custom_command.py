from django.core.management.base import BaseCommand


class CustomCommand(BaseCommand):
    def progress_bar(
        self,
        iteration,
        total,
        prefix="",
        suffix="",
        decimals=1,
        length=100,
        fill="█",
        printEnd="\r",
    ):
        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(total))
        )
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + "-" * (length - filledLength)

        self.stdout.write(
            self.style.SUCCESS("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix)),
            ending=printEnd,
        )

        if iteration == total:
            self.stdout.write("\n")
