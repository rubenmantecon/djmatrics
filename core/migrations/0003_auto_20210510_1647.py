# Generated by Django 3.2 on 2021-05-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_uf_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolment',
            name='uf',
            field=models.ManyToManyField(to='core.UF'),
        ),
        migrations.DeleteModel(
            name='EnrolmentUF',
        ),
    ]
