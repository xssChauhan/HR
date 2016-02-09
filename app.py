import datetime

from flask import Flask, Response, json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
import flask_admin as admin
from flask_mongoengine import MongoEngine
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView
from flask.ext.script import Manager

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/edunuts_beta'

# Create models
db = SQLAlchemy(app)

# Define mongoengine documents
manager = Manager(app)

class Openings(db.Model):
    __tablename__ = 'openings'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    openings = db.Column(db.Integer)

    def __str__(self):
        return self.name

class Positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    positions = db.Column(db.String)
    intro = db.Column(db.String)
    mustknow = db.Column(db.String)
    qualifications = db.Column(db.String)
    youlldo = db.Column(db.String)
    tags = db.Column(db.String)
    opening_id = db.Column(db.ForeignKey('openings.id'))
    opening = db.relationship(Openings, backref = 'positions')

    def __str__(self):
        return self.title


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, name='Kya baat!', template_mode='bootstrap3')

    # Add views
    admin.add_view(sqla.ModelView(Positions, db.session))
    admin.add_view(sqla.ModelView(Openings, db.session))
    # Start app
    #app.run(debug=True)
    manager.run()