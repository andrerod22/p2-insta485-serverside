"""
Comment (main) view.

URLs include:
/
/posts/post_url_slug
"""
import datetime
import flask
import insta485


@insta485.app.route('/comments/', methods=['POST'])
def update_user_comment():
    """Increment Comment Table with New Like."""
    operation = flask.request.form['operation']
    curr_user = flask.session['username']
    target = flask.request.args.get('target')
    if target is None:
        url = '/'
    elif '/posts/' in target:
        url = target
    elif '/posts/' not in target:
        url = '/posts/' + str(target) + '/'
    else:
        url = '/'
    connection = insta485.model.get_db()
    if operation == 'create':
        postid = flask.request.form['postid']
        text = flask.request.form['text']
        if text is None:
            flask.abort(400)
        time_stamp = datetime.datetime.utcnow()
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO comments
         (owner, postid, text, created) VALUES ('%s', '%s', '%s', '%s')
         """ % (curr_user, postid, text, time_stamp)
        cur = connection.execute(sql)

    elif operation == 'delete':
        commentid = flask.request.form['commentid']
        sql = "SELECT owner FROM comments WHERE commentid='%s'" % (commentid)
        cur = connection.execute(sql)
        comment_owner = cur.fetchone()
        comment_owner = comment_owner['owner']

        if curr_user != comment_owner:
            flask.abort(403, "Can't delete other user's comment")
        sql = """DELETE FROM comments WHERE commentid='%s'
         AND owner='%s'""" % (commentid, curr_user)
        cur = connection.execute(sql)

    if target == '/':
        return flask.redirect('/')
    return flask.redirect(url)
