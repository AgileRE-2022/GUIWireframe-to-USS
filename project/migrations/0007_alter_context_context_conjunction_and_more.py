# Generated by Django 4.0.2 on 2022-06-05 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_context_rule_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='context',
            name='context_conjunction',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='context',
            name='context_statement',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
