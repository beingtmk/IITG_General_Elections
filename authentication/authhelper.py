from urllib.parse import quote, urlencode
import base64
import json
import time
import requests

import logging
logger = logging.getLogger(__name__)

# Client ID and secret
client_id = '2597b493-ebd9-4260-927d-f08b1865cb77'
client_secret = 'XtmswPCAOf8/jmp4rE2nfXfbaP58nA02iPoiucvS7Kc='

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(
    authority, '/850aa78d-94e1-4bc6-9cf3-8c11b530701c/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(
    authority, '/850aa78d-94e1-4bc6-9cf3-8c11b530701c/oauth2/v2.0/token')

# The scopes required by the app
scopes = ['openid',
          'offline_access',
          'User.Read']

proxies = {
    'http': 'http://tusharyadav:merimaa52@202.141.80.20:3128',
    'https': 'http://tusharyadav:merimaa52@202.141.80.20:3128',
    }

def get_signin_url(redirect_uri):
    # Build the query parameters for the signin url
    params = {'client_id': client_id,
              'redirect_uri': redirect_uri,
              'response_type': 'code',
              'scope': ' '.join(str(i) for i in scopes),
              'prompt': 'login'
              }

    signin_url = authorize_url.format(urlencode(params))

    return signin_url


def get_token_from_code(auth_code, redirect_uri):
    logger.info("get_token_from_code accessed!")
    # Build the post form for the token request
    post_data = {'grant_type': 'authorization_code',
                 'code': auth_code,
                 'redirect_uri': redirect_uri,
                 'scope': ' '.join(str(i) for i in scopes),
                 'client_id': client_id,
                 'client_secret': client_secret
                 }

    logger.info(requests.get('https://google.com', proxies=proxies))

    r = requests.post(token_url, data=post_data, proxies=proxies)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_token_from_refresh_token(refresh_token, redirect_uri):
    # Build the post form for the token request
    post_data = {'grant_type': 'refresh_token',
                 'refresh_token': refresh_token,
                 'redirect_uri': redirect_uri,
                 'scope': ' '.join(str(i) for i in scopes),
                 'client_id': client_id,
                 'client_secret': client_secret,
                 }

    r = requests.post(token_url, data=post_data, , proxies=proxies)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_access_token(request, redirect_uri):
    current_token = request.session['access_token']
    expiration = request.session['token_expires']
    now = int(time.time())
    if (current_token and now < expiration):
        # Token still valid
        return current_token
    else:
        # Token expired
        refresh_token = request.session['refresh_token']
        new_tokens = get_token_from_refresh_token(refresh_token, redirect_uri)

        # Update session
        # expires_in is in seconds
        # Get current timestamp (seconds since Unix Epoch) and
        # add expires_in to get expiration time
        # Subtract 5 minutes to allow for clock differences
        expiration = int(time.time()) + new_tokens['expires_in'] - 300

        # Save the token in the session
        request.session['access_token'] = new_tokens['access_token']
        request.session['refresh_token'] = new_tokens['refresh_token']
        request.session['token_expires'] = expiration

        return new_tokens['access_token']
