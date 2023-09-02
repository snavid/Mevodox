from flask import Blueprint, render_template, request, flash, redirect, url_for
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from websites import db
from flask_login import login_user, logout_user, login_required


auth = Blueprint("auth", __name__)

regex = re.compile(r'''([a-zA-Z0-9._%+-]+ @[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))''', re.VERBOSE)

@auth.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('passwd')
        print(username, password)
        user = User.query.filter_by(username=username).first()
        mail = User.query.filter_by(email=username).first()
        
        if username == 'admin':
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.admin'))
        elif user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Your Password is incorrect', category='danger')
        elif bool(re.match(regex, username)):
            if mail:
                if check_password_hash(mail.password, password):
                    login_user(mail, remember=True)
                    return redirect(url_for('views.homepage'))
                else:
                    flash('Your Password is incorrect', category='danger')
            else:
                flash('Your email is incorrect', category='danger')
        else:
            flash('Your username is incorrect', category='danger')
    return render_template('login.html')
@auth.route('/SIGN_IN', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('uname')
        email    = request.form.get('email')
        password1 = request.form.get('passwd1')
        password2 = request.form.get('passwd2')
        gender = request.form.get('gender')
        print(username, email, password1, password2, gender)
        user = User.query.filter_by(username=username).first()
        mail = User.query.filter_by(email=email).first()
        if len(username) < 3:
            flash("Username should have more than 3 character", category="danger")
        elif user:
            flash("This username is available", category='danger')    
        else:
            if bool(re.match(regex, email)) == False:
                flash("Email given is invalid", category="danger" )
            elif mail:
                flash("Email provided is in user by another account", category="danger")
            else:
                if password1 != password2:
                    flash('Passwords did not match', category='danger')
                else:
                    user = User(username=username, email=email, password=generate_password_hash(password2, method='scrypt'), gender=int(gender))
                    db.session.add(user)
                    db.session.commit()
                    print("Data successfully stored to the database")
                    login_user(user, remember=True)
                    return redirect(url_for('views.homepage'))
    return render_template('signin.html')



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')







