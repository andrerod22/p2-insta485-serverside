import flask
import insta485
import pdb
import uuid
import pathlib
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
    return flask.redirect(URL)

