from puppies import app
from flask import render_template, request, make_response, redirect, flash
from flask import session as login_session
import random
import string
import json
import httplib2
import requests
from puppies.functions import createUser, getUserID, getUserInfo

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client import client

fb_client_secrets_file = app.config.get('CLIENT_SECRETS_DIR') + 'fb_client_secrets.json'
g_client_secrets_file = app.config.get('CLIENT_SECRETS_DIR') + 'client_secrets.json'

CLIENT_ID = json.loads(
    open(g_client_secrets_file, 'r').read())['web']['client_id']

@app.route('/session')
def setSessionInfo():
    sessioninfo = login_session._get_current_object()
    response = make_response(
        json.dumps(sessioninfo, 200))
    response.headers['Content-Type'] = 'application/json'
    return response


# Create anti-forgery state token
@app.route('/login')
def initLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/login_fb', methods=['POST'])
def login_fb():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open(fb_client_secrets_file, 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(fb_client_secrets_file, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=40&width=40' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists, if not, create
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    flash("Now logged in as %s" % login_session['username'])
    return 'Success!'


@app.route('/login_g', methods=['POST'])
def login_g():
    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data



    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(g_client_secrets_file, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v2/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    flash("Now logged in as %s" % login_session['username'])
    return 'Success!'


@app.route('/logout')
def logout():
    if 'username' in login_session:
        if login_session['provider'] == 'google':
            access_token = login_session['credentials']
            url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
            h = httplib2.Http()
            result = h.request(url, 'GET')[0]

            if result['status'] == '200':
                # Reset the user's sesson.
                login_session.clear()
                return redirect('/')
            else:
                # For whatever reason, the given token was invalid.
                response = make_response(
                    json.dumps('Failed to revoke token for given user.' + url, 400))
                response.headers['Content-Type'] = 'application/json'
                return response
        if login_session['provider'] == 'facebook':
            facebook_id = login_session['facebook_id']
            # The access token must me included to successfully logout
            access_token = login_session['access_token']
            url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
            h = httplib2.Http()
            result = h.request(url, 'DELETE')[1]
            print result
            if 'success' in result:
                # Reset the user's sesson.
                login_session.clear()
                flash('Logged out')
                return redirect('/')
            else:
                return result
    else:
        return redirect('/')
