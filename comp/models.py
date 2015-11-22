import cmath
import numpy as np
import scipy.stats as stats
import pylab as pl

from django.db import models

from stats.models import Parameters, Months

from comp.app_settings import FIG_DIRECTORY


class Company(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)

    @classmethod
    def create_data(cls, data):
        bi = []
        for _d in data:
            obj = cls(**_d)
            obj.full_clean()
            bi.append(obj)
        cls.objects.bulk_create(bi)


class CompanyStats(models.Model):
    company = models.ForeignKey(Company, to_field="code")
    param = models.ForeignKey("stats.Parameters", to_field="code")
    month = models.ForeignKey("stats.Months", to_field="code")
    value = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("company", "param", "month",)

    def __str__(self):
        return "%s-%s-%s(%s)" % (
            self.company_id, self.month_id,
            self.param_id, self.value)

    @classmethod
    def create_data(cls, month, data):
        bi = []
        ig = []
        for _d in data:
            comp = _d.pop("comp")
            for key in _d.keys():
                obj = {}
                obj.update(**{
                    "company_id": comp, "value": _d[key],
                    "month_id": month, "param_id": key})
                obj = cls(**obj)
                obj.full_clean()
                bi.append(obj)
        cls.objects.bulk_create(bi)


class CompanyMonthlyRating(models.Model):
    company = models.ForeignKey(Company, to_field="code")
    month = models.ForeignKey("stats.Months", to_field="code")
    rating = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("company", "month",)

    def __str__(self):
        return "%s:%s (%s)" % (
            self.company_id, self.month_id,
            self.rating)

    @classmethod
    def calcrating(cls, comp, month):
        stats = CompanyStats.objects.filter(
            company_id=comp, month_id=month).select_related("param")

        rating = float(sum([
            each.param.associated_value * each.value for each in stats]) / sum(
                stats.values_list("param__associated_value", flat=True)))
        return cls.objects.get_or_create(month_id=month, company_id=comp, defaults={
            "month_id": month, "company_id": comp, "rating": rating})

    @classmethod
    def mean(cls, month):
        stats = cls.objects.filter(month_id=month)
        total = sum(stats.values_list("rating", flat=True))
        N = stats.count()
        return total / N

    @classmethod
    def standard_deviation(cls, month):
        stats = cls.objects.filter(month_id=month)
        total = stats.values_list("rating", flat=True)
        N = stats.count()
        mean = cls.mean(month)
        sum_diff = sum([(mean-float(each))**2 for each in total])
        sd = cmath.sqrt(sum_diff / N-1)
        return sd.imag * 100

    @classmethod
    def crs(cls, month, company):
        stat = cls.objects.filter(month_id=month)
        comp = stat.get(company_id=company)
        statics = [float(e) for e in stat.values_list("rating", flat=True)]
        return stats.percentileofscore(statics, comp.rating, kind='mean')

    @classmethod
    def monthly_matrix(cls, month):
        stat = cls.objects.filter(month_id=month)
        stat = sorted([float(e) for e in stat.values_list("rating", flat=True)])
        fit = stats.norm.pdf(stat, np.mean(stat), np.std(stat))
        pl.plot(stat, fit,'-o')
        pl.hist(stat, normed=True)
        path = FIG_DIRECTORY + "%s.pdf" % month
        pl.savefig(path)
        return path
