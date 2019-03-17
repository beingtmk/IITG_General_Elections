from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authentication.authhelper import get_signin_url
import time

# Add import statement to include new function
from authentication.outlookservice import get_me
from authentication.authhelper import get_signin_url, get_token_from_code, get_access_token
from authentication.outlookservice import get_me

def home(request):
    redirect_uri = request.build_absolute_uri(
        reverse('authentication:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url + '">Click here to sign in and test outlook OAuth2</a>')


# Add import statement to include new function

def gettoken(request):
  auth_code = request.GET['code']
  redirect_uri = request.build_absolute_uri(reverse('authentication:gettoken'))
  token = get_token_from_code(auth_code, redirect_uri)
  access_token = token['access_token']
  user = get_me(access_token)

  # Save the token in the session
  request.session['access_token'] = access_token
  return HttpResponse('User: {0}, Access token: {1}'.format(user, access_token))