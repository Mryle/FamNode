# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InformationText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=50)),
                ('data', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('surname', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('person1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personHigher', to='Family.Person')),
                ('person2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personLower', to='Family.Person')),
            ],
        ),
        migrations.AddField(
            model_name='informationtext',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Family.Person'),
        ),
    ]