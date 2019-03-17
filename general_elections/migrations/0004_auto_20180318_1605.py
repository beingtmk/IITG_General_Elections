# Generated by Django 2.0.2 on 2018-03-18 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_elections', '0003_auto_20180318_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voterlist',
            name='dept',
            field=models.CharField(choices=[('BSBE', 'BSBE'), ('CE', 'CE'), ('CH', 'CH'), ('CH ', 'CH '), ('CL', 'CL'), ('CSE', 'CSE'), ('CST', 'CST'), ('DD', 'DD'), ('ECE', 'ECE'), ('EEE', 'EEE'), ('ENC', 'ENC'), ('ENV', 'ENV'), ('EPH', 'EPH'), ('HSS', 'HSS'), ('LST', 'LST'), ('MA', 'MA'), ('MC', 'MC'), ('ME', 'ME'), ('NT', 'NT'), ('PH', 'PH'), ('PH ', 'PH '), ('RT', 'RT'), ('NotListed', 'NotListed')], max_length=100),
        ),
        migrations.AlterField(
            model_name='voterlist',
            name='hostel',
            field=models.CharField(choices=[('Barak', 'Barak'), ('Bramhaputra', 'Bramhaputra'), ('Dhansiri', 'Dhansiri'), ('Dibang', 'Dibang'), ('Dihing', 'Dihing'), ('Kameng', 'Kameng'), ('Kapili', 'Kapili'), ('Lohit', 'Lohit'), ('Manas', 'Manas'), ('Siang', 'Siang'), ('Subansiri', 'Subansiri'), ('Umiam', 'Umiam'), ('Married Scholars', 'Married Scholars'), ('NA', 'NA')], max_length=100),
        ),
    ]
