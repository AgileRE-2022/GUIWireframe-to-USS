# Generated by Django 4.0.2 on 2022-06-03 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_merge_20220601_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='Context',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wireframe_id', models.IntegerField()),
                ('context_type', models.CharField(max_length=200)),
                ('component_id', models.IntegerField(null=True)),
                ('activity_id', models.IntegerField(null=True)),
                ('context_conjunction', models.CharField(max_length=20)),
                ('context_statement', models.CharField(max_length=200)),
            ],
        ),
    ]
