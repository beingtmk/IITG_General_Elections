from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

class Volunteer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

class Voter(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

class VoterList(models.Model):
	PROGRAM_CATEGORY = (
		('UG', 'Undergraduate'),
		('PG', 'Postgraduate'),
	)
	GENDER_CATEGORY = (
		('M', 'Male'),
		('F', 'Female'),
	)
	HOSTEL_CATEGORY = (
		('Barak', 'Barak'),
		('Bramhaputra', 'Bramhaputra'),
		('Dhansiri', 'Dhansiri'),
		('Dibang', 'Dibang'),
		('Dihing', 'Dihing'),
		('Kameng', 'Kameng'),
		('Kapili', 'Kapili'),
		('Lohit', 'Lohit'),
		('Manas', 'Manas'),
		('Siang', 'Siang'),
		('Subansiri', 'Subansiri'),
		('Umiam', 'Umiam'),
		('Married Scholars', 'Married Scholars'),
		('NA', 'NA')
	)
	DEPT_CATEGORY = (
		('BSBE', 'BSBE') ,
		('CE', 'CE') ,
		('CH', 'CH') ,
		('CL', 'CL') ,
		('CSE', 'CSE') ,
		('CST', 'CST') ,
		('DD', 'DD') ,
		('ECE', 'ECE') ,
		('EEE', 'EEE') ,
		('ENC', 'ENC') ,
		('ENV', 'ENV') ,
		('EPH', 'EPH') ,
		('HSS', 'HSS') ,
		('LST', 'LST') ,
		('MA', 'MA') ,
		('MC', 'MC') ,
		('ME', 'ME') ,
		('NT', 'NT') ,
		('PH', 'PH') ,
		('RT', 'RT') ,
		('NotListed1', 'NotListed1'),
	)
	webmail_id = models.CharField(max_length=100, primary_key = True)
	name = models.CharField(max_length=100)
	dept = models.CharField(max_length=100, choices=DEPT_CATEGORY)
	hostel = models.CharField(max_length=100, choices=HOSTEL_CATEGORY)
	roll_no = models.CharField(max_length=9)
	gender = models.CharField(max_length=1, choices=GENDER_CATEGORY)
	program = models.CharField(max_length=2, choices=PROGRAM_CATEGORY)
	mobile_no = models.CharField(max_length=10)
	comments = models.CharField(max_length=140) # big enough for a tweet
	has_voted = models.BooleanField(default=False)
	voting_start = models.DateTimeField(blank=True, null=True)
	voting_end = models.DateTimeField(blank=True, null=True)
	course_registeration = models.BooleanField(default=True) # course registeration status
	def __str__(self):
		return self.webmail_id + '::' + self.name + '::' + self.roll_no

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/webmail_id
	return instance.webmail_id+'.jpg'

class Contestants(models.Model):
	POSTS = (
		('VP', 'Vice President'),
		('HAB', 'Gen Sec - Hostel Affairs Board'),
		('TECH','Gen Sec - Technical Board'),
		('CULT', 'Gen Sec - Cultural Board'),
		('WELFARE', 'Gen Sec - Students Welfare Board'),
		('SPORTS', 'Gen Sec - Sports Board'),
		('SAIL', 'Gen Sec - SAIL'),
		('SWC', 'Gen Sec - SWC'),
		('UGS', 'Under Graduate Senator'),
		('PGS', 'Post Graduate Senator'),
		('GS', 'Girl Senator'),
	)
	webmail_id = models.CharField(max_length=100, primary_key = True)
	name = models.CharField(max_length=100)
	agenda1 = models.CharField(max_length=140)
	agenda2 = models.CharField(max_length=140)
	agenda3 = models.CharField(max_length=140)
	image = models.FileField(upload_to=user_directory_path)
	post = models.CharField(max_length=7, choices=POSTS)
	mobile_no = models.CharField(max_length = 10)
	eligible = models.BooleanField(default=True)
	comments = models.CharField(max_length=140)
	def __str__(self):
		return self.name

class VotesUG(models.Model):
	webmail_id = models.CharField(max_length=100, primary_key = True)
	vp = models.CharField(max_length=60) #hash of the voted contestant webmail-id. len(hash)=60
	hab = models.CharField(max_length=60)
	tech = models.CharField(max_length=60)
	cult = models.CharField(max_length=60)
	welfare = models.CharField(max_length=60)
	sports = models.CharField(max_length=60)
	sail = models.CharField(max_length=60)
	swc = models.CharField(max_length=60)
	ugs_1 = models.CharField(max_length=60)
	ugs_2 = models.CharField(max_length=60)
	ugs_3 = models.CharField(max_length=60)
	ugs_4 = models.CharField(max_length=60)
	ugs_5 = models.CharField(max_length=60)
	ugs_6 = models.CharField(max_length=60)
	ugs_7 = models.CharField(max_length=60)
	gs_1 = models.CharField(max_length=60)
	gs_2 = models.CharField(max_length=60)
	gs_3 = models.CharField(max_length=60)
	voting_start = models.DateTimeField(blank=True, null=True)
	voting_end = models.DateTimeField(blank=True, null=True)

class VotesPG(models.Model):
	webmail_id = models.CharField(max_length=100, primary_key = True)
	vp = models.CharField(max_length=60)
	hab = models.CharField(max_length=60)
	tech = models.CharField(max_length=60)
	cult = models.CharField(max_length=60)
	welfare = models.CharField(max_length=60)
	sports = models.CharField(max_length=60)
	sail = models.CharField(max_length=60)
	swc = models.CharField(max_length=60)
	pgs_1 = models.CharField(max_length=60)
	pgs_2 = models.CharField(max_length=60)
	pgs_3 = models.CharField(max_length=60)
	pgs_4 = models.CharField(max_length=60)
	pgs_5 = models.CharField(max_length=60)
	pgs_6 = models.CharField(max_length=60)
	pgs_7 = models.CharField(max_length=60)
	gs_1 = models.CharField(max_length=60)
	gs_2 = models.CharField(max_length=60)
	gs_3 = models.CharField(max_length=60)
	voting_start = models.DateTimeField(blank=True, null=True)
	voting_end = models.DateTimeField(blank=True, null=True)
