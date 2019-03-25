from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse

from django.shortcuts import render
from django.urls import reverse
from authentication.authhelper import get_signin_url
import time

# Add import statement to include new function
from authentication.outlookservice import get_me
from authentication.authhelper import get_signin_url, get_token_from_code, get_access_token
from authentication.outlookservice import get_me

import logging
logger = logging.getLogger(__name__)


def home(request):
    redirect_uri = request.build_absolute_uri(
        reverse('authentication:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url + '">Click here to sign in and test outlook OAuth2</a>')


# Add import statement to include new function

def gettoken(request):
  auth_code = request.GET['code']
  logger.info('code: %s', auth_code)
  # redirect_uri = request.build_absolute_uri(reverse('authentication:gettoken'))
  redirect_uri = 'https://swc.iitg.ac.in/general_elections/authentication/gettoken/'

  token = get_token_from_code(auth_code, redirect_uri)
  logger.info('token: %s', token)

  access_token = token['access_token']
  logger.info('access_token: %s', access_token)

  user = get_me(access_token)
  logger.info('user: %s', user)


  # Save the data in session
  request.session['access_token'] = access_token
  request.session['name'] = user['displayName']
  request.session['roll_number'] = user['surname']
  request.session['mail'] = user['mail']

  redirect_url = request.session.get('redirect_url', None)
  save_user = request.session.get('save_user', None)

  logins = request.session.get('logins', None)

  if(logins is None):
    request.session['logins'] = list()

  if(save_user):
    request.session['logins'].append(user['mail'].split('@')[0])
    request.session['save_user'] = None
  
  if redirect_url is None:
    return redirect('index')
  else: 
    request.session['redirect_url'] = None
    return redirect(redirect_url)
