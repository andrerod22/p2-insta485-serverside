"""
Insta485 index (main) view.

URLs include:
/login/
/logout/
/create/
/edit/
/password/
/ immediate redirection to where the user originally wanted to go.
"""
import flask
from flask.helpers import url_for
from werkzeug.utils import redirect
import insta485
import uuid
import hashlib
import pathlib
import datetime
import pdb
from pathlib import Path

ALGORITHM = 'sha512'
# salt used from the spec **for easy testing.**
SALT = 'a45ffdcc71884853a2cba9e6bc55e812'


@insta485.app.route('/accounts/', methods=["POST"])
def account_redirect():
    """Master Function For Redirects."""
    # Gets form data from login.html
    operation = flask.request.form['operation']
    URL = flask.request.args.get('target')
    if operation == 'login':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if not username or not password:
            flask.abort(400, "Username or Password field was empty")
        password_salted = SALT + password
        hash_obj = hashlib.new(ALGORITHM)
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([ALGORITHM, SALT, password_hash])
        connection = insta485.model.get_db()
        params = (username, password_db_string)
        print(password_db_string)
        cur = connection.execute(
                "SELECT * FROM users WHERE username = '%s' AND password = '%s'"
                % params)
        user = cur.fetchone()
        if user is None:
            flask.abort(403, "Invalid Username and Password Combination")
        flask.session['username'] = username
        return flask.redirect('/')
    elif operation == 'create':
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        # Compute base name (filename without directory).
        # We use a UUID to avoid
        # clashes with existing files,
        # and ensure that the name is compatible with the filesystem.
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
            )
        fullname = flask.request.form['fullname']
        username = flask.request.form['username']
        email = flask.request.form['email']
        password = flask.request.form['password']
        time_stamp = datetime.datetime.utcnow()
        password_salted = SALT + password
        hash_obj = hashlib.new(ALGORITHM)
        # turns salted password into bits
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([ALGORITHM, SALT, password_hash])
        if not (
                username and password and fullname and
                email and uuid_basename):
            flask.abort(400, "One or more of the required fields are empty.")
        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        params = (
            username,
            fullname,
            email,
            uuid_basename,
            password_db_string,
            time_stamp.strftime('%Y-%m-%d %H:%M:%S'))
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT * FROM users WHERE username = '%s'" % username)
        user = cur.fetchone()
        if user is not None:
            flask.abort(409, "Username already taken")
        cur = connection.execute(
            """INSERT INTO
                users(username,fullname,email,filename,password,created)
                VALUES('%s','%s','%s','%s','%s','%s')""" % params)
        flask.session['username'] = username
    elif operation == 'delete':
        delete_user = flask.session['username']
        # find user icon filename and delete
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT filename FROM users WHERE username = '%s'" %
            delete_user)
        iconfile = cur.fetchone()['filename']
        iconfilePath = insta485.app.config['UPLOAD_FOLDER']/iconfile
        iconfilePath.unlink()
        cur = connection.execute(
            "SELECT filename FROM posts WHERE owner = '%s'" % delete_user)
        postfileList = cur.fetchall()
        for file in postfileList:
            filePath = insta485.app.config['UPLOAD_FOLDER']/file['filename']
            filePath.unlink()
        cur = connection.execute(
            "DELETE FROM users WHERE username = '%s'" % delete_user)
        flask.session.clear()
    elif operation == 'edit_account':
        connection = insta485.model.get_db()
        curr_user = flask.session['username']
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        URL = flask.request.args.get('target')

        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
            )
        fullname = flask.request.form['fullname']
        email = flask.request.form['email']
        if not (fullname and email and uuid_basename):
            flask.abort(400, "One or more of the required fields are empty.")
        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        params = (fullname, email, uuid_basename, curr_user)
        connection.execute(
            """UPDATE users
               SET fullname='%s', email='%s', filename ='%s'
               WHERE username='%s'""" % params)
    elif operation == 'update_password':
        connection = insta485.model.get_db()
        username = flask.session['username']
        password = flask.request.form['password']
        if not password:
            flask.abort(400, "Password field was empty")
        password_db_string = salt_pass(password)
        params = (username, password_db_string)
        cur = connection.execute(
            """SELECT * FROM users
               WHERE username = '%s'
               AND password = '%s'""" % params)
        user = cur.fetchone()
        if user is None:
            flask.abort(403, "Invalid Password")
        new_pass1 = flask.request.form['new_password1']
        new_pass2 = flask.request.form['new_password2']
        if not new_pass1 or not new_pass2:
            flask.abort(400, "New pass word cannot be empty")
        if new_pass1 != new_pass2:
            flask.abort(401, "New password do not match")
        password_db_string = salt_pass(new_pass1)
        params = password_db_string
        sql = """
            UPDATE users
            SET password ='%s'
            WHERE username='%s'""" % (password_db_string, username)
        cur = connection.execute(sql)
    return flask.redirect(URL)


@insta485.app.route('/accounts/login/', methods=["GET"])
def show_login():
    """Render login template."""
    # If the user is already logged in, redirect to index
    if 'username' in flask.session:
        return flask.redirect("/")
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=["POST"])
def logout():
    """Redirect to login."""
    flask.session.clear()
    return flask.redirect(url_for('show_login'))


@insta485.app.route('/accounts/create/', methods=["GET"])
def show_create():
    """Render create template."""
    return flask.render_template("create.html")


@insta485.app.route('/accounts/delete/', methods=['GET'])
def show_delete():
    """Render delete template."""
    username = flask.session['username']
    context = {"delete": username}
    return flask.render_template("delete.html")


def salt_pass(password):
    """Salting for pw."""
    algorithm = 'sha512'
    # salt used from the spec for easy testing.
    salt = 'a45ffdcc71884853a2cba9e6bc55e812'
    password_salted = salt + password
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
