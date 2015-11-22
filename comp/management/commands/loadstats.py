from __future__ import absolute_import

from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_model

from comp.utils import File2Json
from comp.models import CompanyStats


class Command(BaseCommand):

    help = "Management command to load initial data"

    def add_arguments(self, parser):
        parser.add_argument('--filepath',  dest='filepath', type=str)
        parser.add_argument('--month',  dest='month', type=str)

    def validate_options(self, **options):
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

        try:
            self.month = options["month"]
            if not file_path:
                raise KeyError
        except KeyError, e:
            raise CommandError(
                "Invalid file argument, run command by passing"
                "argument --filepath=/home/csvs/csvfilepath.csv")

    def handle(self, *args, **options):
        self.validate_options(**options)
        try:
            CompanyStats.create_data(self.month, self.data)
        except Exception, e:
            raise CommandError("Can not upload data - %s" % str(e))
        self.stdout.write(
            'Successfully uploaded data for "%s"' % self.model.__name__)
