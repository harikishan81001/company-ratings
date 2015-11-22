# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_months'),
        ('comp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyStats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=5, decimal_places=2)),
                ('company', models.ForeignKey(to='comp.Company')),
                ('month', models.ForeignKey(to='stats.Months')),
                ('param', models.ForeignKey(to='stats.Parameters')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='companystats',
            unique_together=set([('company', 'param', 'month')]),
        ),
    ]
