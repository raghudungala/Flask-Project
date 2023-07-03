Navigate to C:\Users\dragh\Documents\ptoject\UpdatedQbank\qbank
set set PYTHONPATH=%PYTHONPATH%;C:\Users\dragh\Documents\ptoject\UpdatedQbank\qbank
C:\Users\dragh\Documents\ptoject\UpdatedQbank\qbank\proenv\Scripts
set FLASK_APP=qbank.py
flask run

flask shell
from qbank.schema import db, User
db.create_all()
db.session.add(student_john)
db.session.commit()