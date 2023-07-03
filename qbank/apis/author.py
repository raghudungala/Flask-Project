from qbank import db
from flask import request, render_template, jsonify, Blueprint, json
# application modules
from qbank.schema import Category, Skill, Question, Question_type, QuestionSchemaUpdateCreate,User,Roles,NewUserSchema
# from werkzeug.datastructures import ImmutableMultiDict
from qbank.apis.login import token_required


author = Blueprint('author', __name__)

def question_obj(id):
  return Question.query.filter_by(id = id).first()

def newUser_obj(id):
  return User.query.filter_by(id = id).first()

@author.route('/addquestion', methods=['POST', "GET"])
def add_questions():
    sid = request.form["sid"]
    new_rec = Question(
                request.form["summary"],
                request.form['description'],
                request.form['weightage'],
                request.form['user_id'],
                request.form['qtype_id'],
                sid,
                request.form['cid']
              )
    try:
      db.session.add(new_rec)
      db.session.commit()
      question_shema = QuestionSchemaUpdateCreate().dump(new_rec).data
      return jsonify({"success": 200, "message": "Question Created Successfully", "question": question_shema})
    except Exception as err:
      print("Failed to create.")
      print(err)
      return jsonify({"status": 404, "message": "Error has occured.Please try again"})

@author.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
  try:
    question = question_obj(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"success": 200, "message": "Question Deleted Successfully", "id": id})
  except Exception as err:
    print("Failed to delete.")
    print(err)
    return jsonify({"status": 404, "message": "Error has occured.Please try again"})

@author.route("/update/<int:id>", methods=["PUT"])
@token_required
def update(current_user,user_role,id):
  question = question_obj(id)
  try:
    if user_role=="admin" or current_user.id== question.author:
      question.description = request.args.get("description")
      question.summary = request.args.get("summary")
      question.weightage = request.args.get("weightage")
      question.qtype_id = request.args.get("qtype_id")
      question.category_id = request.args.get("category_id")
      question.skill_id = request.args.get("skill_id")
      question_shema = QuestionSchemaUpdateCreate().dump(question).data
      db.session.merge(question)
      db.session.commit()
      return jsonify({"success": 200, "message": "Question Updated Successfully", "id": id, "question": question_shema})
  except Exception as err:
    print("Failed to update.")
    print(err)
    return jsonify({"status": 404, "message": "Error has occured.Please try again"})


@author.route("/addUser", methods=['POST','GET'])
@token_required
def addUser(current_user,user_role):
  if request.method == 'POST':
    password = request.form['password']
    confirmPassword = request.form['confirmPassword']
    if password == confirmPassword :
      new_user = User(
                  request.form["username"],
                  request.form['email'],
                  request.form['password'],
                  request.form['role']
                )
    else :
      return jsonify({"status": 404, "message": "Password Mismatch"})
    try:
      db.session.add(new_user)
      db.session.commit()
      addUser_schema = NewUserSchema().dump(new_user).data
      return jsonify({"success": 200, "message": "user Created Successfully", "addUser": addUser_schema})
    except Exception as err:
      print("Failed to create.")
      print(err)
      return jsonify({"status": 404, "message": "Error has occured.Please try again"})

@author.route("/delete/<username>",methods=["DELETE"])
def deleteUser(username):
  try:
    User.query.filter_by(name=username).delete()
    db.session.commit()
    return jsonify({"success": 200, "message": "User Deleted Successfully", "username": username})
  except Exception as err:
    print("Failed to delete.")
    print(err)
    return jsonify({"status": 404, "message": "Error has occured.Please try again"})


@author.route("/user/<id>",methods=["GET"])
def userById(id):
  try:
    users_list = db.session.query(User,Roles).filter_by(id=id).outerjoin(Roles,Roles.id==User.role_id).first()
    return render_template("editUser.html", data=users_list)
    return jsonify({"success": 200, "message": "User Updated Successfully", "id": id, "users_list": users_list})
  except Exception as err:
    print("Failed to find the user.")
    print(err)
    return jsonify({"status": 404, "message": "Error has occured.Please try again"})

@author.route("/updateuser/<username>", methods=["PUT"])
@token_required
def updateuser(current_user,user_role,username):
  try:
    users_list = User.query.filter_by(name=username).first()
    users_list.name = request.args.get("username")
    users_list.email = request.args.get("email")

    users_list.role_id = request.args.get("role_id")

    print(users_list.role_id)

    users_list_shema = NewUserSchema().dump(users_list).data
    db.session.merge(users_list)
    db.session.commit()
    db.session.close()
    return jsonify({"success": 200, "message": "User Updated Successfully", "username": username, "users": users_list_shema})
  except Exception as err:
    print("Failed to update.")
    print(err)
    return jsonify({"status": 404, "message": "Error has occured.Please try again"})

@author.route("/<role>/profile", methods=["GET"])
@token_required
def profile(current_user,user_role,role):
  print("profile")
  users = db.session.query(User,Roles).outerjoin(Roles,User.role_id==Roles.id).all()
  return render_template('userProfile.html', current_user = current_user, role = user_role, users = users)



@author.route("/resetPassword/<username>", methods=["PUT"])
@token_required
def resetPassword(current_user,user_role,username):
  try:
    users_list = User.query.filter_by(name=username).first()
    oldPassword = request.args.get("oldPassword")
    newPassword = request.args.get("newPassword")
    if oldPassword == users_list.password:
      users_list.password = request.args.get("newPassword")
      users_list_shema = NewUserSchema().dump(users_list).data
      db.session.merge(users_list)
      db.session.commit()
      db.session.close()
      return jsonify({"success": 200, "message": "Password Changed Successfully", "username": username, "users": users_list_shema})
    else:
      return jsonify({"status": 404, "message": "Old Password is not matched"})
  except Exception as err:
    print("Failed to update.")
    print(err)
    return jsonify({"status": 404, "message": "Error has occured.Please try again"})



if __name__ == '__main__':
    #db.create_all()
    app.run(debug = True)
