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
import insta485
import uuid
import hashlib
import pathlib
import datetime
import pdb

algorithm = 'sha512'
salt = 'a45ffdcc71884853a2cba9e6bc55e812' # salt used from the spec **for easy testing.**
# salt = uuid.uuid4().hex Maybe uncomment this line later, because salt is always generated randomly. 


@insta485.app.route('/accounts/', methods=["POST"])
def account_redirect():
    #Gets form data from login.html
    operation = flask.request.form['operation']
    target = flask.request.args.get('target')

    if operation == 'login':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if not username or not password:
            flask.abort(400, "Username or Password field was empty")
        password_salted = salt + password
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        connection = insta485.model.get_db()
        params = (username, password_db_string)
        print(password_db_string)
        cur = connection.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % params)
        user = cur.fetchone()
        if user is None:
            flask.abort(403, "Invalid Username and Password Combination")
        flask.session['username'] = username
        
    elif operation == 'create':
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        # Compute base name (filename without directory).  We use a UUID to avoid
        # clashes with existing files, and ensure that the name is compatible with the
        # filesystem.
        uuid_basename = "{stem}{suffix}".format(
            stem=uuid.uuid4().hex,
            suffix=pathlib.Path(filename).suffix
            )
        fullname = flask.request.form['fullname']
        username = flask.request.form['username']
        email = flask.request.form['email']
        password = flask.request.form['password']
        time_stamp = datetime.datetime.utcnow()
        password_salted = salt + password
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(password_salted.encode('utf-8')) #turns salted password into bits
        password_hash = hash_obj.hexdigest() 
        password_db_string = "$".join([algorithm, salt, password_hash])
        if not (username and password and fullname and email and uuid_basename):
            flask.abort(400, "One or more of the required fields are empty.")
        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        params = (username, fullname, email, uuid_basename, password_db_string, time_stamp.strftime('%Y-%m-%d %H:%M:%S'))
        connection = insta485.model.get_db()
        cur = connection.execute("SELECT * FROM users WHERE username = '%s'" % username)
        user = cur.fetchone()
        if user is not None:
            flask.abort(409, "Username already taken")
        cur = connection.execute("INSERT INTO users(username,fullname,email,filename,password,created) VALUES('%s','%s','%s','%s','%s','%s')" % params)
        flask.session['username'] = username
    if target == '':
        return flask.redirect("/")
    #TODO Other operations like account create, edit, etc. Refer to spec. 


@insta485.app.route('/accounts/login/', methods=["GET"])
def show_login():
    if 'username' in flask.session: #If the user is already logged in, redirect back to index.
        return flask.redirect("/")
    return flask.render_template("login.html")

@insta485.app.route('/accounts/logout/', methods=["POST"])
def logout():
    return flask.redirect("/")

@insta485.app.route('/accounts/create/', methods=["GET"])
def show_create():
    return flask.render_template("create.html")