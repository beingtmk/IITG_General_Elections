from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.core.signing import Signer
from django.utils.decorators import method_decorator
from formtools.wizard.views import SessionWizardView
from datetime import datetime, timedelta, timezone
import bcrypt
import logging

from ..models import *
from .api import webmail_login
from ..forms import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Custom decorators
def is_voter(user):
	return Voter.objects.filter(user=user).exists()

def is_admin(user):
	return Admin.objects.filter(user=user).exists()

def is_volunteer(user):
	return Volunteer.objects.filter(user=user).exists()

# Views
def voter_login(request):
	if request.method == "GET":
		if request.session.get('mail', None):
			username = request.session.get('mail', None).split('@')[0]
			return render(request, 'login.html', {"ll_username" : username})
		else: return redirect('index')
	elif request.method == "POST":
		username = request.POST["username"] # Webmail-id
		token = request.POST["token"] # Provided token
		# authenticated = webmail_login(username, password, login_server)
		authenticated = True
		if authenticated:
			user = authenticate(username=username, password=token)
			if user is not None and is_voter(user):
				u = VoterList.objects.get(webmail_id=user.username)
				# Check if has voted
				if u.has_voted:
					logger.info('Voter: %s already voted tried logging in again', u.webmail_id)
					err = 'Your vote is already recorded.'
					return render(request, 'login.html', {'error': err})
				logger.info('Voter: %s logged in', u.webmail_id)
				login(request, user)
				# Set voting start time just before redirecting
				u.voting_start = datetime.now(timezone.utc)
				u.save()
				return redirect('voting_start')
			else:
				logger.info('Voter: %s invalid token', username)
				err = 'Invalid token'
				return render(request, 'login.html', {'error': err})
		else:
			logger.info('Voter: %s invalid webmail_id credentials', username)
			err = 'Invalid webmail credentials'
			return render(request, 'login.html', {'error': err})


def voter_logout(request):
	if not (is_admin(request.user) or is_volunteer(request.user)):
		logger.info('Voter: %s setting inactive. vote complete.', request.user.username)
		request.user.is_active = False # Deactivate this user if he's only a voter
	request.user.save()
	logger.info('Voter: %s logged out.', request.user.username)
	logout(request)
	return redirect('index')

def show_girls_senators(user):
	u = VoterList.objects.get(webmail_id=user.username)
	if u.gender == 'F':
		return True
	return False

def show_pg_senators(user):
	u = VoterList.objects.get(webmail_id=user.username)
	if u.program == 'PG':
		return True
	return False

def show_ug_senators(user):
	u = VoterList.objects.get(webmail_id=user.username)
	if u.program == 'UG':
		return True
	return False

def save_data(request, vote_dict):
	logger.info('Voter: %s saving vote', request.user.username)
	u = VoterList.objects.get(webmail_id=(str(request.user)))
	salt = bcrypt.gensalt()
	votes = dict()
	votes['vp']=bcrypt.hashpw(vote_dict['vp'].encode('utf-8'), salt)
	votes['hab']=bcrypt.hashpw(vote_dict['hab'].encode('utf-8'), salt)
	votes['tech']=bcrypt.hashpw(vote_dict['tech'].encode('utf-8'), salt)
	votes['cult']=bcrypt.hashpw(vote_dict['cult'].encode('utf-8'), salt)
	votes['welfare']=bcrypt.hashpw(vote_dict['welfare'].encode('utf-8'), salt)
	votes['sports']=bcrypt.hashpw(vote_dict['sports'].encode('utf-8'), salt)
	votes['sail']=bcrypt.hashpw(vote_dict['sail'].encode('utf-8'), salt)
	votes['swc']=bcrypt.hashpw(vote_dict['swc'].encode('utf-8'), salt)

	vote_list = list()
	if u.gender == 'F':
		flag_gs = 0
		if 'nota_gs' in vote_dict['gs']:
			flag_gs = 1
			vote_list = ['nota_gs', '', '']
		else:
			for i in vote_dict['gs']:
				vote_list.append(i)
			for j in range(3-len(vote_dict['gs'])):
				vote_list.append('')
		votes['gs_1'] = bcrypt.hashpw(vote_list[0].encode('utf-8'), salt)
		votes['gs_2'] = bcrypt.hashpw(vote_list[1].encode('utf-8'), salt)
		votes['gs_3'] = bcrypt.hashpw(vote_list[2].encode('utf-8'), salt)
	else:
		# For male candidate, sign an empty string for gs senator
		empty_unicode = ''.encode('utf-8')
		votes['gs_1']=bcrypt.hashpw(empty_unicode, salt)
		votes['gs_2']=bcrypt.hashpw(empty_unicode, salt)
		votes['gs_3']=bcrypt.hashpw(empty_unicode, salt)

	vote_list = list()
	if u.program == 'UG':
		flag_ugs = 0
		if 'nota_ugs' in vote_dict['ugs']:
			flag_ugs = 1
			vote_list = ['nota_ugs', '', '', '', '', '', '']
		else:
			for i in vote_dict['ugs']:
				vote_list.append(i)
			for j in range(7-len(vote_dict['ugs'])):
				vote_list.append('')
		votes['ugs_1']=bcrypt.hashpw(vote_list[0].encode('utf-8'), salt)
		votes['ugs_2']=bcrypt.hashpw(vote_list[1].encode('utf-8'), salt)
		votes['ugs_3']=bcrypt.hashpw(vote_list[2].encode('utf-8'), salt)
		votes['ugs_4']=bcrypt.hashpw(vote_list[3].encode('utf-8'), salt)
		votes['ugs_5']=bcrypt.hashpw(vote_list[4].encode('utf-8'), salt)
		votes['ugs_6']=bcrypt.hashpw(vote_list[5].encode('utf-8'), salt)
		votes['ugs_7']=bcrypt.hashpw(vote_list[6].encode('utf-8'), salt)
	else:
		flag_pgs = 0
		if 'nota_pgs' in vote_dict['pgs']:
			flag_pgs = 1
			vote_list = ['nota_pgs', '', '', '', '', '', '']
		else:
			for i in vote_dict['pgs']:
				vote_list.append(i)
			for j in range(7-len(vote_dict['pgs'])):
				vote_list.append('')
		votes['pgs_1']=bcrypt.hashpw(vote_list[0].encode('utf-8'), salt)
		votes['pgs_2']=bcrypt.hashpw(vote_list[1].encode('utf-8'), salt)
		votes['pgs_3']=bcrypt.hashpw(vote_list[2].encode('utf-8'), salt)
		votes['pgs_4']=bcrypt.hashpw(vote_list[3].encode('utf-8'), salt)
		votes['pgs_5']=bcrypt.hashpw(vote_list[4].encode('utf-8'), salt)
		votes['pgs_6']=bcrypt.hashpw(vote_list[5].encode('utf-8'), salt)
		votes['pgs_7']=bcrypt.hashpw(vote_list[5].encode('utf-8'), salt)
	votes['webmail_id'] = u.webmail_id
	votes['voting_start'] = u.voting_start
	votes['voting_end'] = u.voting_end

	# String -> Bytes : s.encode('utf-8')
	# Bytes -> String : s.decode('utf-8')
	# Decode all inputs to string before saving to db
	# Encode all the read values when comparing hash to get results
	skip_keys = ['webmail_id', 'voting_start', 'voting_end']
	for k,v in votes.items():
		if k not in skip_keys:
			votes[k] = v.decode('utf-8')
	if u.program == 'UG':
		m = VotesUG(**votes)
	else:
		m = VotesPG(**votes)
	u.has_voted = True
	u.save()
	m.save()
	logger.info('Voter: %s saved vote successfully', request.user.username)

FORMS = [
	('vp', VoteVP),
	('hab', VoteHAB),
	('tech', VoteTECH),
	('cult', VoteCULT),
	('welfare', VoteWELFARE),
	('sports', VoteSPORTS),
	('sail', VoteSAIL),
	('swc', VoteSWC),
	('gs', VoteGS),
	('ugs', VoteUGS),
	('pgs', VotePGS),
]

TEMPLATES = {
	'vp': "voting.html",
	'hab': "voting.html",
	'tech': "voting.html",
	'cult': "voting.html",
	'welfare': "voting.html",
	'sports': "voting.html",
	'sail': "voting.html",
	'swc': "voting.html",
	'gs': "voting_multiple.html",
	'ugs': "voting_multiple.html",
	'pgs': "voting_multiple.html",
}

POST_NAMES = {
	'vp': "Vice President",
	'hab': "General Secretary - Hostel Affairs Board",
	'tech': "General Secretary - Technical Board",
	'cult': "General Secretary - Cultural Board",
	'welfare': "General Secretary - Students Welfare Board",
	'sports': "General Secretary - Sports Board",
	'sail': "General Secretary - SAIL",
	'swc': "General Secretary - SWC",
	'gs': "Girl Senators",
	'ugs': "Under Graduate Senators",
	'pgs': "Post Graduate Senators",
}

class VoteWizard(SessionWizardView):
	form_list = FORMS
	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	condition_dict = {'gs':lambda w: show_girls_senators(w.request.user),
	'pgs':lambda w: show_pg_senators(w.request.user),
	'ugs':lambda w: show_ug_senators(w.request.user),
	}

	def get_context_data(self, form, **kwargs):
		context = super(VoteWizard, self).get_context_data(form=form, **kwargs)
		context.update({'post_name': POST_NAMES[self.steps.current]})
		u = VoterList.objects.get(webmail_id=str(self.request.user))
		time_remaining = (u.voting_start + timedelta(seconds=300) - datetime.now(timezone.utc)).seconds
		context.update({'time_remaining': time_remaining})
		if self.steps.current == 'gs':
			context.update({'target_count': 3})
		elif self.steps.current == 'ugs':
			context.update({'target_count': 7})
		elif self.steps.current == 'pgs':
			context.update({'target_count': 7})
		return context

	def done(self, form_list, form_dict, **kwargs):
		# Set voting end time
		logger.info('Voter: %s completed voting', self.request.user.username)
		u = VoterList.objects.get(webmail_id=str(self.request.user))
		u.voting_end = datetime.now()
		u.save()
		vote_dict = dict()
		vote_dict['vp'] = form_dict['vp'].cleaned_data.get('contestants').webmail_id
		vote_dict['hab'] = form_dict['hab'].cleaned_data.get('contestants').webmail_id
		vote_dict['tech'] = form_dict['tech'].cleaned_data.get('contestants').webmail_id
		vote_dict['cult'] = form_dict['cult'].cleaned_data.get('contestants').webmail_id
		vote_dict['welfare'] = form_dict['welfare'].cleaned_data.get('contestants').webmail_id
		vote_dict['sports'] = form_dict['sports'].cleaned_data.get('contestants').webmail_id
		vote_dict['sail'] = form_dict['sail'].cleaned_data.get('contestants').webmail_id
		vote_dict['swc'] = form_dict['swc'].cleaned_data.get('contestants').webmail_id
		if 'gs' in form_dict:
			# If NOTA candidate is selected, only one element is returned in cleaned data
			l = list()
			for c in form_dict['gs'].cleaned_data['contestants']:
				l.append(c.webmail_id)
			vote_dict['gs'] = l
		if 'ugs' in form_dict:
			l = list()
			for c in form_dict['ugs'].cleaned_data['contestants']:
				l.append(c.webmail_id)
			vote_dict['ugs'] = l
		else:
			l = list()
			for c in form_dict['pgs'].cleaned_data['contestants']:
				l.append(c.webmail_id)
			vote_dict['pgs'] = l
		save_data(self.request, vote_dict)
		logger.info('Voter: %s logged out', self.request.user.username)
		messages.success(self.request,'%s, Your Vote has been recorded!' %self.request.user.username)

		return redirect('logout')
