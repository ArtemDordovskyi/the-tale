# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-02-24 17:44
from __future__ import unicode_literals

import json

from django.db import migrations


NEW_SIZES = {0: 3,
             1: 3,
             2: 4,
             3: 0,
             4: 3,
             5: 3,
             6: 1,
             7: 1,
             8: 3,
             9: 3,
             10: 3,
             11: 2,
             12: 2,
             13: 2,
             14: 2}


def fill_properties(apps, schema_editor):
    Companion = apps.get_model("companions", "CompanionRecord")

    for companion in Companion.objects.all().iterator():
        data = json.loads(companion.data)

        data['features'] = [feature for feature in data.get('features', ()) if feature != 0]
        data['size'] = NEW_SIZES[data.get('size', 0)]
        data['orientation'] = 0 if data.get('body') in (1, 4) else 1

        if companion.id in (39, 162, 103, 130, 38, 65, 163, 96, 40, 41, 67, 102, 55, 95, 42, 145, 66, 97, 113):
            data['weapons'][0] = {'weapon': 27,
                                  'material': 8,
                                  'power_type': 4}

        if companion.id in (139, 140):
            data['weapons'][0] = {'weapon': 28,
                                  'material': 10,
                                  'power_type': 4}

        if companion.id == 49:
            data['weapons'][0] = {'weapon': 30,
                                  'material': 2,
                                  'power_type': 4}

        if companion.id == 71:
            data['weapons'][0] = {'weapon': 31,
                                  'material': 10,
                                  'power_type': 4}

        if companion.id in (69, 84):
            data['weapons'][0] = {'weapon': 32,
                                  'material': 3,
                                  'power_type': 4}

        if companion.id == 3:
            data['weapons'][0] = {'weapon': 33,
                                  'material': 3,
                                  'power_type': 4}

        if companion.id in (1, 167):
            data['weapons'][0] = {'weapon': 34,
                                  'material': 2,
                                  'power_type': 4}

        if companion.id == 37:
            data['structure'] = 8

        if companion.id in (37, 60):
            data['features'].append(53)

        if companion.id == 51:
            data['features'].append(54)

        if companion.id == 171:
            data['movement'] = 12

        if companion.id in (169, 165, 164, 166, 167, 143):
            data['body'] = 19

        companion.data = json.dumps(data)

        companion.save()


class Migration(migrations.Migration):

    dependencies = [
        ('companions', '0004_auto_20161019_1613'),
    ]

    operations = [
        migrations.RunPython(
            fill_properties,
        ),
    ]
