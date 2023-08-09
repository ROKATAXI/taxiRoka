from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchingRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('departure_area', models.CharField(max_length=10)),
                ('destination_area', models.CharField(max_length=10)),
                ('max_num', models.IntegerField()),
                ('current_num', models.IntegerField()),
                ('create_date', models.DateTimeField()),
                ('end_yn', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Matching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_yn', models.BooleanField()),
                ('seat_num', models.IntegerField()),
                ('matching_date', models.DateTimeField()),
                ('matching_room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.matchingroom')),
            ],
        ),
    ]
