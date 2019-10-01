from . import main
from flask_login import current_user, login_required
from .forms import AddPostForm,SubscribeForm,AddComment,EditBio
from ..models import Post,User,Comment,Subscriber
from flask import redirect,url_for,render_template,flash,request
from .. import db,photos
from datetime import datetime
from app.email import create_mail

@main.route("/", methods = ["GET","POST"])
def index():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        new_subscriber = Subscriber(email = email)
        db.session.add(new_subscriber)
        db.session.commit()
        flash("Thank You for subscribing!")
        return redirect(url_for("main.index"))
    posts = Post.query.order_by(Post.time.desc())
    title = "Home"
    return render_template("index.html",posts = posts,form = form,title = title)

@main.route("/add/post/",methods = ["GET","POST"])
@login_required
def add_post():
    form = AddPostForm()
    title = "Add Post"


    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        posted = str(datetime.now())
        print(posted)
        if "photo" in request.files:
            pic = photos.save(request.files["photo"])
            file_path = f"photos/{pic}"
            image = file_path
        new_post = Post(title = title, content = content, user = current_user,image = image,time = posted)
        new_post.save_post()
        subscribers = Subscriber.query.all()
        emails = []
        for subscriber in subscribers:
            emails.append(subscriber.email)
        for email in emails:
            create_mail("Update!","email/update",email, user = current_user)
        print(emails)
        return redirect(url_for('main.index'))

    return render_template("add_pitch.html",form = form,title = title)

@main.route("/post/<int:id>",methods = ["GET","POST"])
def post_page(id):
    post = Post.query.filter_by(id = id).first()
    title = post.title
    form = AddComment()
    if form.validate_on_submit():
        name = form.name.data
        content = form.comment.data
        new_comment = Comment(name = name, content = content, post = post)
        new_comment.save_comment()
        return redirect(url_for('main.post_page', id = post.id))
    comments = Comment.query.filter_by(post_id = post.id)
    title = post.title
    return render_template("post.html", title = title, post = post,form = form,comments = comments)

@main.route("/delete/<id>")
def delete(id):
    post = Post.query.filter_by(id = id).first()
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('main.profile', id = user_id))

@main.route("/delete/comment/<id>")
def delete_comment(id):
    comment = Comment.query.filter_by(id = id).first()
    post_id = comment.post.id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("main.post_page", id = post_id))

@main.route("/profile/<id>")
def profile(id):
    user = User.query.filter_by(id = id).first()
    posts = Post.query.filter_by(user_id = user.id).order_by(Post.time.desc())
    title = user.full_name
    return render_template("profile.html", user = user,posts = posts, title = title)

@main.route("/<user_id>/profile/edit",methods = ["GET","POST"])
@login_required
def update_profile(user_id):
    title = "Edit Profile"
    user = User.query.filter_by(id = user_id).first()
    form = EditBio()

    if form.validate_on_submit():
        bio = form.bio.data
        user.bio = bio
        db.session.commit() 
        return redirect(url_for('main.profile',id = user.id)) 
    return render_template("update_profile.html",form = form,title = title)

@main.route("/pic/<user_id>/update", methods = ["POST"])
@login_required
def update_pic(user_id):
    user = User.query.filter_by(id = user_id).first()
    title = "Edit Profile"
    if "profile-pic" in request.files:
        pic = photos.save(request.files["profile-pic"])
        file_path = f"photos/{pic}"
        user.image = file_path
        db.session.commit()
    return redirect(url_for("main.profile", id = user.id))
