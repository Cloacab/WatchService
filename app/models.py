from app import db


class Covid_model(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    body = db.Column(db.String)
    status = db.Column(db.Integer)

    def __init__(self, date, body, status):
        self.date = date
        self.body = body
        self.status = status


class Currency_model(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime)
    body = db.Column(db.String)
    status = db.Column(db.Integer)

    def __init__(self, date, body, status):
        self.date = date
        self.body = body
        self.status = status
