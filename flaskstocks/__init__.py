from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OOooooOOOo'

from flaskstocks import routes
