import base64
import hashlib
import logging
import secrets
import sys
import threading
import urllib
import webbrowser
from time import sleep

import requests
from flask import Flask, render_template, request
from werkzeug.serving import make_server

from suite_py.lib import logger
from suite_py.lib import metrics

# Global vars for comunication between flask thread and main cli function
received_callback = None
code = None
error_message = None
received_state = None

# Global Flask App
app = Flask(__name__, template_folder="templates")
log = logging.getLogger("werkzeug")
log.disabled = True


@app.route("/callback")
def callback():
    """# pylint: disable-next=missing-timeout
    The callback is invoked after a completed login attempt (succesful or otherwise).
    It sets global variables with the auth code or error messages, then sets the
    polling flag received_callback.
    :return:
    """
    global received_callback, code, error_message, received_state
    error_message = None
    code = None
    if "error" in request.args:
        error_message = request.args["error"] + ": " + request.args["error_description"]
    else:
        code = request.args["code"]
    received_state = request.args["state"]
    received_callback = True
    return render_template("login.html")


class ServerThread(threading.Thread):
    """
    The Flask server is done this way to allow shutting down after a single request has been received.
    """

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server("127.0.0.1", 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        # logger.debug('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


class Login:
    def __init__(self, config):

        try:
            if not config.okta["client_id"] or not config.okta["base_url"]:
                self.usage()
                sys.exit(-1)
        except AttributeError:
            self.usage()
            sys.exit(-1)

        self._config = config
        self.okta_client_id = config.okta["client_id"]
        self.base_url = config.okta["base_url"]
        self.okta_scope = "openid"
        self.redirect_uri = "http://127.0.0.1:5000/callback"

    def usage(self):
        logger.warning("Unable to login: missing config")
        logger.warning(
            "please check docs: https://github.com/primait/suite_py/blob/master/README.md"
        )

    def url_encode_no_padding(self, byte_data):
        """
        Safe encoding handles + and /, and also replace = with nothing
        :param byte_data:
        :return:
        """
        return base64.urlsafe_b64encode(byte_data).decode("utf-8").replace("=", "")

    def generate_challenge(self, a_verifier):
        return self.url_encode_no_padding(hashlib.sha256(a_verifier.encode()).digest())

    @metrics.command("login")
    def run(self):
        global received_callback

        # from https://auth0.com/docs/flows/add-login-using-the-authorization-code-flow-with-pkce
        # Step1: Create code verifier: Generate a code_verifier that will be sent to Auth0 to request tokens.
        verifier = self.url_encode_no_padding(secrets.token_bytes(32))
        # Step2: Create code challenge: Generate a code_challenge from the code_verifier that will be sent to Auth0 to request an authorization_code.
        challenge = self.generate_challenge(verifier)
        state = self.url_encode_no_padding(secrets.token_bytes(32))
        client_id = self.okta_client_id
        base_url = self.base_url
        scope = self.okta_scope
        redirect_uri = self.redirect_uri
        #
        # We generate a nonce (state) that is used to protect against attackers invoking the callback
        url = f"{base_url}/authorize?"
        url_parameters = {
            "scope": scope,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_challenge": challenge.replace("=", ""),
            "code_challenge_method": "S256",
            "state": state,
        }
        url = url + urllib.parse.urlencode(url_parameters)

        # Step3: Authorize user: Request the user's authorization and redirect back to your app with an authorization_code.
        # Open the browser window to the login url
        # Start the server
        # Poll til the callback has been invoked
        received_callback = False
        logger.info(
            "A browser tab should've opened. If not manually navigate to: " + url
        )
        webbrowser.open(url)
        server = ServerThread(app)
        server.start()
        while not received_callback:
            sleep(1)
        server.shutdown()

        if state != received_state:
            logger.error(
                "Error: session replay or similar attack in progress. Please log out of all connections."
            )
            sys.exit(1)

        if error_message:
            logger.error("An error occurred:")
            logger.error(error_message)
            sys.exit(1)

        # Step4: Request tokens: Exchange your authorization_code and code_verifier for tokens.
        url = f"{base_url}/token"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        body = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code_verifier": verifier,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        # pylint: disable-next=missing-timeout
        r = requests.post(url, headers=headers, data=body)
        data = r.json()
        logger.debug(data)
        if "id_token" in data:
            token = str(data["id_token"])
        else:
            logger.error("id_token not found in okta response")
            sys.exit(1)
        logger.info("login succeded")
        self._config.put_cache(f"{base_url}_token", token)
