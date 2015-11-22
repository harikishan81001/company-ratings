from django.db import models

# Create your models here.


class Parameters(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    associated_value = models.DecimalField(max_digits=5, decimal_places=2)

    @classmethod
    def create_data(cls, data):
        bi = []
        for _d in data:
            obj = cls(**_d)
            obj.full_clean()
            bi.append(obj)
        cls.objects.bulk_create(bi)


class Months(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)

    @classmethod
    def create_data(cls, data):
        bi = []
        for _d in data:
            obj = cls(**_d)
            obj.full_clean()
            bi.append(obj)
        cls.objects.bulk_create(bi)
