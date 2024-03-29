from . import auth
from flask import redirect,render_template,url_for
from flask_login import login_user,logout_user
from .forms import RegistrationForm,LoginForm
from ..models import User
from ..email import create_mail

@auth.route("/register", methods = ["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        full_name = form.full_name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user = User(full_name = full_name, password = password,email = email, username = username)
        user.save_user()
        create_mail("Welcome","email/welcome_user",user.email,name = user.full_name)

        return redirect(url_for('auth.login'))

    title = "Register"
    return render_template("auth/register.html", form = form)

@auth.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email = email).first()
        if user is not None and user.verify_pass(form.password.data):
            login_user(user,form.remember.data)
            return redirect(url_for('main.index'))
    title = "Login"
    return render_template("auth/login.html", form = form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))

    @auth.route('/index/')
    def index():
        return render_template("index.html")
