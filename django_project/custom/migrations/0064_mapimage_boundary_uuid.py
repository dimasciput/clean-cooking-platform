# Generated by Django 2.2.16 on 2022-01-19 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0063_mapimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapimage',
            name='boundary_uuid',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
