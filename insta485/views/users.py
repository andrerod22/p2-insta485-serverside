import flask
import insta485

@insta485.app.route('/users/<user_slug>/', methods=["GET"])
def show_user(user_slug):
    currUser = flask.session['username']
    connection = insta485.model.get_db()
    #Check if user_slug is in the database
    sql = "SELECT username FROM users"
    cur = connection.execute(sql)
    checkUser = cur.fetchall()
    is_in_db = False
    for ind_user in checkUser:
        if ind_user['username'] == user_slug:
            is_in_db = True
    if is_in_db is False:
        flask.abort(404, "User_slug was not found in DB")
    #retrieve info for user.html
    #Grab visited user's username:
    sql = "SELECT * FROM users WHERE username='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData = cur.fetchall() # LIST, should be
    #Grab all posts user made:
    sql = "SELECT postid FROM posts WHERE owner='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]["numPosts"] = len(cur.fetchall())
    #Get owner's profile picture:
    sql = "SELECT filename FROM posts WHERE owner='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]['post_img'] = cur.fetchall()
    sql = "SELECT postid FROM posts WHERE owner='%s'" % (user_slug)
    cur = connection.execute(sql)
    post_ids = cur.fetchall()
    i = 0
    for post in userData[0]['post_img']:
        post['post_id'] = post_ids[i]['postid']
        i += 1
    
    #Get number of following:
    sql = "SELECT * FROM following WHERE username1='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]['numFollowing'] = len(cur.fetchall())
    sql = "SELECT username2 FROM following WHERE username1='%s' AND username2='%s'" % (currUser, user_slug)
    cur = connection.execute(sql)
    userData[0]['relation'] = cur.fetchall()
    sql = "SELECT * FROM following WHERE username2='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]['numFollowers'] = len(cur.fetchall())
    context = {"UserData": userData}
    return flask.render_template("user.html", **context)