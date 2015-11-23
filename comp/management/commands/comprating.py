from __future__ import absolute_import

from django.core.management.base import BaseCommand, CommandError
from django.db.models.loading import get_model

from comp.models import CompanyMonthlyRating, Company
from stats.models import Months


class Command(BaseCommand):

    help = "Management command to load initial data"

    def handle(self, *args, **options):
        months = Months.objects.all()
        cmps = Company.objects.all()
        for month in months:
            for comp in cmps:
                print CompanyMonthlyRating.calcrating(comp.code, month.code)
        self.stdout.write(
            'Successfully calculated ranking for')
