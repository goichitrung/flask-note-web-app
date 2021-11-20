from flask import Blueprint,render_template,request,flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Sign in successfully",category='success')
                login_user(user,remember = True)
                return redirect(url_for('views.home'))
            else:
                flash("Wrong password",category="error")
        else:
            flash("Incorrect email",category="error")
    return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required # we need to login in order to log out
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email=request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user :
            flash("Email already exists",category='error')
        
        elif (len(email)<10):
            flash('Email is too short', category='error')
        elif (len(firstName)<2):
            flash('First name is too short', category='error')
        elif password1!=password2:
            flash('Password don\'t match', category='error')
        else:
            #add user to db 
            new_user = User(email=email,firstName=firstName,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            login_user(new_user,remember = True)
            return redirect(url_for("views.home"))
    return render_template("sign_up.html",user=current_user)