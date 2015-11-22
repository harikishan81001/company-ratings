# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_months'),
    ]

    operations = [
        migrations.AddField(
            model_name='parameters',
            name='associated_value',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
            preserve_default=False,
        ),
    ]
