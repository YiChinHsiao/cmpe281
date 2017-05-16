from flask import Flask, render_template, session, request, redirect, url_for
from application import db
from application.models import *
import os
from flask_mail import Mail,  Message

application = Flask(__name__)
application.secret_key = os.urandom(32)

application.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'cmpeapp@gmail.com',
    MAIL_PASSWORD = 'cmpeapp.1234',
)
mail = Mail(application)

db.create_all()

app_root = 'http://127.0.0.1:5000'

@application.route('/', methods=['Get', 'POST'])
@application.route('/main', methods=['Get', 'POST'])
def main():
    session['user_id'] = 'Admin'
    name = session['user_id']
    communities = Community.query.all()
    my_community = User_community.query.filter_by(user_id=name).all()
    my_community_id = [community.community_id for community in my_community]
    communities_id = [community.community_id for community in communities if community.community_id not in my_community_id]
    if User.query.filter_by(user_id=name).first().isAdmin == True:
        isAdmin = User.query.filter_by(user_id=name).first().isAdmin
        return render_template('main.html', name=name, isAdmin=isAdmin, my_community_id=my_community_id, communities_id=communities_id)
    else:
        return render_template('main.html', name=name, my_community_id=my_community_id, communities_id=communities_id)

@application.route('/join_community', methods=['Get', 'POST'])
def join_community():
    name = session['user_id']
    communities = Community.query.all()
    for community in communities:
        if request.form.get(community.community_id):
            community_id = community.community_id
            join = User_community(name, community_id)
            db.session.add(join)
            db.session.commit()
            break
            
    return redirect(url_for('main'))

@application.route('/create_community', methods=['Get', 'POST'])
def create_community():
    name = session['user_id']
    error = ''
    if request.form.get('create_community'):		
        if request.form.get('new_community_id') and Community.query.filter_by(community_id=request.form.get('new_community_id')).first() is None:
            new_community_id = request.form.get('new_community_id')
            new_community_description = request.form.get('new_community_description')
            new_community = Community(new_community_id, new_community_description)
            new_user_community = User_community(name, new_community_id)
            new_moderator_community = Moderator_community(new_community_id, name)
            db.session.add(new_community)
            db.session.add(new_user_community)
            db.session.add(new_moderator_community)
            db.session.commit()
            return redirect(url_for('main'))
        elif Community.query.filter_by(community_id=request.form.get('new_community_id')).first(): 
            error = 'Community name already existed'
            return render_template('create_community.html', error=error)
        else:
            error = 'Community name cannot be blank'
            return render_template('create_community.html', error=error)
    else:
        return render_template('create_community.html')

@application.route('/admin', methods=['Get', 'POST'])
def admin():
    users = User.query.all()
    users_id = [user.user_id for user in users if user.isAdmin == False]
    communities = Community.query.all()
    communities_id = [community.community_id for community in communities]
    moderator_communities = Moderator_community.query.all()
    error = request.args.get('error')
    if error:
        return render_template('admin.html', users_id=users_id, communities_id=communities_id, moderator_communities=moderator_communities, error=error)
    else:
        return render_template('admin.html', users_id=users_id, communities_id=communities_id, moderator_communities=moderator_communities)

@application.route('/delete_user', methods=['Get', 'POST'])
def delete_user():
    users = User.query.all()
    for user in users:
        if request.form.get(user.user_id) == 'Delete User':
            user_id = user.user_id
            delete_user = User.query.filter_by(user_id=user_id).first()
            db.session.delete(delete_user)
            db.session.commit()
            
            user_communities = User_community.query.filter_by(user_id=user_id).all()
            for user_community in user_communities:
                db.session.delete(user_community)
                db.session.commit()
            
            posts = Post.query.filter_by(poster_id=user_id).all()
            for post in posts:
                db.session.delete(post)
                db.session.commit()
            
            moderator_communities = Moderator_community.query.filter_by(moderator=user_id).all()
            for moderator_community in moderator_communities:
                db.session.delete(moderator_community)
                db.session.commit()
            
            tasks = Task.query.filter_by(owner=user_id).all()
            for task in tasks:
                db.session.delete(task)
                db.session.commit()
            
            task_requests = Task_request.query.filter_by(requestor_id=user_id).all()
            for task_request in task_requests:
                db.session.delete(task_request)
                db.session.commit()
                
            break
            
    return redirect(url_for('admin'))
        
@application.route('/delete_community', methods=['Get', 'POST'])
def delete_community():
    communities = Community.query.all()
    for community in communities:
        if request.form.get(community.community_id) == 'Delete Community':
            community_id = community.community_id	
            communities = Community.query.filter_by(community_id=community_id).first()
            db.session.delete(community)
            db.session.commit()
            
            user_communities = User_community.query.filter_by(community_id=community_id).all()
            for user_community in user_communities:
                db.session.delete(user_community)
                db.session.commit()
                
            posts = Post.query.filter_by(community_id=community_id).all()
            for post in posts:
                db.session.delete(post)
                db.session.commit()
            
            moderator_communities = Moderator_community.query.filter_by(community_id=community_id).all()
            for moderator_community in moderator_communities:
                db.session.delete(moderator_community)
                db.session.commit()
                
            break

    return redirect(url_for('admin'))
            
@application.route('/delete_moderator', methods=['Get', 'POST'])
def delete_moderator():
    error = ''
    moderator_communities = Moderator_community.query.all()
    for moderator_community in moderator_communities:
        if request.form.get(moderator_community.community_id) == 'Delete Moderator':
            delete_community_id = moderator_community.community_id
            delete_moderator = moderator_community.moderator
            check = Moderator_community.query.filter_by(community_id=delete_community_id).all()
            if len(check) > 1:
                delete_moderator_community = Moderator_community.query.filter_by(community_id=delete_community_id, moderator=delete_moderator).first()
                db.session.delete(delete_moderator_community)
                db.session.commit()
                break
            else:
                error = 'Each community should have at least one moderator'

    return redirect(url_for('admin', error=error))		    
                
@application.route('/add_moderator', methods=['Get', 'POST'])
def add_moderator():
    error = ''
    communities = Community.query.all()
    for community in communities:
        if request.form.get('community_id') == community.community_id:
            users = User.query.all()
            for user in users:
                if request.form.get('user_id') == user.user_id:
                    community_id = community.community_id
                    user_id = user.user_id
                    check = Moderator_community.query.filter_by(community_id=community_id, moderator=user_id).first()
                    if check is None:
                        new_moderator = Moderator_community(community_id, user_id)
                        db.session.add(new_moderator)
                        db.session.commit()
                        break
                    else:
                        error = 'The moderator already exists'
                        break

    return redirect(url_for('admin', error=error))

@application.route('/email_test')
def send_mail(email='eric.clone@gmail.com', subject='Testing', content='none'):
    msg = mail.send_message(
        subject,
        sender='cmpeapp@gmail.com',
        recipients=[email],
        body=content
    )
    return 'Successfully sent email to ' + email 
    
if __name__ == '__main__':
    application.run(debug = True)