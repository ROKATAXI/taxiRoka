# Generated by Django 4.2.4 on 2023-08-05 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchingroom',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
