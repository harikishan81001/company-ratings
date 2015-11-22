# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_parameters_associated_value'),
        ('comp', '0003_auto_20151122_0905'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyMonthlyRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.DecimalField(max_digits=5, decimal_places=2)),
                ('company', models.ForeignKey(to='comp.Company', to_field=b'code')),
                ('month', models.ForeignKey(to='stats.Months', to_field=b'code')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='companymonthlyrating',
            unique_together=set([('company', 'month')]),
        ),
    ]
