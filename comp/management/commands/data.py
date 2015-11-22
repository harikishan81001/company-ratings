from __future__ import absolute_import

from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_model

from comp.utils import File2Json


class Command(BaseCommand):

    help = "Management command to load initial data"

    def add_arguments(self, parser):
        parser.add_argument('--filepath',  dest='filepath', type=str)
        parser.add_argument('--model',  dest='model', type=str)

    def validate_options(self, **options):
        try:
            model = options.get("model")
            model = model.split(".")
            self.model = get_model(model[0], model[1])
        except (IndexError, AttributeError), e:
            raise CommandError(
                "No model name passed, run command by passing"
                " argument --model=app.modelname")
        except LookupError, e:
            raise CommandError(
                "Invalid model name passed, run command by passing"
                " argument --model=app.modelname")
        try:
            file_path = options["filepath"]
            if not file_path:
                raise KeyError
            f = File2Json(file_path)
            self.data = f.convert()
        except KeyError, e:
            raise CommandError(
                "Invalid file argument, run command by passing"
                "argument --filepath=/home/csvs/csvfilepath.csv")
        except Exception, e:
            raise CommandError(str(e))

    def handle(self, *args, **options):
        self.validate_options(**options)
        try:
            self.model.create_data(self.data)
        except Exception, e:
            raise CommandError("Can not upload data - %s" % str(e))
        self.stdout.write(
            'Successfully uploaded data for "%s"' % self.model.__name__)
