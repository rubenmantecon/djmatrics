# Generated by Django 3.2 on 2021-05-12 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210512_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolment',
            name='profile_req',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.profilerequirement'),
        ),
    ]