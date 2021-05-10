# Generated by Django 3.2 on 2021-05-06 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_profilerequirement_profile_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilerequirement',
            name='profile_type',
            field=models.CharField(choices=[('EX', 'exemption'), ('BO', 'bonus')], default=None, max_length=9, verbose_name='profile_type'),
        ),
    ]