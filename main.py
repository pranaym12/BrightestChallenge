# N2S: print statement: #app.logger.error('hello world')

from requests_oauthlib import OAuth2Session 
import requests #pip install requests requests_oauthlib

from flask import Flask, request, redirect, session, url_for #pip install flask
from flask.json import jsonify
import os
from flask import render_template #for Home and About

import logging #also for printing?

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "3BXHKSKAFIL2HZQ7D6"
client_secret = "RDJMSHVG2RRBMPACDMRAQXL4OZ3MXWMU4TW56NK3KDDNHSV5JJ"
redirect_uri = 'http://localhost:5000/callback'
#From Eventbrite documentation
authorization_base_url = 'https://www.eventbrite.com/oauth/authorize'
token_url = 'https://www.eventbrite.com/oauth/token'
refresh_url = token_url #apparently true for Google but not all?

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. eventbrite)
    using an URL with a few key OAuth parameters.
    """
    eventbrite = OAuth2Session(client_id, redirect_uri = redirect_uri) #redirect_uri may not be nec
    authorization_url, state = eventbrite.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state #comm4Pot
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    #STEP 1: get token through post request
    code = request.args.get("code") #right now code gets the code from the URL
    url = "https://www.eventbrite.com/oauth/token"
    payload = "code="+code+"&client_id="+client_id+"&client_secret="+client_secret+"&grant_type=authorization_code"
    headers = {'Content-Type': "application/x-www-form-urlencoded",}
    #make the post request!
    response = requests.request("POST", url, data=payload, headers=headers)

    return str(response.json()["access_token"]) #display the token!

    #STEP 2: redirect to https://www.eventbriteapi.com/v3/users/me/?token=SESXYS4X3FJ5LHZRWGKQ


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    eventbrite = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(eventbrite.get('https://www.eventbriteapi.com/v3/users/me/').json())
    # "query string parameter Include the token on the end of the URL as the token parameter:"


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)