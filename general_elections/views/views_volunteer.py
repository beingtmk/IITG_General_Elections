from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test
from django.core.signing import Signer
import logging

from ..models import *
from .api import webmail_login

logger = logging.getLogger(__name__)

# Custom decorators
def is_voter(user):
	return Voter.objects.filter(user=user).exists()

def is_admin(user):
	return Admin.objects.filter(user=user).exists()

def is_volunteer(user):
	return Volunteer.objects.filter(user=user).exists()

def is_volunteer_or_admin(user):
	return Volunteer.objects.filter(user=user).exists() or Admin.objects.filter(user=user).exists() 


# Views
def volunteer_login(request):
	if request.method == "GET":
		logger.info('Volunteer: login accessed')
		return render(request, "volunteer_login.html")
	elif request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]
		login_server = request.POST["login_server"]
		token = request.POST["token"]
		authenticated = webmail_login(username, password, login_server)
		if authenticated:
			user = authenticate(username=username, password=token)
			if user is not None and is_volunteer(user):
				logger.info('Volunteer: %s logging in', username)
				login(request, user)
				return redirect('volunteer_panel')
			else:
				err = 'Invalid username or token'
				return render(request, 'volunteer_login.html', {'error': err})
		else:
			err = 'Invalid webmail credentials'
			return render(request, 'volunteer_login.html', {'error': err})

def volunteer_logout(request):
	logger.info('Volunteer: %s logging out', request.user.username)
	logout(request)
	return redirect('volunteer_login')

def get_or_none(classmodel, **kwargs):
	try:
		return classmodel.objects.get(**kwargs)
	except ObjectDoesNotExist:
		return None

def volunteer_login_new(request):
	if request.method == "GET":
		if request.session.get('mail', None):
			username = request.session.get('mail', None).split('@')[0]
			return render(request, 'login.html', {"ll_username" : username})
		else: return redirect('index')
	elif request.method == "POST":
		username = request.POST["username"] # Webmail-id
		token = request.POST["token"] # Provided token
		user = authenticate(username=username, password=token)
		if user is not None and is_volunteer(user):
			logger.info('Volunteer: %s logging in', username)
			login(request, user)
			return redirect('volunteer_panel')
		else:
			err = 'Invalid username or token'
			return render(request, 'login.html', {'error': err})



"""
Generate a token for a voter present in the VoterList, and create a django User with username=webmail_id
and password=token.
If User already exists and has voted, then error is displayed.
If User already exists, but has not voted, the password is changed to the new token.
"""
@login_required
@user_passes_test(is_volunteer_or_admin)
def volunteer_panel(request):
	if request.method == 'POST':
		webmail_id = request.POST['webmail_id']
		user = VoterList.objects.filter(webmail_id=webmail_id)
		if not user.exists():
			logger.info('Volunteer: %s attempt to create voter who is not in VoterList', request.user.username)
			err = 'This user does not exist in the voter list. Check the webmail-id entered.\
					Or ask the admin to add them to the voter list.'
		elif user[0].has_voted:
			logger.info('Volunteer: %s attempt to create new token for %s who has already voted', request.user.username, user[0].webmail_id)
			err = 'User has already voted. New token cannot be generated.'
		elif not user[0].course_registeration:
			logger.info('Volunteer: %s token cannot be generated for %s, not course registered', request.user.username, user[0].webmail_id)
			err = 'Voter has not done course registeration, and is not allowed to vote.'
		else:
			user = get_or_none(User, username=webmail_id)
			if not (is_admin(user) or is_volunteer(user)):
				token = User.objects.make_random_password(length=6)
				try:
					u = User.objects.get(username=webmail_id)
					user = Voter.objects.get(user=u)
				except ObjectDoesNotExist:
					user = None
				if user is not None:
					logger.info('Volunteer: %s reset token for %s', request.user.username, u.username)
					u.is_active = True # Make the voter active again
					u.set_password(token) # Only change password
					u.save()
					msg = 'Token for %s was already created. Do you want to create a new token?' %(webmail_id)
				else:
					user = User.objects.create_user(
						username=webmail_id,
						password=token,
						is_active=True,
					)
					voter = Voter.objects.create(user=user)
					voter.save()
					logger.info('Volunteer: %s created token for %s', request.user.username, user.username)
					msg='Voter token successfully created for %s!' %(webmail_id)
				voter = VoterList.objects.get(webmail_id=webmail_id)
				return render(request, 'volunteer_panel.html', {'voter': voter,'msg':msg, 'token':token})
			else:
				try:
					voter = Voter.objects.create(user=user)
					voter.save()
					logger.info('Volunteer: %s admin/volunteer became voter=%s', request.user.username, user.username)
				except:
					pass
				err = 'Admin/Volunteer can now login as voter with their own token'
				return render(request, 'volunteer_panel.html', {'error': err})
		return render(request, 'volunteer_panel.html', {'error': err})
	else:
		return render(request, 'volunteer_panel.html')
