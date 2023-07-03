from flask import request, render_template, jsonify, Blueprint

# application modules
from qbank import db

import pdb;

viewer = Blueprint('viewer', __name__)

# @viewer.route('/')
@viewer.route('/viewer2')
def index():
    category = Category.query.all()
    skills = Skill.query.all()
    qtypes = Question_type.query.all()

    return render_template('viewer.html',category=category,skills=skills,qtypes=qtypes)


if __name__ == '__main__':
    #db.create_all()
    app.run(debug = True)