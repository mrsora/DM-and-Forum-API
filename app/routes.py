from app import app, db, login
from app.models import User, Message, Post
from flask_login import login_required, login_user, logout_user, current_user
from flask import request, json
from sqlalchemy import exc


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/api/deluser/<username>', methods=['DELETE'])
def delUser(username):
    try:
        user = User.query.filter(User.username == username).one()
    except exc.NoResultFound:
        return json.jsonify({"error": "Username not found"}), 403
    db.session.delete(user)
    db.session.commit()

    return "Success", 204


@app.route('/api/showusers')
def showUsers():
    users = User.query.all()
    output = []
    for user in users:
        output.append(
            {'id': user.id, 'username': user.username, "pw": user.password_hash})

    return {"all users": output}, 200


@app.route('/api/showmessages')
def showMessages():
    messages = Message.query.all()
    output = []
    for message in messages:
        output.append({'senderID': message.senderID,
                      'recID': message.recipientID, 'content': message.body})
    return {'all messages': output}, 200


@app.route('/api/showposts')
def showPosts():
    posts = Post.query.all()
    output = []
    for post in posts:
        output.append(
            {'id': post.id, 'posterID': post.posterID, 'body': post.body})
    return {"all posts": output}, 200
# Endpoints --------
# Section 1 --------


@app.route('/api/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:

        return json.jsonify({"error": "Username or Password cannot be empty"}), 403
    if User.query.filter_by(username=username).first() is not None:
        return json.jsonify({"error": "Username already exists"}), 403

    user = User(username=username)
    user.hash_pw(password)
    db.session.add(user)
    db.session.commit()

    return "Success", 201


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    candidateUser = User.query.filter_by(username=username).first()
    if not candidateUser or candidateUser.verify_pass(password) is None:
        return json.jsonify({"error": "Incorrect Credentials"}), 403
    login_user(candidateUser)
    return "Success", 200


@app.route('/api/logout')
def logout():
    logout_user()
    return "Success", 200

# Section 2 --------
# Chatting with other users


@app.route('/api/message/<recipient>', methods=['GET', 'POST'])
@login_required
def sendMessage(recipient):
    content = request.json.get('content')
    if len(content) > 140:
        return json.jsonify({"error": "Message content too long"}), 400
    # getting user object of recipient
    ruser = User.query.filter_by(username=recipient).first()
    if not ruser:  # check if recipient even exists
        return json.jsonify({"error": "User does not exist"}), 404
    message = Message(senderID=current_user.id,
                      recipientID=ruser.id, body=content)
    db.session.add(message)
    db.session.commit()
    return "Success", 201


@app.route('/api/checkmessages', methods=['GET'])
@login_required
def checkMessages():
    messages = current_user.messagesReceived.order_by(Message.timestamp.desc())
    output = []
    for message in messages:
        output.append({'senderID': message.senderID,
                      'recID': message.recipientID, 'content': message.body})
    return {f'messages received by {current_user.username}': output}, 200

# Create, read, update, delete tweet


@app.route('/api/createpost', methods=['POST'])
@login_required
def createPost():
    body = request.json.get('content')
    if len(body) > 280:  # never used twitter, but pretty sure message length is 280 max
        return json.jsonify({"error": "Post content too long"}), 400
    post = Post(posterID=current_user.id, body=body)
    db.session.add(post)
    db.session.commit()
    return json.jsonify({"postID": post.id}), 200


@app.route('/api/readpost/<postID>', methods=['GET'])
def readPost(postID):
    post = Post.query.filter_by(id=postID).first_or_404()
    return {'postID': post.id, 'postContent': post.body, 'posterID': post.posterID}, 200


@app.route('/api/updatepost/<postID>', methods=['PUT'])
@login_required
def updatePost(postID):
    # Check if current_user is the poster
    post = Post.query.filter_by(id=postID).first_or_404()
    if not current_user.id == post.posterID:
        return json.jsonify({"error": "Cannot edit post, you are not poster"}), 403
    newcontent = request.json.get('content')
    post.body = newcontent
    db.session.commit()
    return "Success", 200


@app.route('/api/deletepost/<postID>', methods=['DELETE'])
@login_required
def deletePost(postID):
    # Check if post exists
    post = Post.query.filter_by(id=postID).first_or_404()
    # Check if current_user is the poster
    if not current_user.id == post.posterID:
        return json.jsonify({"error": "Cannot delete post, you are not poster"}), 403
    db.session.delete(post)
    db.session.commit()
    return "Success", 204
