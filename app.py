import datetime

from flask import Flask

import flask_admin as admin
from flask_mongoengine import MongoEngine
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = {
    'DB': 'shikhar',
    'host' : 'edunutssearch-1.edunuts.7319.mongodbdns.com',
    'port' : 27000
}

# Create models
db = MongoEngine()
db.init_app(app)


# Define mongoengine documents

class Content(db.EmbeddedDocument):
    title = db.StringField()
    intro = db.StringField()
    mustknow = db.ListField(db.StringField())
    youlldo = db.ListField(db.StringField())
    qualifications = db.StringField()
    positions = db.IntField()
    tags = db.ReferenceField('Tag')

class Engineering(db.Document):
    #positions = db.StringField(max_length = 50)
    Openings = db.EmbeddedDocumentField(Content)


class User(db.Document):
    name = db.StringField(max_length=40)
    tags = db.ListField(db.ReferenceField('Tag'))
    password = db.StringField(max_length=40)

    def __unicode__(self):
        return self.name


# class Todo(db.Document):
#     title = db.StringField(max_length=60)
#     text = db.StringField()
#     done = db.BooleanField(default=False)
#     pub_date = db.DateTimeField(default=datetime.datetime.now)
#     user = db.ReferenceField(User, required=False)

#     # Required for administrative interface
#     def __unicode__(self):
#         return self.title


class Tag(db.Document):
    name = db.StringField(max_length=10)

    def __unicode__(self):
        return self.name


# Customized admin views
class UserView(ModelView):
    column_filters = ['name']

    column_searchable_list = ('name', 'password')

    form_ajax_refs = {
        'tags': {
            'fields': ('name',)
        }
    }


class TodoView(ModelView):
    column_filters = ['done']

    form_ajax_refs = {
        'user': {
            'fields': ['name']
        }
    }


class PostView(ModelView):
    form_subdocuments = {
        'inner': {
            'form_subdocuments': {
                None: {
                    # Add <hr> at the end of the form
                    'form_rules': ('name', 'tag', 'value', rules.HTML('<hr>')),
                    'form_widget_args': {
                        'name': {
                            'style': 'color: red'
                        }
                    }
                }
            }
        }
    }

class EngineeringView(ModelView):
    form_ajax_refs = {
        'tags' : {
            'fields' : ['name']
        }
    }

# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    # Create admin
    admin = admin.Admin(app, 'Example: MongoEngine')

    # Add views
    admin.add_view(UserView(User))
    admin.add_view(ModelView(Tag))
    admin.add_view(ModelView(Engineering))
    # Start app
    app.run(debug=True)