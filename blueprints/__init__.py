from blueprints.auth import bp_auth
from blueprints.like.resource import bp_like
from blueprints.cart.resource import bp_cart
from blueprints.book.resource import bp_book
from blueprints.penerbit.resource import bp_penerbit
from blueprints.user.resource import bp_user
import json
import os
from datetime import timedelta
from functools import wraps

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

###########################
# JWT
###########################
app.config['JWT_SECRET_KEY'] = 'njnFTsdiMDni7632jk3lNeu'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# jwt custom decorator
# @jwt.user_claims_loader


def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['internal_status'] != 'internal':
            return {'status': 'FORBIDDEN', 'message': 'Internal Only!'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


#################
# DATABASE
################
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:agungajin19@portofolio.ce1fym8eoinv.ap-southeast-1.rds.amazonaws.com:3306/portofolio_testing'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:agungajin19@portofolio.ce1fym8eoinv.ap-southeast-1.rds.amazonaws.com:3306/portofolio'
except Exception as e:
    raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

###################
# Middlewares
###################


###################
# LOG RESPONSE
###################

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()

    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': request.args.to_dict(),
            'responese': json.loads(response.data.decode('utf-8'))
        })
        )
    else:
        app.logger.error("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': request.args.to_dict(),
            'responese': json.loads(response.data.decode('utf-8'))
        })
        )
    return response

###################
# IMPORT BluePrint
###################


# from blueprints.collection.resource import bp_collection

app.register_blueprint(bp_auth, url_prefix='/user/login')
app.register_blueprint(bp_user, url_prefix='')
app.register_blueprint(bp_penerbit, url_prefix='')
app.register_blueprint(bp_book, url_prefix='')
app.register_blueprint(bp_cart, url_prefix='')
app.register_blueprint(bp_like, url_prefix='')
# app.register_blueprint(bp_collection, url_prefix='')


db.create_all()
