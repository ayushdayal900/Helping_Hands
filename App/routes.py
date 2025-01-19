import os
from operator import or_
from flask import render_template, request, redirect, url_for, flash
from App.models import Questions, User, Subjects, Chapters
from App.forms import ChapterForm, QuestionForm, RegistrationForm, LoginForm, SubjectForm, UpdateAccountForm
from App import app, db,bcrypt
from flask_login import login_user, current_user, login_required, logout_user 
import secrets
from PIL import Image




@app.route('/')
@app.route('/home',methods = ['GET','POST'])
def home():
    return render_template('home.html', title = 'Home')





def save_pucture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route('/account',methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pucture(form.picture.data)
            current_user.image_file = picture_file

        current_user.name = form.name.data
        current_user.lname = form.lname.data
        current_user.username = form.username.data
        current_user.dob = form.dob.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated", 'success')
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.name.data = current_user.name 
        form.lname.data = current_user.lname 
        form.dob.data = current_user.dob 
        form.email.data = current_user.email 

    image_file = url_for('static',filename="images/" + current_user.image_file)
    return render_template('account.html', title= "Account", image_file=image_file, form = form)








@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
                    name = form.name.data,
                    lname = form.lname.data,
                    dob = form.dob.data,
                    username = form.username.data,
                    email = form.email.data,
                    password = hashed_password,
                    )

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',form = form, title = 'Register')



    

@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
        or_(User.username == form.email_username.data,
            User.email == form.email_username.data
            )
        ).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your credientials.','danger')
    return render_template('login.html',form = form, title = 'Login')










@app.route('/logout',methods = ['GET','POST'])
def logout():
    
    logout_user()
    return redirect(url_for('home'))







@app.route('/users_list', methods = ['GET', 'POST'])
def users_list():
    users = User.query.all()
    return render_template('users_list.html',  title = 'Users', users = users) 



@app.route('/subjects/new', methods=['GET', 'POST'])
@login_required
def new_sub():
    form = SubjectForm()
    if form.validate_on_submit():
        id = form.id.data
        existing_subject = Subjects.query.get(id)

        if existing_subject:
            id = existing_subject.id
            flash('Subject Already Exists ..!', 'danger')
            return redirect(url_for('new_sub'))
        
        sub = Subjects(name = form.name.data, id=id, no_of_chapters = 0, no_of_questions = 0)
        db.session.add(sub)
        db.session.commit()

        sub.number_of_chapters = len(sub.chapters)
        db.session.commit()

        flash('New Subject Created..!', 'success')
        return redirect(url_for('home'))
    return render_template('add_sub.html', title='New Subject', form = form)


@app.route('/chapters/new', methods=['GET', 'POST'])
@login_required
def new_chap():
    form = ChapterForm()
    if form.validate_on_submit():
        id=form.id.data
        existing = Chapters.query.get(id)
        if existing:
            id = existing.id

        # Create a new chapter
        chap = Chapters(
            name=form.name.data,
            id = id,
            subject_id=form.subject_id.data,
            no_of_questions=0  # Default to 0
        )
        db.session.add(chap)
        db.session.commit()

        # Update the associated subject
        subject = Subjects.query.get(form.subject_id.data)
        if subject:
            subject.update_stats()
            db.session.commit()

        flash('New Chapter Created and Subject Updated!', 'success')
        return redirect(url_for('home'))
    return render_template('add_chap.html', title='New Chapter', form=form)


@app.route('/questions/new', methods=['GET', 'POST'])
@login_required
def new_que():
    form = QuestionForm()
    if form.validate_on_submit():
        # Create a new chapter
        que = Questions(
            name=form.name.data,
            subject_id=form.subject_id.data,
            chapter_id=form.chapter_id.data
        )
        db.session.add(que)
        db.session.commit()

        # Update the associated subject
        chapter = Chapters.query.get(form.chapter_id.data)
        if chapter:
            chapter.update_stats()
            db.session.commit()

        flash('New Question Added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_que.html', title='New Chapter', form=form)





@app.route('/subjects/list',methods = ['GET','POST'])
def subject_list():
    subjects = Subjects.query.all()
    return render_template('subject_list.html',title = 'Subjects', subjects = subjects)


@app.route('/subjects/chapters',methods = ['GET','POST'])
def chapter_list():
    chapters = Chapters.query.all()
    return render_template('chapter_list.html',title = 'Chapters', chapters = chapters)




@app.route('/subjects/chapters/questions',methods = ['GET','POST'])
def question_list():
    questions = Questions.query.all()
    return render_template('question_list.html',title = 'Questions', questions = questions)

