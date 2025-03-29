from flask_mail import Mail, Message
from flask import current_app
import threading

mail = Mail()

def send_async_email_reminders(flask_app_instance, mail_data: dict):
    mail_subject = "New Quiz Available on your portal"
    with flask_app_instance.app_context():
        for user in mail_data['users']:
            if not mail_data['chapter_name']:
                scope_text = f"the subject {mail_data['subject_name']}"
            else:
                scope_text = f"{mail_data['chapter_name']} from {mail_data['subject_name']}"
            mail_body = f"Hi {user[0]}\n\nWe just released a new quiz on {scope_text}.\n\nGo check it out now and see if you can get it all right."

            msg = Message(mail_subject, recipients=[user[1]], body=mail_body)
            mail.send(msg)

def send_email_reminders(quiz_id):
    mail_data = {
        'subject_name': '',
        'chapter_name': '',
        'description': '',
        'users': [],
    }

    # fetch mail details
    from utils.models import Quiz, Chapter, Subject, User
    quiz = Quiz.query.get(quiz_id)
    mail_data['description'] = quiz.description
    subjectId = quiz.subject_id
    if quiz.scope == 'chapter':
        chapter = Chapter.query.get(quiz.chapter_id)
        mail_data['chapter_name'] = chapter.name
        subjectId = chapter.subject_id
    subject = Subject.query.get(subjectId)
    mail_data['subject_name'] = subject.name
    mail_data['users'] = [(user.name.split()[0], user.email) for user in User.query.all()]

    # start the email process in a new thread
    flask_app_instance = current_app._get_current_object()
    thread = threading.Thread(target=send_async_email_reminders, args=(flask_app_instance, mail_data))
    thread.start()