from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pandas
from fileinput import filename
 

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password!', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
         # Set session variables for the logged-in user
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be more than 4 characters.', category='error')
        elif len(password1) < 3:
            flash('Password must be more than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords are not the same.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)
   
@auth.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        username = session['username']
        # Retrieve user data from the database
        mycursor = mydb.cursor()
        sql = "SELECT * FROM users WHERE user_id = %s"
        val = (user_id,)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()
        # Display personalized content on the home page
        return render_template('home.html', user=user)
    else:
        # Redirect user to the login page
        return redirect('/')

 
