# Generated by Django 2.2.13 on 2020-08-22 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_factory_cet_reviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='cet_staff',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]