# Generated by Django 3.2.4 on 2021-06-10 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_review_unique_review'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review',
        ),
    ]