from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    chapter=db.relationship("Chapter",backref='subject',lazy=True)

class Chapter(db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    subject_id=db.Column(db.Integer,db.ForeignKey('subject.id',ondelete="CASCADE"),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    description=db.Column(db.String(250),nullable=True)

    


    
    
