# Generated by Django 3.2.4 on 2021-06-10 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210610_1937'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('title', 'author')},
        ),
    ]