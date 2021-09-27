"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/explore/', methods=["GET"])
def show_explore():
    """Render the explore template."""
    currUser = flask.session['username']
    connection = insta485.model.get_db()  # username is a primary key.
    sql = """SELECT username, filename FROM users
    WHERE username <> '%s' AND username NOT in
    (SELECT username2 FROM following
    WHERE username1='%s')""" % (currUser, currUser)
    cur = connection.execute(sql)
    exploreData = cur.fetchall()
    context = {"not_following": exploreData}
    return flask.render_template("explore.html", **context)
