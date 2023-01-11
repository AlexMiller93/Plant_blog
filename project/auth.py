from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Oops .. Email does not exist.', category='error')
        
        # flash(error)
    
    return render_template("auth/login.html", user=current_user)
    # return render_template("auth/login.html")



@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        # nickname = request.form.get("nickname")
        
        # Todo 
        # make logic if checkbox was pressed, input nickname will be vanished
        # if 
        
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        # checking inputs
        # """
        
        if email_exists:
            flash('Oops... User is already in use with current email.', category='error')
        elif username_exists:
            flash('Hmm... User is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        # elif len(nickname) < 2:
        #     flash('Nickname is too short.' , category='error')
        # elif not 8 <= len(password1) <= 20:
        #     flash('Password should have at least 8 chars but no bigger than 20 chars.', category='error') 
        elif len(email) < 6:
            flash('Email is invalid.', category='error')
        elif len(password1) < 5:
            flash('Password is too short.' , category='error')

        # Todo 
        # add some simple regex to validate password and email
        
        # if all checks were passed -> create new_user and save into database
        

        else:
            new_user = User(
                username=username, 
                # nickname=nickname, 
                email=email,
                password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            # login_user(new_user, remember=True)
            flash('Account created!', category='success')
        # """
        
            return redirect(url_for('views.home'))

        
    return render_template("auth/register.html", user=current_user)
    # return render_template("auth/register.html")





@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))



# print(f'Username: {username}, {type(username)}')
# print(f'Nickname: {nickname}, {type(nickname)}')
# print(f'Email: {email}, {type(email)}')
# print(f'Password1: {password1}, {type(password1)}')
# print(f'Password2: {password2}, {type(password2)}')