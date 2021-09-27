"""
Insta485 like (main) view.

URLs include:

"""
# import pdb
import flask
import insta485
# import uuid
# import pathlib
# import hashlib
# from urllib.parse import urlparse


# render edit page:
@insta485.app.route('/accounts/edit/', methods=["GET"])
def show_edit():
    """Render the edit template."""
    connection = insta485.model.get_db()
    curr_user = flask.session['username']
    sql = "SELECT * FROM users WHERE username='%s'" % (curr_user)
    cur = connection.execute(sql)
    edit = cur.fetchall()
    context = {"edit": edit}
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/', methods=['GET'])
def show_edit_password():
    """Render the edit password template."""
    # username = flask.session['username']
    # context = {"edit": username}
    return flask.render_template("editPassword.html")
