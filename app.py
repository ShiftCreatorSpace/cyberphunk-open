import os

import jwt
from flask import Flask, send_file, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, text, Integer

from config import config_by_name

# Initialize flask with configuration & static folder
app = Flask(__name__, static_url_path='', static_folder='public', )
app.config.from_object(config_by_name[os.environ.get('FLASK_ENV', 'default')])

# Initialize sqlalchemy (db URL comes is in configuration)
db = SQLAlchemy()
db.init_app(app)


class OverlordPasscodes(db.Model):
    __tablename__ = 'overlord_passcodes'

    code = Column(Integer, nullable=False, primary_key=True)


@app.route('/')
def home():
    return send_file('views/index.html')


@app.route('/cpanel')
def cpanel():
    # TODO: the intern wrote the jwt code so we should double check this
    token = request.cookies.get('jwt')

    if token is not None:
        auth = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])

        if auth['role'] == 'overlord':
            return send_file('views/cpanel.html')

    return send_file('views/unauthorized.html')


@app.route('/stopEndOfWorld', methods=['POST'])
def stop():
    # TODO: the intern also wrote this
    test = db.session.query(OverlordPasscodes).filter(text("code={}".format(request.form['code']))).first()

    if test is not None:
        return send_file('views/end.html')

    return send_file('views/oops.html')
