# Generated by Django 2.2.16 on 2022-03-03 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0066_auto_20220222_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='preset',
            name='population_ani_text',
            field=models.CharField(default='Population with medium to high Assistance Needed Index', help_text='Description text in the report', max_length=255),
        ),
        migrations.AddField(
            model_name='preset',
            name='population_ccp_text',
            field=models.CharField(default='Population within areas of high clean cooking potential index', help_text='Description text in the report', max_length=255),
        ),
        migrations.AddField(
            model_name='preset',
            name='population_supply_text',
            field=models.CharField(default='Population within areas of high supply index', help_text='Description text in the report', max_length=255),
        ),
    ]
