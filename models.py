from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db=SQLAlchemy()



class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    fullname=db.Column(db.String(100),nullable=False)
    qualification=db.Column(db.String(250),nullable=True)
    dob=db.Column(db.String(50),nullable=True)
    

class Subject(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(250),nullable=True)
    chapter=db.relationship("Chapter",backref='subject',cascade='all,delete')

class Chapter(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    subject_id=db.Column(db.Integer,db.ForeignKey('subject.id',ondelete="CASCADE"),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(250),nullable=True)
    quiz=db.relationship('Quiz',backref='chapter',cascade='all,delete')

class Quiz(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    chapter_id=db.Column(db.Integer,db.ForeignKey('chapter.id',ondelete="CASCADE"),nullable=False)
    remarks=db.Column(db.String(300),nullable=True)
    question=db.relationship('Question',backref='quiz',cascade='all,delete')
    score=db.relationship('Score',backref='quiz',cascade='all,delete')

class Question(db.Model):
     id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
     quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id',ondelete="CASCADE"),nullable=False)
     statement=db.Column(db.Text,nullable=False)
     option_1=db.Column(db.String(200),nullable=False)
     option_2=db.Column(db.String(200),nullable=False)
     option_3=db.Column(db.String(200),nullable=False)
     option_4=db.Column(db.String(200),nullable=False)
     correct_answer=db.Column(db.String(200),nullable=False)
     
class Score(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id',ondelete="CASCADE"),nullable=False)
    time_stamp_of_attempt=db.Column(db.DateTime,default= datetime.now().replace(microsecond=0))
    total_scored=db.Column(db.Integer,nullable=False)
    total_question=db.Column(db.Integer,nullable=False)

    user=db.relationship('User',backref='score')
   
    


    


    
    
