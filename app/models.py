from . import db
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class User(UserMixin,db.Model):
    """
    Class I will use to create users
    """
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key = True)
    full_name = db.Column(db.String)
    username = db.Column(db.String)
    email = db.Column(db.String)
    bio = db.Column(db.String)
    image = db.Column(db.String)
    posts = db.relationship("Post", backref = "user", lazy = "dynamic")
    user_pass = db.Column(db.String)

    def save_user(self):
        db.session.add(self)
        db.session.commit()
        
    @property
    def password(self):
        raise AttributeError("Gerrarahia")

    @password.setter
    def password(self,password):
        self.user_pass = generate_password_hash(password)

    def verify_pass(self,password):
        return check_password_hash(self.user_pass, password)
    


class Post(db.Model):
    __tablename__ = "posts"
    id  = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    content = db.Column(db.String)
    time = db.Column(db.String)
    image = db.Column(db.String)
    comments = db.relationship("Comment",backref = "post", lazy = "dynamic")
    def get_post_comments(self):
        return Comment.query.filter_by(post_id = self.id)

    def save_post(self):
        db.session.add(self)
        db.session.commit()

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    title = db.Column(db.String)
    content = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    time = db.Column(db.String)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

class Subscriber(db.Model):
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()