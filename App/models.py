from App import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import Session
from sqlalchemy import event


@event.listens_for(Session, "before_flush")
def update_on_change(session, flush_context, _):
    """
    Automatically updates Subjects and Chapters when Chapters or Questions are added, updated, or deleted.
    """
    for instance in session.new.union(session.dirty):
        if isinstance(instance, Chapters):
            subject = Subjects.query.get(instance.subject_id)
            if subject:
                subject.update_stats()
        
        if isinstance(instance, Questions):
            subject = Subjects.query.get(instance.subject_id)
            chapter = Chapters.query.get(instance.chapter_id)
            if subject:
                subject.update_stats()
            if chapter:
                chapter.update_stats()

    for instance in session.deleted:
        if isinstance(instance, Chapters):
            subject = Subjects.query.get(instance.subject_id)
            if subject:
                subject.update_stats()

        if isinstance(instance, Questions):
            subject = Subjects.query.get(instance.subject_id)
            chapter = Chapters.query.get(instance.chapter_id)
            if subject:
                subject.update_stats()
            if chapter:
                chapter.update_stats()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.name}', '{self.lname}', '{self.dob}', '{self.email}')"


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    no_of_chapters = db.Column(db.Integer, nullable=False, default=0)
    no_of_questions = db.Column(db.Integer, nullable=False, default=0)
    
    # Define relationships
    chapters = db.relationship('Chapters', backref='subject', lazy=True)
    questions = db.relationship('Questions', backref='subject', lazy=True)

    def update_stats(self):
        """Updates the number of chapters and total questions."""
        self.no_of_chapters = db.session.query(Chapters).filter_by(subject_id=self.id).count()
        self.no_of_questions = db.session.query(Questions).filter_by(subject_id=self.id).count()

    def __repr__(self):
        return f"Subjects('{self.name}', '{self.no_of_chapters}', '{self.no_of_questions}')"


class Chapters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    no_of_questions = db.Column(db.Integer, nullable=False, default=0)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
    # Define relationship with Questions
    questions = db.relationship('Questions', backref='chapter', lazy=True)

    def update_stats(self):
        """Updates the number of questions in the chapter."""
        self.no_of_questions = db.session.query(Questions).filter_by(chapter_id=self.id).count()

    def __repr__(self):
        return f"Chapters('{self.name}', '{self.no_of_questions}')"


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)

    def __repr__(self):
        return f"Questions('{self.name}')"




# from App import db, login_manager
# from datetime import datetime
# from flask_login import UserMixin
# from sqlalchemy.orm import Session
# from sqlalchemy import event


# @event.listens_for(Session, "before_flush")
# def update_on_change(session, flush_context, _):
#     """
#     Automatically updates Subjects and Chapters when Chapters or Questions are added, updated, or deleted.
#     """
#     for instance in session.new.union(session.dirty):
#         if isinstance(instance, Chapters):
#             subject = Subjects.query.get(instance.subject_id)
#             if subject:
#                 subject.update_stats()
#                 session.add(subject)

#         if isinstance(instance, Questions):
#             subject = Subjects.query.get(instance.subject_id)
#             chapter = Chapters.query.get(instance.chapter_id)
#             if subject:
#                 subject.update_stats()
#                 session.add(subject)
#             if chapter:
#                 chapter.update_stats()
#                 session.add(chapter)

#     for instance in session.deleted:
#         if isinstance(instance, Chapters):
#             subject = Subjects.query.get(instance.subject_id)
#             if subject:
#                 subject.update_stats()
#                 session.add(subject)

#         if isinstance(instance, Questions):
#             subject = Subjects.query.get(instance.subject_id)
#             chapter = Chapters.query.get(instance.chapter_id)
#             if subject:
#                 subject.update_stats()
#                 session.add(subject)
#             if chapter:
#                 chapter.update_stats()
#                 session.add(chapter)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False)
#     name = db.Column(db.String(20), nullable=False)
#     lname = db.Column(db.String(20), nullable=False)
#     dob = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     email = db.Column(db.String(20), nullable=False)
#     password = db.Column(db.String(20), nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

#     def __repr__(self):
#         return f"User('{self.name}', '{self.lname}', '{self.dob}', '{self.email}')"


# class Subjects(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     no_of_chapters = db.Column(db.Integer, nullable=False, default=0)
#     no_of_questions = db.Column(db.Integer, nullable=False, default=0)
    
#     # Define relationships
#     chapters = db.relationship('Chapters', backref='subject', lazy=True)
#     questions = db.relationship('Questions', backref='subject', lazy=True)

#     def update_stats(self):
#         """Updates the number of chapters and total questions."""
#         self.no_of_chapters = len(self.chapters)
#         self.no_of_questions = sum(chap.no_of_questions for chap in self.chapters)

#     def __repr__(self):
#         return f"Subjects('{self.name}', '{self.no_of_chapters}', '{self.no_of_questions}')"


# class Chapters(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=False)
#     no_of_questions = db.Column(db.Integer, nullable=False, default=0)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    
#     # Define relationship with Questions
#     questions = db.relationship('Questions', backref='chapter', lazy=True)

#     def update_stats(self):
#         """Updates the number of questions in the chapter."""
#         self.no_of_questions = len(self.questions)  # Count the number of associated questions

#     def __repr__(self):
#         return f"Chapters('{self.name}', '{self.no_of_questions}')"


# class Questions(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(20), nullable=False)
#     chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
#     subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)

#     def __repr__(self):
#         return f"Questions('{self.name}')"

