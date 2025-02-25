from flask import url_for,redirect,render_template,request,Flask,flash,session
from flask_sqlalchemy import SQLAlchemy
from models import User,Subject,Chapter,Quiz,Question,Score
from models import db
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///quiz_app.db"
app.secret_key="akruti99"

db.init_app(app)


with app.app_context():
    db.create_all()
    admin=User.query.filter_by(username='admin').first()
    if not admin:
     add_admin=User(username='admin',password='akruti123',fullname='admin',qualification='admin',dob='03/05/2002')
     db.session.add(add_admin)
     db.session.commit()






def load_user(user_id):
    user_id=session.get('user_id')
    if user_id:
        return User.query.get(int(user_id))
    return None

@app.route('/')
def home():
    return render_template('login.html')



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter_by(username=username,password=password).first()
        if user:
            if user.username=='admin' and user.password=='akruti123':
                return redirect(url_for('admin_dashboard'))
            else:
               session['user_id']=user.id
               return redirect(url_for('user_dashboard'))
            
        else:
            flash ("wrong credentials")
            
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        fullname=request.form.get('fullname')
        qualification=request.form.get('qualification')
        dob=request.form.get('dob')
        user=User.query.filter_by(username=username).first()
        if(user):
            flash('user already exists!')
        else:
            new_user=User(username=username,password=password,fullname=fullname,qualification=qualification,dob=dob)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin/dashboard',methods=['GET','POST'])
def admin_dashboard():
    search=request.form.get('search'," ").strip().lower()
    subject=Subject.query.all()
    user=User.query.filter(User.username!='admin').all()
    quiz=Quiz.query.all()
    chapter=Chapter.query.all()
    question=Question.query.all()

    if search:
        user=User.query.filter(User.username.ilike(f"%{search}%" )).all()
        subject=Subject.query.filter(Subject.name.ilike(f"%{search}%" )).all()
        chapter=Chapter.query.filter(Chapter.name.ilike(f"%{search}%" )).all()
        quiz=Quiz.query.filter(Quiz.name.ilike(f"%{search}%" )).all()
    else:
        user=User.query.all()
        subject=Subject.query.all()
        quiz=Quiz.query.all()
        chapter=Chapter.query.all()

    return render_template('admin_dashboard.html',user=user,subject=subject,quiz=quiz,question=question,chapter=chapter)

@app.route('/admin/subject',methods=['GET','POST'])
def create_new_subject():
   return render_template('create_subject.html')

@app.route('/admin/create_new_subject',methods=['GET','POST'])
def create_subject():
    name=request.form.get('name')
    description=request.form.get('description')
    subjects=Subject(name=name,description=description)
    db.session.add(subjects)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_subject/<int:subject_id>',methods=['GET','POST'])
def edit_subject(subject_id):
    subject=Subject.query.get(subject_id)
    if request.method=='POST':
      subject.name=request.form.get('name')
      subject.description=request.form.get('description')
      db.session.commit()
      return redirect(url_for('admin_dashboard'))
    return render_template('edit_subject.html',subject=subject)
   
@app.route('/admin/delete/<int:subject_id>',methods=["GET","POST"])
def delete_subject(subject_id):
    subject=Subject.query.get(subject_id)
    
    for chap in subject.chapter:
        for quiz in chap.quiz:
            for question in quiz.question:
                db.session.delete(question)
            db.session.delete(quiz)
        db.session.delete(chap)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))
    


@app.route('/admin/chapter/<int:subject_id>',methods=['GET','POST'])
def create_chapter(subject_id):
    
    subject=Subject.query.get(subject_id)
    if request.method=="POST":
    
     name=request.form.get('name')
     description=request.form.get('description')
     chapter=Chapter(subject_id=subject_id,name=name,description=description)
     db.session.add(chapter)
     db.session.commit()
     return redirect(url_for('admin_dashboard')) 
    return render_template('create_chapter.html',subject=subject)

@app.route('/admin/edit_chapter/<int:chapter_id>/<int:subject_id>',methods=["GET","POST"])
def edit_chapter(chapter_id,subject_id):
    chapter=Chapter.query.get(chapter_id)
    subject=Subject.query.get(subject_id)
    if request.method=="POST":
        chapter.name=request.form.get('name')
        chapter.description=request.form.get('description')
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_chapter.html',subject=subject,chapter=chapter)

@app.route('/admin/delete_chapter/<int:chapter_id>/<int:subject_id>',methods=["POST","GET"])
def delete_chapter(chapter_id,subject_id):
    chapter=Chapter.query.get(chapter_id)
    
    for i in chapter.quiz:
        for j in i.question:
            db.session.delete(j)
        db.session.delete(i)
    
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))



@app.route('/admin/create_quiz/<int:chapter_id>/<int:subject_id>',methods=["GET","POST"])
def create_quiz(chapter_id,subject_id):
    
    chapter=Chapter.query.get(chapter_id)
    subject=Subject.query.get(subject_id)
    if request.method=="POST":
        name=request.form.get('name')
        
        
        remarks=request.form.get('remarks')
        duration=datetime.strptime(request.form.get('duration'),'%H:%M').time()
        quiz = Quiz(name=name,chapter_id=chapter.id,remarks=remarks,duration=duration)
        
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('create_new_quiz.html',chapter=chapter,subject=subject)

@ app.route('/admin/editquiz/<int:quiz_id>/<int:subject_id>',methods=["GET","POST"])
def edit_quiz(quiz_id,subject_id):
    quiz=Quiz.query.get(quiz_id)
    subject=Subject.query.get(subject_id)
    if request.method=='POST':
        quiz.name=request.form.get('name')
        quiz.remarks=request.form.get('remarks')
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_quiz.html',quiz=quiz,subject=subject)

@app.route('/admin/deletequiz/<int:quiz_id>,<int:subject_id>',methods=["POST","GET"])
def delete_quiz(quiz_id,subject_id):
    quiz=Quiz.query.get(quiz_id)
    
    for question in quiz.question:
        db.session.delete(question)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/addquestion/<int:subject_id>/<int:quiz_id>',methods=["POST",'GET'])
def add_question(quiz_id,subject_id):
    quiz=Quiz.query.get(quiz_id)
    subject=Subject.query.get(subject_id)
    
    if request.method=="POST":
        statement=request.form.get('statement')
        option_1=request.form.get('option_1')
        option_2=request.form.get('option_2')
        option_3=request.form.get('option_3')
        option_4=request.form.get('option_4')
        correct_answer=request.form.get('correct_answer')
        question=Question(quiz_id=quiz_id,statement=statement,option_1=option_1,option_2=option_2,option_3=option_3,option_4=option_4,correct_answer=correct_answer)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('create_question.html',subject=subject,quiz=quiz)
    


@app.route('/admin/addquestion/<int:subject_id>/<int:quiz_id>/<int:question_id>',methods=["POST",'GET'])
def edit_question(quiz_id,subject_id,question_id):
    question=Question.query.get(question_id)
    quiz=Quiz.query.get(quiz_id)
    subject=Subject.query.get(subject_id)
    if request.method=="POST":
        question.statement=request.form.get('statement')
        question.option_1=request.form.get('option_1')
        question.option_2=request.form.get('option_2')
        question.option_3=request.form.get('option_3')
        question.option_4=request.form.get('option_4')
        question.correct_answer=request.form.get('correct_answer')
       
      
        db.session.commit()
        return redirect(url_for('admin_dashbboard'))
    return render_template('edit_question.html',quiz=quiz,subject=subject,question=question)
    

@app.route('/admin/delete_question/<int:subject_id>/<int:quiz_id>/<int:question_id>',methods=["POST",'GET'])
def delete_question(subject_id,quiz_id,question_id):
    
    question=Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/summary',methods=['GET','POST'])
def summary():
    user=User.query.filter(User.username!='admin').all()
    
    return render_template('summary.html',user=user)

@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    user_id=User.query.get(session['user_id'])
    subject=Subject.query.all()
    score=Score.query.filter_by(user_id=session['user_id']).all()
    previous_quiz_attempts={}
    user_id=session.get('user_id')
    previous_attempt=Score.query.filter_by(user_id=user_id).all()
    for i in previous_attempt:
          quiz_name=i.quiz.name
          if quiz_name in  previous_quiz_attempts:
            previous_quiz_attempts[quiz_name]+=1
          else:
            previous_quiz_attempts[quiz_name]=1
    return render_template('user_dashboard.html',user=user_id,subject=subject,score=score,previous_quiz_attempts=previous_quiz_attempts)

@app.route('/user/attempt_quiz/<int:quiz_id>',methods=['GET','POST'])
def attempt_quiz(quiz_id):
    quiz=Quiz.query.get(quiz_id)
    question=Question.query.filter_by(quiz_id=quiz.id).all()
    feedback=[]



    if request.method=="POST":
        total_scored =0
        for i in question:
            answer=request.form.get(str(i.id))
            if answer==i.correct_answer:
                total_scored=total_scored+1
            
            feedback.append({
                'question':i.statement,
                'answer' : answer,
                'correct_answer':i.correct_answer
            })
            
        attempt=Score(user_id=session['user_id'],quiz_id=quiz.id,total_scored=total_scored)

        try:
            db.session.add(attempt)
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
           
        

        
        #return redirect(url_for('user_dashboard'))
    return render_template('attempt_quiz.html',quiz=quiz,question=question,feedback=feedback)










        
   

    


@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))




if __name__=='__main__':
    
    app.run(debug=True)

