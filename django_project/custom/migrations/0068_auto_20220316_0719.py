# Generated by Django 2.2.16 on 2022-03-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0067_auto_20220303_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='summaryreportcategory',
            name='show_percentage',
            field=models.BooleanField(default=False, help_text='Show percentage value rather than absolute value.'),
        ),
        migrations.AlterField(
            model_name='summaryreportcategory',
            name='category',
            field=models.CharField(blank=True, default='', help_text='To be displayed in the table for the total value e.g. Total Number of health facilities.', max_length=255),
        ),
    ]
