import flask
import insta485

@insta485.app.route('/users/<user_slug>/', methods=["GET"])
def show_user(user_slug):
    #currUser = flask.session['username']
    sql = "SELECT * FROM users WHERE username='%s'" % (user_slug)
    connection = insta485.model.get_db()
    cur = connection.execute(sql)
    userData = cur.fetchall() # LIST, should be
    sql = "SELECT postid FROM posts WHERE owner='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]["numPosts"] = len(cur.fetchall())
    sql = "SELECT * FROM following WHERE username1='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]['numFollowing'] = len(cur.fetchall())
    sql = "SELECT * FROM following WHERE username2='%s'" % (user_slug)
    cur = connection.execute(sql)
    userData[0]['numFollowers'] = len(cur.fetchall())
    #ssql = "SELECT fullname FROM users WHERE username='%s'" % (currUser)
    #cur = connection.execute(sql)
    #userData['fullname'] = cur.fetchall()
    context = {"UserData": userData} 
    #breakpoint()
    return flask.render_template("user.html", **context)