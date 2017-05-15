from flask import Flask, render_template, session, request
from application import db
from application.models import *
import os

application = Flask(__name__)
application.secret_key = os.urandom(32)

db.create_all()

app_root = 'http://127.0.0.1:5000'

@application.route('/', methods=['Get', 'POST'])
@application.route('/main', methods=['Get', 'POST'])
def main():
    session['user_id'] = 'Admin'
    name = session['user_id']
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
        elif Community.query.filter_by(community_id=request.form.get('new_community_id')).first(): 
            error = 'Community name already existed'
            return render_template('create_community.html', error=error)
        else:
            error = 'Community name cannot be blank'
            return render_template('create_community.html', error=error)
    communities = Community.query.all()
    for community in communities:
        if request.form.get(community.community_id):
            community_id = community.community_id
            join = User_community(name, community_id)
            db.session.add(join)
            db.session.commit()
            break
    communities = Community.query.all()
    my_community = User_community.query.filter_by(user_id=name).all()
    my_community_id = [community.community_id for community in my_community]
    communities_id = [community.community_id for community in communities if community.community_id not in my_community_id]
    if User.query.filter_by(user_id=name).first().isAdmin == True:
        isAdmin = User.query.filter_by(user_id=name).first().isAdmin
        return render_template('main.html', name=name, app_root = app_root, isAdmin=isAdmin, my_community_id=my_community_id, communities_id=communities_id)
    else:
    	return render_template('main.html', name=name, app_root = app_root, my_community_id=my_community_id, communities_id=communities_id)

@application.route('/create_community')
def create_community():
    return render_template('create_community.html')

@application.route('/admin', methods=['Get', 'POST'])
def admin():
    error = ''
    #Delete User
    users = User.query.all()
    for user in users:
    	if request.form.get(user.user_id):
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
	#Delete Community
    #---communities = Community.query.all()
    #---for community in communities:
	#Delete Moderator
	moderator_communities = Moderator_community.query.all()
    for moderator_community in moderator_communities:
		if request.form.get(moderator_community.community_id) and request.form.get(moderator_community.moderator):
			delete_community_id = moderator_community.community_id
			delete_moderator = moderator_community.moderator
			check = Moderator_community.query.filter_by(community_id=delete_community_id).all()
			delete_moderator_community = Moderator_community.query.filter_by(community_id=delete_community_id, moderator=delete_moderator).first()
			db.session.delete(delete_moderator_community)
			db.session.commit()
			break
			#if len(check) > 1:
				#delete_moderator_community = Moderator_community.query.filter_by(community_id=delete_community_id, moderator=delete_moderator).first()
				#db.session.delete(delete_moderator_community)
				#db.session.commit()
				#break
	#Add Moderator
    if request.form.get('add_moderator'):	
		data='test'
    users = User.query.all()
    users_id = [user.user_id for user in users if user.isAdmin == False]
    communities = Community.query.all()
    communities_id = [community.community_id for community in communities]
    moderator_communities = Moderator_community.query.all()
    return render_template('admin.html', users_id=users_id, communities_id=communities_id, moderator_communities=moderator_communities)

if __name__ == '__main__':
    application.run(debug = True)

