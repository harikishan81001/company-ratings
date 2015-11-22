# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0002_auto_20151122_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companystats',
            name='company',
            field=models.ForeignKey(to='comp.Company', to_field=b'code'),
        ),
        migrations.AlterField(
            model_name='companystats',
            name='month',
            field=models.ForeignKey(to='stats.Months', to_field=b'code'),
        ),
        migrations.AlterField(
            model_name='companystats',
            name='param',
            field=models.ForeignKey(to='stats.Parameters', to_field=b'code'),
        ),
    ]
