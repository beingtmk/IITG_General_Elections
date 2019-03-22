from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control, never_cache
from django.core.signing import Signer
from django.core.paginator import Paginator
from django.db.models import Count, F
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist
from threading import Thread
import bcrypt
import time, multiprocessing, pickle
import logging
import pandas as pd

from ..models import *
from ..forms import VolunteerForm, VoterListForm, AddVoterForm, AddContestantForm
from .api import webmail_login
from authentication.authhelper import get_signin_url


logger = logging.getLogger(__name__)

# Custom decorators
def is_admin(user):
	return Admin.objects.filter(user=user).exists()

def is_volunteer(user):
	return Volunteer.objects.filter(user=user).exists()

def get_or_none(classmodel, **kwargs):
	try:
		return classmodel.objects.get(**kwargs)
	except ObjectDoesNotExist:
		return None



# Views
def index(request):
	redirect_uri = request.build_absolute_uri(
		reverse('authentication:gettoken'))
		
	mail = request.session.get('mail', None)

	admin = False
	volunteer = False

	if(mail):
		username = mail.split('@')[0]
		user = get_or_none(User, username=username)
		admin = is_admin(user)
		volunteer = is_volunteer(user)

	context = {
		'name' : request.session.get('name', None),
		'roll_number' : request.session.get('roll_number', None),
		'mail' : request.session.get('mail', None),
		'access_token' : request.session.get('access_token', None),
		'sign_in_url' : get_signin_url(redirect_uri),
		"is_admin" : admin,
		"is_volunteer" : volunteer
	}

	return render(request, 'index.html', context)

"""
Two stage login.
	1. Election webmail id + password ('admin_login.html')
	2. Personal webmail id + password + passphrase ('admin_personal_login.html')
passphrase = password for django User of the admin

"""
def admin_webmail_login(request):
	if request.method == "GET":
		return render(request, 'admin_login.html')
	elif request.method == "POST":
		# Add check for Election id
		valid = ['elections', 'amogh.gupta', 'k.durgesh', 'swc', 'dos'] # 'mehul.jain']
		election_id = request.POST["election_id"]
		if election_id not in valid:
			err = 'Unauthorised User'
			log = 'Admin: Unauthorised user attempt webmail_id credentials:%s'%(election_id)
			logger.info(log)
			return render(request, 'admin_login.html', {'error': err})
		election_password = request.POST["election_password"]
		login_server = request.POST["login_server"]
		if webmail_login(election_id, election_password, login_server):
			request.session['election_login'] = Signer().sign('TRUE')
			logger.info('Admin: election webmail_id credentials verified')
			return redirect('admin_personal_login')
		else:
			err = 'Invalid credentials'
			logger.info('Admin: invalid election webmail_id credentials')
			return render(request, 'admin_login.html', {'error': err})

def admin_personal_login(request):
	# Retrieve step 1 login proof
	election_login = request.session.get('election_login', None)
	if election_login is not None:
		election_login = Signer().unsign(election_login)
		if election_login == 'TRUE':
			# Ensured that user is logged in with election id
			if request.method == "GET":
				return render(request, 'admin_personal_login.html')
			elif request.method == "POST":
				personal_id = request.POST["personal_id"]
				personal_password = request.POST["personal_password"]
				passphrase = request.POST["passphrase"]
				login_server = request.POST["login_server"]
				if webmail_login(personal_id, personal_password, login_server):
					logger.info('Admin: %s webmail credentials verified', personal_id)
					user = authenticate(username=personal_id, password=passphrase)
					if user is not None and is_admin(user):
						logger.info('Logging in Admin %s', personal_id)
						login(request, user) # Login as django Admin user
						return redirect('admin_panel')
					else:
						err = 'Invalid passphrase provided'
						logger.info('Admin: %s invalid passphrase', personal_id)
						return render(request, 'admin_personal_login.html', {'error': err})
				else:
					err = 'Invalid credentials for personal webmail id'
					logger.info('Admin: %s invalid personal webmail_id credentials', personal_id)
					return render(request, 'admin_personal_login.html', {'error': err})
		else:
			logger.info('Admin: attempt to forge reference token for election webmail_id login!')
			err = 'Please login with the election webmail id first'
			return render(request, 'admin_login.html', {'error': err})
	else:
		logger.info('Admin: attempt to login directly with personal webmail_id')
		err = 'Please login with the election webmail id first'
		return render(request, 'admin_login.html', {'error': err})

def admin_login_new(request):
	username = request.session.get('mail', None).split('@')[0]
	if request.method == "GET":
		if request.session.get('mail', None):
			return render(request, 'admin_login.html', {"ll_username" : username})
		else: return redirect('index')
	elif request.method == "POST":
		username = request.POST["username"] # Webmail-id
		token = request.POST["token"] # Provided token
		user = authenticate(username=username, password=token)
		if user is not None and is_admin(user):
			logger.info('Logging in Admin %s', username)
			login(request, user) # Login as django Admin user
			return redirect('admin_panel')
		else:
			err = 'Invalid passphrase provided'
			logger.info('Admin: %s invalid passphrase', username)
			return render(request, 'admin_login.html', {'error': err})


def admin_logout(request):
	logger.info('Admin: %s logging out', request.user.username)
	logout(request)
	return redirect('index')

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def create_volunteer(request):
	if request.method == "POST":
		form = VolunteerForm(request.POST)
		url = "/general_elections/create_volunteer/"
		logger.info('Admin: %s posted a create volunteer form', request.user.username)
		if form.is_valid():
			first_name = form.cleaned_data["first_name"]
			last_name = form.cleaned_data["last_name"]
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			try:
				user = User.objects.create_user(
					username=username,
					password=password,
					first_name=first_name,
					last_name=last_name,
					is_active=True,
				)
				msg = "Volunteer successfully created!"
				logger.info('Admin: %s created volunteer with username=%s', request.user.username, username)
			except:
				err = "Volunteer NOT created. User already exists."
				logger.info('Admin: %s volunteer not created as username=%s already exists', request.user.username, username)
				return render(request, 'show_message_and_redirect.html', {'err': err, 'url': url})
			else:
				volunteer = Volunteer.objects.create(user=user)
				return render(request, 'show_message_and_redirect.html', {'msg': msg, 'url': url})
		else:
			return render(request, 'show_message_and_redirect.html', {'form': form, 'url': url})
	else:
		form = VolunteerForm()
	return render(request, 'create_volunteer.html', {'form': form})

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def view_volunteers(request):
	volunteers = list(Volunteer.objects.all())
	return render(request, 'view_volunteers.html', {'volunteers' : volunteers})

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def admin_panel(request):
	return render(request, 'admin_panel.html')

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def voter_list(request):
	logger.info('Admin: %s requested voter list', request.user.username)
	voter_list = VoterList.objects.all()
	hostel_list = VoterList.objects.values('hostel').distinct()

	roll_no = request.GET.get('roll_no')
	hostel = request.GET.get('hostel')
	gender = request.GET.get('gender')
	program = request.GET.get('program')

	if roll_no:
		voter_list = voter_list.filter(roll_no=roll_no)
	else:
		if hostel:
			voter_list = voter_list.filter(hostel=hostel)
		if gender:
			voter_list = voter_list.filter(gender=gender)
		if program:
			voter_list = voter_list.filter(program=program)

	msg = {}
	if not voter_list.exists():
		msg = "No voter found"

	paginator = Paginator(voter_list, 25) # Shows 25 entries in a page

	page_number = request.GET.get('page')
	voters = paginator.get_page(page_number)
	return render(request, 'voter_list.html', {'voters': voters, 'hostel': hostel,'gender': gender,'program': program, 'hostel_list': hostel_list, 'msg': msg})

# Helper function for voting_stats
def create_stats_list(voters_stats, voted_stats):
	result = list()
	for i in voters_stats:
		row = i
		# If field is not present in voted_stats then voted = 0 for that field
		row['voted'] = 0
		for j in voted_stats:
			if j['cat'] == i['cat']:
				row['voted'] = j['voted']
				break
		try:
			row['percentage'] = (row['voted']/row['voters'])*100
		except:
			row['percentage'] = 0
		result.append(row)
	return result

# Display live voting stats to admin
@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def voting_stats(request):
	logger.info('Admin: %s requested voting stats', request.user.username)
	# Each category is a element of dictonary, which contains a list of statistics
	stats = {}
	categories = ['hostel', 'dept', 'program', 'gender']
	for category in categories:
		voters = list(VoterList.objects.values(cat = F(category)).order_by(category).annotate(voters = Count(category)))
		voted = list(VoterList.objects.filter(has_voted = 1).values(cat = F(category)).order_by(category).annotate(voted = Count(category)))
		stats[category] = create_stats_list(voters, voted)
	return render(request, 'voting_stats.html', {'stats': stats,}
													)

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def save_voter(request, webmail_id = ''):
	if request.method == 'POST':
		old_webmail_id = request.session['old_webmail_id']
		voter = VoterList.objects.get(webmail_id=old_webmail_id)
		form = VoterListForm(request.POST, instance = voter)
		url = "/general_elections/voter_list"
		if form.is_valid():
			if not form.cleaned_data['webmail_id'] == old_webmail_id:
				VoterList.objects.get(webmail_id=old_webmail_id).delete()
				logger.info('Admin: %s updated voter with webmail_id=(%s->%s)', request.user.username, old_webmail_id, voter.webmail_id)
			else:
				logger.info('Admin: %s updated voter with webmail_id=%s', request.user.username, voter.webmail_id)
			# print(form)
			form.save(commit=True)
			msg = "Voter details updated."
			return render(request, 'show_message_and_redirect.html', {'msg': msg, 'url': url})
		return render(request, 'show_message_and_redirect.html', {'form': form, 'url': url})
	else:
		logger.info('Admin: %s requested voter update form', request.user.username)
		voter = VoterList.objects.get(webmail_id=webmail_id)
		form = VoterListForm(instance=voter)
		request.session['old_webmail_id'] = webmail_id
		return render(request, 'show_voter_modal.html', {'voter': voter, 'form': form})

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def add_voter(request):
	if request.method == 'POST':
		url = "/general_elections/voter_list"
		msg = "Voters NOT added"
		form = AddVoterForm(request.POST)
		if form.is_valid():
			logger.info('Admin: %s created new voter with webmail_id=%s', request.user.username, form.cleaned_data['webmail_id'])
			form.save(commit=True)
			msg = "Voter added."
		return render(request, 'show_message_and_redirect.html', {'msg': msg, 'url': url})
	else:
		logger.info('Admin: %s requested voter addition form', request.user.username)
		form = AddVoterForm()
		return render(request, 'add_voter_modal.html', {'form': form})


@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def delete_voter(request, webmail_id=""):
	if webmail_id == "":
		msg = "Invalid voter"
	else:
		logger.info('Admin: %s deleted voter with webmail_id=%s', request.user.username, webmail_id)
		VoterList.objects.filter(webmail_id=webmail_id).delete()
		msg = "Voter deleted"
	url = "/general_elections/voter_list"
	return render(request, 'show_message_and_redirect.html', {'msg': msg, 'url': url})

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def add_contestant(request):
	if request.method == 'POST':
		url = "/general_elections/add_contestant/"
		msg = "Contestant NOT added"
		form = AddContestantForm(request.POST, request.FILES)
		if form.is_valid():
			logger.info('Admin: %s created contestant with webmail_id=%s for post=%s', request.user.username,
				form.cleaned_data['webmail_id'], form.cleaned_data['post'])
			form.save(commit=True)
			msg = "Contestant added."
		return render(request, 'show_message_and_redirect.html', {'msg': msg, 'url': url, 'form': form})
	else:
		form = AddContestantForm()
		return render(request, 'add_contestant.html', {'form': form})

def view_contestants(request):
	contestants = list(Contestants.objects.all().order_by('post'))
	return render(request, 'view_contestants.html', {'contestants' : contestants})

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def delete_contestant(request):
	if request.method=="POST":
		url = "/general_elections/delete_contestant/"
		msg = "Contestant NOT found"
		webmail_id = request.POST.get("webmail_id")
		if webmail_id is None:
			return render(request, 'delete_contestant.html')
		try:
			contestant = Contestants.objects.get(webmail_id=webmail_id)
		except ObjectDoesNotExist:
			pass
		else:
			contestant.delete()
			msg = 'Contestant successfully deleted'
		return render(request, 'show_message_and_redirect.html', {'msg': msg, 'url': url})
	else:
		return render(request, 'delete_contestant.html')


@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def get_result2(request, results, index, nthreads):

	# UG VOTES
	temp = dict()
	all_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc', 
						'ugs', 'gs', 'pgs']
	single_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc']
	
	for cat in all_categories:
		temp[cat] = dict()
		conts = Contestants.objects.filter(post=cat.upper())
		for c in conts:
			temp[cat][c.webmail_id] = 0
	
	UGlist = VotesUG.objects.all()
	n = len(UGlist)
	print(index)
	start = index*int(n/nthreads)
	end = (index+1)*int(n/nthreads)
	if index == nthreads-1:
		end = n

	for ii in range(start, end):
		vote = UGlist[ii]
		# single choice votes
		for cat in single_categories:
			conts = Contestants.objects.filter(post=cat.upper())
			vv = getattr(vote, cat)
			# compare against all contestants
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp[cat][c.webmail_id] += 1
					break
				else:
					continue
		# UGS
		conts = Contestants.objects.filter(post='UGS')
		cols = ['ugs_1', 'ugs_2', 'ugs_3', 'ugs_4', 'ugs_5', 'ugs_6', 'ugs_7']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['ugs'][c.webmail_id] += 1
					break
				else:
					continue

		# GS
		conts = Contestants.objects.filter(post='GS')
		cols = ['gs_1', 'gs_2', 'gs_3']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['gs'][c.webmail_id] += 1
					break
				else:
					continue

	PGlist = VotesPG.objects.all()
	n = len(PGlist)
	start = index*int(n/nthreads)
	end = (index+1)*int(n/nthreads)
	if index == nthreads-1:
		end = n
	print(index)
	for ii in range(start, end):
		vote = PGlist[ii]
		# single choice votes
		for cat in single_categories:
			conts = Contestants.objects.filter(post=cat.upper())
			vv = getattr(vote, cat)
			# compare against all contestants
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp[cat][c.webmail_id] += 1
					break
				else:
					continue
		# PGS
		conts = Contestants.objects.filter(post='PGS')
		cols = ['pgs_1', 'pgs_2', 'pgs_3', 'pgs_4', 'pgs_5', 'pgs_6', 'pgs_7']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['pgs'][c.webmail_id] += 1
					break
				else:
					continue

		# GS
		conts = Contestants.objects.filter(post='GS')
		cols = ['gs_1', 'gs_2', 'gs_3']
		for i in cols:
			vv = getattr(vote, i)
			for c in conts:
				if bcrypt.hashpw(c.webmail_id.encode('utf-8'), vv.encode('utf-8')) == vv.encode('utf-8'):
					temp['gs'][c.webmail_id] += 1
					break
				else:
					continue
	results[index] = temp

def combine_results(results):
	results_dict = dict()
	all_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc', 
						'ugs', 'gs', 'pgs']
	single_categories = ['vp', 'hab', 'tech', 'cult', 'welfare', 'sports', 'sail', 'swc']
	
	for cat in all_categories:
		results_dict[cat] = dict()
		conts = Contestants.objects.filter(post=cat.upper())
		for c in conts:
			results_dict[cat][c.webmail_id] = 0
			for temp in results:
				results_dict[cat][c.webmail_id] += temp[cat][c.webmail_id]

	return results_dict

# Final results login and display
ADMINS = ['beingtmk', 'swc']
@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
@cache_control(private=True, no_cache=True, must_revalidate=True)
@never_cache
def results_login(request):
	if request.method == "GET":
		request.session['logins'] = list()
		return render(request, 'results.html')
	elif request.method == "POST":
		webmail_id = request.POST["webmail_username"]
		if webmail_id in ADMINS:
			password = request.POST["webmail_password"]
			login_server = request.POST["login_server"]
			already_logged_in = request.session.get('logins')
			if webmail_id not in already_logged_in: # See if current admin is already logged in once
				prev = request.session.get('prev') # Check if all prev are logged in
				if (prev is not None and Signer().unsign(prev)=='TRUE') or prev is None:
					if webmail_login(webmail_id, password, login_server): # Proceed with current login
						request.session['logins'].append(webmail_id)
						logger.info('Results: %s webmail_id credentials verified', webmail_id)
						if len(request.session.get('logins')) == len(ADMINS):
							s = time.time()
							try:
								pkl_file = open('results.pkl', 'rb')
								results_dict = pickle.load(pkl_file)
								print('Read Pickle')
							except:
								results_dict = dict()
							return render(request, 'results.html', {'results_dict': results_dict})
						else:
							request.session['prev'] = Signer().sign('TRUE')
							return render(request, 'results.html')
					else:
						err = 'Invalid credentials'
						logger.info('Results: %s invalid webmail_id credentials', webmail_id)
						return render(request, 'results.html', {'error': err})
				else:
					err = 'All admin logins required. Please start again.'
					return render(request, 'results.html', {'error': err})
			else:
				err = 'You are already logged in. Please ask other admins to log in'
				return render(request, 'results.html', {'error': err})
		else:
			err = 'This webmail_id is not authorised to access results'
			return render(request, 'results.html', {'error': err})

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def results_logout(request):
	logger.info('Loggging out all admins from results view')
	request.session.pop('logins')
	request.session.pop('prev')
	return redirect('admin_panel')

@login_required(login_url='/general_elections/admin_login/')
@user_passes_test(is_admin)
def bulk_upload(request):
	col_list = VoterListForm.Meta.fields
	if request.method == "GET":
		return render(request, "bulk_upload.html", {'voter_col_list':col_list})
	else:
		msg = ""
		errors = list()
		try:
			csv_file = request.FILES["voters"]
			if not csv_file.name.endswith('.csv'):
				messages.error(request,"File is not CSV type")
				return render(request, "bulk_upload.html")
			#if file is too large, return
			if csv_file.multiple_chunks():
				messages.error(request,"File is too big")
				return render(request, "bulk_upload.html")
			df = pd.read_csv(csv_file, keep_default_na=False)
			data_dict = df.to_dict('records')
			for i in range(len(data_dict)):
				if '' in data_dict[i].values():
					# msg = failed to a create new voter at row=%s due to incomplete/invalid info of that voter', request.user.username, i
					logger.info('Admin: %s failed to a create new voter at row=%s due to incomplete/invalid info of that voter', request.user.username, i)
					messages.error(request,'Voter at row = %s not created. Exception raised' %(i))
				else:
					try:
						form = VoterListForm(data_dict[i])
						if form.is_valid():
							form.save()
							logger.info('Admin: %s created new voter with webmail_id=%s', request.user.username, form.cleaned_data['webmail_id'])
						else:
							logger.info('Admin: %s failed to a create new voter due to incomplete/invalid info of that voter', request.user.username)
							messages.error(request,'Voter at row = %s not created. Exception raised' %(i))
					except Exception as e:
						logger.info('Admin: %s failed to create a new voter due to incomplete/invalid info of that voter', request.user.username)
						messages.error(request,'Voter at row = %s not created. Exception raised' %(i))

		except Exception as e:
			messages.error(request,"Unable to upload file. "+repr(e))
		return render(request, "bulk_upload.html", {'col_list': col_list})
