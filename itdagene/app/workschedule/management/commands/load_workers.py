import json
import os

from django.core.management.base import BaseCommand

from itdagene.app.workschedule.models import Worker


class Command(BaseCommand):
    option_list = BaseCommand.option_list

    requires_model_validation = False
    help = ""

    def handle(self, *args, **options) -> None:
        path = args[0]
        if not os.path.exists(path):
            print("First argument should be the path to the file with worker info")
            return

        with open(path, encoding="utf-8") as json_data:
            data = json.load(json_data)

        count = 0

        for worker in data:
            w = Worker(
                phone=int(worker["tlf"]),
                username=worker["username"],
                email=f"{worker['username']}@stud.ntnu.no",
            )
            if "name" in worker:
                w.name = worker["name"]
            else:
                w.name = (f"{worker['firstname']} {worker['lastname']}",)

            try:
                w.t_shirt_size = int(worker["storrelse"])
            except ValueError:
                str_ = worker["storrelse"].upper()
                sizes = ("XS", "S", "M", "L", "XL", "XXL", "XXXL", "XXXXL")
                w.t_shirt_size = sizes.index(str_) + 1

            w.save()
            count += 1

        print(f"Added {count} workers")
