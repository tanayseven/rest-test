import os
from flask import Flask

from rest_test.config import apply_dev_config
from rest_test.extensions import db, jwt, migrate, mail, bcrypt
from rest_test.product.view import products_view
from rest_test.user.user import authenticate, identity
from rest_test.user.view import user_view
from rest_test.view import root_view

app: Flask = Flask(__name__.split('.')[0])

if os.environ.get('APP_ENVIRONMENT').lower() == 'dev':
    apply_dev_config(app)

# Perform migrations on the database
db.init_app(app)
migrate.init_app(app)

# Add handlers for Flask-JWT
jwt.identity_handler(identity)
jwt.authentication_handler(authenticate)
jwt.init_app(app)

mail.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(products_view)
app.register_blueprint(user_view)
app.register_blueprint(root_view)
