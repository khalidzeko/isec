# set up the Blueprint: let the code that there a punch of  routes associated 
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from  flask_login import login_user, login_required, logout_user, current_user 


auth = Blueprint('auth', __name__)

@auth.route('/records')
@login_required
def records():
    return render_template('records.html', user=current_user)

@auth.route('/receipt')
@login_required
def receipt():
    return render_template('receipt.html', user=current_user)

@auth.route('/log-in', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            if (user.password, password):
                flash('Logged in seccessfully!')
                login_user(user, remember=True) # to remember the user untill logout
                return redirect(url_for('view.home'))
            else:
                flash('Invalid Password')
        else:
            flash('Email not found', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    # check:
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('FirstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('user exists, please try another email', category='error')
        elif len(email) < 4:
            flash('email must be al least 4 chars', category='error')
        elif len(fname) < 2:
            flash('first must be al least 2 chars', category='error')
        elif password1 != password2:
            flash('Your passowrd is not match', category='error')
        else:
            new_user = User(email=email, first_name=fname, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True) # to remember the user untill logout
            flash('Account created', category='success')
            return redirect(url_for('view.home'))
            
    #Then go to base.html & make the alert messagaes
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required # login required to logout'make sence'
def logout():
    logout_user() # logout user
    return redirect(url_for('auth.login'))

