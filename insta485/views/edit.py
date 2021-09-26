import flask
import insta485
import pdb
import uuid
import pathlib
import hashlib
from urllib.parse import urlparse


#render edit page:
@insta485.app.route('/accounts/edit/', methods=["GET"])
def show_edit():
    connection = insta485.model.get_db()
    currUser = flask.session['username']
    sql = "SELECT * FROM users WHERE username='%s'" % (currUser)
    cur = connection.execute(sql)
    edit = cur.fetchall()
    context = {"edit": edit}
    #breakpoint()
    return flask.render_template("edit.html", **context)

@insta485.app.route('/accounts/password/', methods=['GET'])
def show_edit_password():
    username = flask.session['username']
    context = {"edit": username}
    return flask.render_template("editPassword.html")
