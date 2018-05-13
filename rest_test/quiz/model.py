from enum import Enum

from rest_test.extensions import db


class CandidateStatus(Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'


class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)
    token = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(64))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
