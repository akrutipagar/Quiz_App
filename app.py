from flask import url_for,redirect,render_template,request,Flask,flash,session
from flask_login import login_manager,LoginManager
from flask_sqlalchemy import SQLAlchemy
from models import User,Subject,Chapter
from models import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///quiz_app.db"
app.secret_key="akruti99"
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.init_app(app)
db.init_app(app)


with app.app_context():
    db.create_all()
    admin=User.query.filter_by(username='admin').first()
    if not admin:
     add_admin=User(username='admin',password='akruti123',fullname='admin',qualification='admin',dob='03/05/2002')
     db.session.add(add_admin)
     db.session.commit()






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    subject=Subject.query.all()
    user=User.query.filter(User.username!='admin').all()
    return render_template('admin_dashboard.html',user=user,subject=subject)

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
    if not subject:
        flash ('no such subject exists')
        redirect(url_for('admin_dashboard'))
    else:
        Chapter.query.filter_by(subject_id=subject_id).delete()
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_subject.html',subject=subject)


@app.route('/admin/chapter',methods=['GET','POST'])
def create_chapter():
    subject=Subject.query.all()
    if request.method=="POST":
     subject_id=request.form.get('subject.id')
     name=request.form.get('name')
     description=request.form.get('description')
     chapter=Chapter(subject_id=subject_id,name=name,description=description)
     db.session.add(chapter)
     db.session.commit()
     return redirect(url_for('admin_dashboard')) 
    return render_template('create_chapter.html',subject=subject)

@app.route('/admin/edit_chapter/<int:subject_id>',methods=["GET","POST"])
def edit_chapter(subject_id):
    chapter=Chapter.query.get(subject_id)
    if request.method=="POST":
        chapter.name=request.form.get('name')
        chapter.description=request.form.get('description')
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_chapter.html',chapter=chapter)









        
   

    


@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    session.pop('is_admin',False)
    return render_template(url_for('home'))



if __name__=='__main__':
    print(app.url_map)
    app.run(debug=True)

