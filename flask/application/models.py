from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from application import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.String(30), primary_key=True)
    email = db.Column(db.String(60), index=True, unique=False)
    password_hash = db.Column(db.String(128), index=True, unique=False)
    phone = db.Column(db.String(15), index=True, unique=False)
    isAdmin = db.Column(db.Boolean, index=True, unique=False, default=False)
    
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __init__(self, user_id, email, password, phone):
        self.user_id = user_id
        self.email = email
        self.password= password
        self.phone = phone
        
    def __repr__(self):

        return '<User %r>' % self.user_id   
        
    def get_id(self):
        return unicode(self.user_id)     

class User_community(db.Model):
    __tablename__ = 'User_community'

    user_id = db.Column(db.String(30), primary_key=True)
    community_id = db.Column(db.String(30), primary_key=True)

    def __init__(self, user_id, community_id):
        self.user_id = user_id
        self.community_id = community_id
        
    def __repr__(self):

        return '<User_community %r>' % self.user_id
        
class Community(db.Model):
    __tablename__ = 'Community'

    community_id = db.Column(db.String(30), primary_key=True)
    community_description = db.Column(db.String(1000), index=True, unique=False)

    def __init__(self, community_id, community_description):
        self.community_id = community_id
        self.community_description = community_description
        
    def __repr__(self):

        return '<Community %r>' % self.community_id

class Post(db.Model):
    __tablename__ = 'Post'

    post_id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.String(30), index=True, unique=False)
    poster_id = db.Column(db.String(30), index=True, unique=False)
    content = db.Column(db.String(2000), index=True, unique=False)
    title = db.Column(db.String(50), index=True, unique=False)

    def __init__(self, post_id, community_id, poster_id, content, title):
        self.post_id = post_id
        self.community_id = community_id
        self.poster_id = poster_id
        self.content = content
        self.title = title
        
    def __repr__(self):

        return '<Post %r>' % self.post_id
        
class Moderator_community(db.Model):
    __tablename__ = 'Moderator_community'

    community_id = db.Column(db.String(30), primary_key=True)
    moderator = db.Column(db.String(30), primary_key=True)

    def __init__(self, community_id, moderator):
        self.community_id = community_id
        self.moderator = moderator
        
    def __repr__(self):

        return '<Moderator_community %r>' % self.community_id
        
class Task(db.Model):
    __tablename__ = 'Task'

    task_id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.String(30), index=True, unique=False)
    owner = db.Column(db.String(30), index=True, unique=False)
    task_name = db.Column(db.String(50), index=True, unique=False)

    def __init__(self, task_id, community_id, owner, task_name):
        self.task_id = task_id
        self.community_id = community_id
        self.owner = owner
        self.task_name = task_name
        
    def __repr__(self):

        return '<Task %r>' % self.task_id
        
class Task_request(db.Model):
    __tablename__ = 'Task_request'

    request_id = db.Column(db.Integer, primary_key=True)
    requestor_id = db.Column(db.String(30), index=True, unique=False)
    task_id = db.Column(db.Integer, index=True, unique=False)
    status = db.Column(db.String(30), index=True, unique=False)

    def __init__(self, request_id, requestor_id, task_id, status):
        self.request_id = request_id
        self.requestor_id = requestor_id
        self.task_id = task_id
        self.status = status
        
    def __repr__(self):

        return '<Task_request %r>' % self.request_id