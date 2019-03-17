# Generated by Django 2.0.2 on 2018-03-16 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import general_elections.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contestants',
            fields=[
                ('webmail_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('agenda1', models.CharField(max_length=140)),
                ('agenda2', models.CharField(max_length=140)),
                ('agenda3', models.CharField(max_length=140)),
                ('image', models.FileField(upload_to=general_elections.models.user_directory_path)),
                ('post', models.CharField(choices=[('VP', 'Vice President'), ('HAB', 'Gen Sec - Hostel Affairs Board'), ('TECH', 'Gen Sec - Technical Board'), ('CULT', 'Gen Sec - Cultural Board'), ('WELFARE', 'Gen Sec - Students Welfare Board'), ('SPORTS', 'Gen Sec - Sports Board'), ('SAIL', 'Gen Sec - SAIL'), ('CBS', 'Gen Sec - CBS'), ('UGS', 'Under Graduate Senator'), ('PGS', 'Post Graduate Senator'), ('GS', 'Girl Senator')], max_length=7)),
                ('mobile_no', models.CharField(max_length=10)),
                ('eligible', models.BooleanField(default=True)),
                ('comments', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VoterList',
            fields=[
                ('webmail_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('dept', models.CharField(max_length=100)),
                ('hostel', models.CharField(max_length=100)),
                ('roll_no', models.CharField(max_length=9)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('program', models.CharField(choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')], max_length=2)),
                ('mobile_no', models.CharField(max_length=10)),
                ('comments', models.CharField(max_length=140)),
                ('has_voted', models.BooleanField(default=False)),
                ('voting_start', models.DateTimeField(blank=True, null=True)),
                ('voting_end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VotesPG',
            fields=[
                ('webmail_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('vp', models.CharField(max_length=60)),
                ('hab', models.CharField(max_length=60)),
                ('tech', models.CharField(max_length=60)),
                ('cult', models.CharField(max_length=60)),
                ('welfare', models.CharField(max_length=60)),
                ('sports', models.CharField(max_length=60)),
                ('sail', models.CharField(max_length=60)),
                ('cbs', models.CharField(max_length=60)),
                ('pgs_1', models.CharField(max_length=60)),
                ('pgs_2', models.CharField(max_length=60)),
                ('pgs_3', models.CharField(max_length=60)),
                ('pgs_4', models.CharField(max_length=60)),
                ('pgs_5', models.CharField(max_length=60)),
                ('pgs_6', models.CharField(max_length=60)),
                ('gs_1', models.CharField(max_length=60)),
                ('gs_2', models.CharField(max_length=60)),
                ('gs_3', models.CharField(max_length=60)),
                ('voting_start', models.DateTimeField(blank=True, null=True)),
                ('voting_end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VotesUG',
            fields=[
                ('webmail_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('vp', models.CharField(max_length=60)),
                ('hab', models.CharField(max_length=60)),
                ('tech', models.CharField(max_length=60)),
                ('cult', models.CharField(max_length=60)),
                ('welfare', models.CharField(max_length=60)),
                ('sports', models.CharField(max_length=60)),
                ('sail', models.CharField(max_length=60)),
                ('cbs', models.CharField(max_length=60)),
                ('ugs_1', models.CharField(max_length=60)),
                ('ugs_2', models.CharField(max_length=60)),
                ('ugs_3', models.CharField(max_length=60)),
                ('ugs_4', models.CharField(max_length=60)),
                ('ugs_5', models.CharField(max_length=60)),
                ('ugs_6', models.CharField(max_length=60)),
                ('ugs_7', models.CharField(max_length=60)),
                ('gs_1', models.CharField(max_length=60)),
                ('gs_2', models.CharField(max_length=60)),
                ('gs_3', models.CharField(max_length=60)),
                ('voting_start', models.DateTimeField(blank=True, null=True)),
                ('voting_end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
