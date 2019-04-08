from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os
from flask import render_template #for Home and About

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "3BXHKSKAFIL2HZQ7D6"
client_secret = "RDJMSHVG2RRBMPACDMRAQXL4OZ3MXWMU4TW56NK3KDDNHSV5JJ"
authorization_base_url = 'https://www.eventbrite.com/oauth/authorize'
token_url = 'https://www.eventbrite.com/oauth/token'

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
    eventbrite = OAuth2Session(client_id)
    authorization_url, state = eventbrite.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    # session['oauth_state'] = state #comm4Pot
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    # eventbrite = OAuth2Session(client_id, state=session['oauth_state']) #comm4Pot
    eventbrite = OAuth2Session(client_id)

    token = eventbrite.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile')) #this was in the copypasta


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