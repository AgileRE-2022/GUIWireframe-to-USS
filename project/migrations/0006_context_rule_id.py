# Generated by Django 4.0.2 on 2022-06-03 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_context'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='rule_id',
            field=models.IntegerField(null=True),
        ),
    ]
