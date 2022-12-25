import os
from flask import Flask


app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

# app.secret_key = os.urandom(12)
app.secret_key = 'secret'