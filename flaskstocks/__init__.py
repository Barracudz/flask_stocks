from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OOooooOOOo'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # No caching

from flaskstocks import routes
