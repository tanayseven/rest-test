from types import MethodType

import os
import pytest
from flask import json
from flask.testing import FlaskClient

from rest_test.app import app
from rest_test.extensions import db, mail


def _post_json(self, url: str = '/', body=None, headers=None):
    headers = {} if headers is None else headers
    body = {} if body is None else body
    return self.post(
        url,
        data=json.dumps(body),
        content_type='application/json',
        headers=headers,
    )


class DatabaseTest:
    @pytest.fixture(autouse=True)
    def database_setup(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TEST_DATABASE_URI')
        self._ctx = app.test_request_context()
        self._ctx.push()
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield
        if hasattr(self, '_ctx'):
            self._ctx.pop()


class ApiTestBase(DatabaseTest):
    @staticmethod
    def create_app() -> FlaskClient:
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        with app.app_context():
            return app.test_client()

    @staticmethod
    def create_outbox():
        with mail.record_messages() as outbox:
            return outbox

    @pytest.fixture(autouse=True)
    def api_setup(self):
        self.app_test = self.create_app()
        self.mail_outbox = self.create_outbox()
        self.app_test.post()
        self.app_test.post_json = MethodType(_post_json, self.app_test)
