from qbank import db
from flask import request, render_template, jsonify, Blueprint,flash,redirect,url_for
# application modules
from qbank.schema import Category, Skill, Level, Question, Question_type,User,Roles
from qbank.apis.login import token_required
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

application = Blueprint('application', __name__)

# @application.route('/question', methods=['GET','POST'])
# @token_required
# def questions(current_user,user_role):
#     category = Category.query.all()
#     skills = Skill.query.all()
#     qtypes = Question_type.query.all()
#     levels = Level.query.all()

#     qtype = request.args.get("qtype")
#     weightage = request.args.get("weightage")

#     if qtype == 'All' and weightage == 'All':
#       questions = Question.query.filter_by(
#                   skill_id= request.args.get("skill_list"),
#                   category_id= request.args.get("category_list"),
#                 )
#     elif weightage == 'All':
#       questions = Question.query.filter_by(
#                   skill_id= request.args.get("skill_list"),
#                   category_id= request.args.get("category_list"),
#                   qtype_id = request.args.get("qtype")
#                 )
#     elif qtype == 'All':
#       questions = Question.query.filter_by(
#                   skill_id= request.args.get("skill_list"),
#                   category_id= request.args.get("category_list"),
#                   weightage= request.args.get("weightage")
#                 )
#     else:
#       questions = Question.query.filter_by(
#                   skill_id= request.args.get("skill_list"),
#                   qtype_id= request.args.get("qtype"),
#                   category_id= request.args.get("category_list"),
#                   weightage= request.args.get("weightage")
#                 )
#     return render_template('questions.html', current_user = current_user, questions=questions,category=category,skills=skills,qtypes=qtypes)

@application.route('/question', methods=['GET', 'POST'])
@token_required
def questions(current_user,user_role):
    weightage=request.args.getlist("weightage[]")
    qtypes = Question_type.query.all()
    questionsList= []
    if request.args.get("qtype")=="All" and weightage[0]=="All":
        questions = Question.query.filter_by(
            category_id=request.args.get("category_list"),
            skill_id=request.args.get("skill_list"),
        )
        for ques in questions:
          questionsList.append(ques)
    elif request.args.get("qtype")=="All":
        for weightageList in weightage:
            questions = Question.query.filter_by(
                category_id=request.args.get("category_list"),
                skill_id=request.args.get("skill_list"),
                weightage=weightageList
            )
            for ques in questions:
              questionsList.append(ques)
    elif weightage[0]=="All":
        questions = Question.query.filter_by(
            category_id=request.args.get("category_list"),
            skill_id=request.args.get("skill_list"),
            qtype_id=request.args.get("qtype"),
        )
        for ques in questions:
          questionsList.append(ques)
    else:
        for weightageList in weightage:
            questions = Question.query.filter_by(
                category_id=request.args.get("category_list"),
                skill_id=request.args.get("skill_list"),
                qtype_id=request.args.get("qtype"),          
                weightage=weightageList
            )
            for ques in questions:
                questionsList.append(ques)
    return render_template('questions.html', questions=questionsList,qtypes=qtypes,current_user=current_user)


@application.route('/question/<int:id>', methods=["GET"])
def question(id):
  try:
    category = Category.query.all()
    skills = Skill.query.all()
    qtypes = Question_type.query.all()
    levels = Level.query.all()
    
    question = db.session.query(
      Question.author,
      Question.id,
      Question.description,
      Question.weightage,
      Question.summary,
      (Skill.id).label("sid"),
      (Category.id).label("cid"),
      (Question_type.id).label("q_type_id"),
      (Skill.name).label("skill"),
      Category.name.label("category"),
      Question_type.name.label("qtype")
      ).filter_by(id=id).\
      join(Skill, Skill.id == Question.skill_id).\
      join(Question_type, Question_type.id == Question.qtype_id).\
      join(Category, Category.id == Skill.category_id).\
      first()
    weightages = {}
    for level in levels:
      weightages[level.name] = round(float(question.weightage)*float(level.weightage_factor), 2)  
      form = ('edit.html' if request.args.get("form_type")== "#editQuestion" else "show.html")
    return render_template(form, question=question, category=category, skills=skills, qtypes=qtypes, levels=levels, weightages=weightages)
  except Exception as err:
    print("Failed to find the question.")
    print(err)    

