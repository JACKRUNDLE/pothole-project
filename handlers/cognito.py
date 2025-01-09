from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
 
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_z86Hyz3oe',
  client_id='7f8llgjj0kao7q2m8s20qcsijh',
  client_secret='<client secret>',
  server_metadata_url='https://cognito-idp.us-west-2.amazonaws.com/us-west-2_z86Hyz3oe/.well-known/openid-configuration',
  client_kwargs={'scope': 'phone openid email'}
)