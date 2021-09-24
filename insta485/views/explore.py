import flask
import insta485

@insta485.app.route('/explore/', methods=["GET"])
def show_explore():
    currUser = flask.session['username']
    connection = insta485.model.get_db() #username is a primary key. 
    sql = "SELECT username FROM users WHERE username NOT in (SELECT username2 FROM following WHERE username1='%s')"  % (currUser)
    #Select username2 from following where username1 does not follow username2
    #  
    cur = connection.execute(sql)
    exploreData = cur.fetchall()
    context = {"not_following": exploreData}
    return flask.render_template("explore.html", **context)