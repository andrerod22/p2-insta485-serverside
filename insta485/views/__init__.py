"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.index import serve_img
from insta485.views.accounts import show_login
from insta485.views.accounts import account_redirect
from insta485.views.accounts import logout
from insta485.views.accounts import show_delete
from insta485.views.comments import update_user_comment
from insta485.views.likes import update_likes
from insta485.views.explore import show_explore
from insta485.views.users import show_user
from insta485.views.follow import follow_redirect
from insta485.views.post import show_post
from insta485.views.post import post_redirect
from insta485.views.users import show_user
from insta485.views.edit import show_edit