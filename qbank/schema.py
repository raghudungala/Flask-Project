from qbank import db, ma
import datetime


class Question_type(db.Model):
    __tablename__ = 'question_type'
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.SmallInteger, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    questions = db.relationship("Question", backref="question_type")

    def __init__(self, name):
        self.name = name


class Question(db.Model):
    __tablename__ = 'question'
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.Integer, primary_key=True)
    summary = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    weightage = db.Column(db.SmallInteger, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qtype_id = db.Column(db.SmallInteger, db.ForeignKey('question_type.id'))
    skill_id = db.Column(db.SmallInteger, db.ForeignKey('skill.id'))
    category_id = db.Column(db.SmallInteger, db.ForeignKey('category.id'))
    last_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, summary, description, weightage, author_id, qtype_id, skill_id, category_id):
        self.summary = summary
        self.description = description
        self.weightage = weightage
        self.author_id = author_id
        self.qtype_id = qtype_id
        self.skill_id = skill_id
        self.category_id = category_id


class Category(db.Model):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.SmallInteger, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    skills = db.relationship("Skill", backref="category")
    questions = db.relationship("Question", backref="category")

    def __init__(self, name):
        self.name = name


class Skill(db.Model):
    __tablename__ = 'skill'
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.SmallInteger, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    questions = db.relationship('Question', backref="skill")

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id


class Level(db.Model):
    __tablename__ = 'difficulty_level'
    __table_args__ = {'extend_existing': True}
    id = db.Column('id', db.SmallInteger, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    weightage_factor = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, name, weightage_factor):
        self.name = name
        self.weightage_factor = weightage_factor


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.SmallInteger, db.ForeignKey('role.id'))
    questions = db.relationship('Question', backref='author')
    role = db.relationship('Roles', back_populates='user')

    def __init__(self, name, email, password, role_id):
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id


class Roles(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    user = db.relationship("User", back_populates="role")

    def __init__(self, name):
        self.name = name


class NewUserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", 'name', 'email', 'password', 'role_id')


class QuestionSchemaUpdateCreate(ma.Schema):
    class Meta:
        model = Question
        fields = ("id", 'summary', 'description', 'weightage', 'author_id', 'qtype_id', 'skill_id', 'category_id')
