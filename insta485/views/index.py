"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'), code=200) #302

    # Connect to database
    # connection = insta485.model.get_db()

    # Query database
    # cur = connection.execute(
    #     "SELECT username, fullname "
    #     "FROM users"
    # )
    # users = cur.fetchall()

    # Add database info to context
    # context = {"users": users}

    # return flask.render_template("index.html", **context)
    return flask.render_template("index.html")