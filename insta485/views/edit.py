import flask
import insta485
import pdb
import uuid
import pathlib
import hashlib
from urllib.parse import urlparse
algorithm = 'sha512'
salt = 'a45ffdcc71884853a2cba9e6bc55e812' # salt used from the spec **for easy testing.**
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

#update SQL based on submission form:
@insta485.app.route('/accounts/edit/', methods=['POST'])
def update_profile():
    operation = flask.request.form['operation']
    if operation == "edit_account":
        curr_user = flask.session['username']
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        URL = flask.request.args.get('target')
        # Compute base name (filename without directory).  We use a UUID to avoid
        # clashes with existing files, and ensure that the name is compatible with the
        # filesystem.
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
        connection = insta485.model.get_db()
        cur = connection.execute("UPDATE users SET fullname='%s', email='%s', filename='%s' WHERE username='%s'" % params)
    #CHECK LATER
    #breakpoint()
    return flask.redirect(URL)

@insta485.app.route('/accounts/password/', methods=['GET'])
def show_edit_password():
    username = flask.session['username']
    context = {"edit": username}
    return flask.render_template("editPassword.html")

def salt_pass(password):
    password_salted = salt + password
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string

@insta485.app.route('/accounts/password/', methods=['GET'])
def update_edit_password():
    URL = flask.request.args.get('target')
    operation = flask.request.form['operation']
    if operation == "update_password":
        connection = insta485.model.get_db()
        username = flask.session['username']
        password = flask.request.form['password']
        if not password:
            flask.abort(400, "Password field was empty")
        password_db_string = salt_pass(password)
        params = (username, password_db_string)
        #print(password_db_string)
        cur = connection.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % params)
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
        sql = "UPDATE users SET password ='%s' WHERE username='%s'" % (password_db_string, username)
        cur = connection.execute(sql)
        #REDO LATER TO IMPLEMENT TARGET VARIABLE
        return flask.redirect(URL)
    #CHECK LATER
    #breakpoint()
    return flask.redirect(URL)