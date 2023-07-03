from qbank import db, secretKey
from flask import Flask, Blueprint, request, render_template, redirect, flash, url_for, jsonify, Response, \
    make_response, session

# application modules
from qbank.schema import Category, Skill, Question, Question_type, QuestionSchemaUpdateCreate, User, Roles
import jwt
from functools import wraps
import datetime
from sqlalchemy import func

login = Blueprint('login', __name__)
algorithms = ['HS256']

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' in session:
            token = session['token']
            if not token:
                flash("Session Timeout.Please login to Continue", "danger")
                return redirect(url_for('login.loginUser'))
            else:
                try:
                    data = jwt.decode(token, secretKey, algorithms=algorithms)
                    current_user = User.query.filter_by(email=data['email']).first()
                    # role=db.session.query(User,Roles).filter_by(email=current_user.email).outerjoin(Roles,User.id==Roles.user_id).first()
                    user_role = session['role']
                except:
                    flash("Session Timeout.Please login to Continue", "danger")
                    return redirect(url_for('login.loginUser'))
                return f(current_user, user_role, *args, **kwargs)
        else:
            flash("Session Timeout.Please login to continue", "danger")
            return redirect(url_for('login.loginUser'))

    return decorated


@login.route('/', methods=['GET', 'POST'])
@login.route('/login', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            flash("Please enter your credentials to login", "danger")
            return render_template('login.html')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid Email/Password", "danger")
        elif password == user.password:
            userRole = db.session.query(User, Roles).filter_by(email=email).outerjoin(Roles,
                                                                                      User.role_id == Roles.id).first()
            token = jwt.encode({'email': email, 'role': userRole[1].name,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secretKey)
            session['token'] = token
            session['role'] = userRole[1].name
            return redirect(url_for('login.home', role=userRole[1].name))
        else:
            flash("Invalid Email/Password", "danger")
            return render_template('login.html')
    return render_template('login.html')


@login.route('/<role>')
@token_required
def home(current_user, user_role, role):
    questions = Question.query.all()
    category = Category.query.all()
    skills = Skill.query.all()
    qtypes = Question_type.query.all()

    if user_role == role:
        return render_template('home.html', current_user=current_user, role=user_role, question=questions,
                               category=category, skills=skills, qtypes=qtypes)
    else:
        flash("You are not an authorized person to view this page", "danger")
        return render_template('layout.html', role=user_role)
    return render_template('home.html', role=user_role)


@login.route('/<role>/users', methods=['GET', 'POST'])
@token_required
def users(current_user, user_role, role):
    users = db.session.query(User, Roles).outerjoin(Roles, User.role_id == Roles.id).all()
    if current_user.role.name == 'admin':
        return render_template('users.html', users=users, role=user_role, current_user=current_user)
    else:
        flash("You are not an authorized person to view this page", "danger")
        return render_template('layout.html', role=user_role)
    return render_template('users.html', current_user=current_user, users=users, role=user_role)


# @login.route('<role>/update/<email>',methods = ['GET','POST'])
# def updateUser(email,role):
#    if request.method == 'POST':
#       existed_users = User.query.filter_by(email = email).first()

#       existed_users.username = request.form['username']
#       existed_users.email = request.form['email']
#       existed_users.role_id = request.form['role']

#       db.session.commit()
#       flash("Your Details has been updated successfully","success")
#       return redirect(url_for('login.users',role='admin'))
#    return redirect(url_for('login.users',role='admin'))

# @login.route('<role>/addUser',methods = ['GET','POST'])
# def addUser(role):
#    if request.method == 'POST':
#       username = request.form['username']
#       email = request.form['email']
#       password = request.form['password']
#       confirmPassword = request.form['confirmPassword']
#       user_role = request.form.get('role')
#       print user_role
#       existed_users = User.query.all()
#       for user in existed_users:
#          if user.email == email:
#             flash("Email ID already exists","danger")
#             return redirect(url_for('login.users', role = 'admin')) 
#       if password == confirmPassword:
#          newUser = User(username,email,password,user_role)
#          print newUser.username
#          db.session.add(newUser)
#          newUserRole = Roles(user_role)
#          db.session.add(newUserRole)
#          db.session.commit()
#          flash("New User Created Successfully","success")
#          return redirect(url_for('login.users', role = 'admin'))
#       else:
#          flash("Password Mismatch","danger")
#          return redirect(url_for('login.users',role = 'admin'))
#    return redirect(url_for('login.users', role = 'admin'))

@login.route('/delete/<email>/<role>')
def deleteUser(email, role):
    deleteUser = User.query.filter_by(email=email).first()
    db.session.delete(deleteUser)
    db.session.commit()
    flash("User Deleted Successfully", "success")
    return redirect(url_for('login.users', role='admin'))


@login.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.loginUser'))


if __name__ == '__main__':
    app.run(debug=True)
