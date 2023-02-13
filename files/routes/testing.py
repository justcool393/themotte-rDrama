import sys
from typing import Optional

from flask import abort, g, request, make_response

from files.classes.comment import Comment
from files.classes.user import User
from files.helpers.comments import comment_on_publish
from files.helpers.const import SITE
from files.helpers.get import get_comment
from files.helpers.strings import bool_from_string
from files.helpers.wrappers import get_logged_in_user
from files.__main__ import app, limiter

def allowed_to_test():
	def wrapper_maker(f):
		def wrapper(*args, **kwargs):
			v:Optional[User] = get_logged_in_user()
			if not v: abort(401)
			if v.admin_level < 3: abort(403)
			if v.id != 11: abort(403, 'nope lol')
			if request.referrer and SITE not in request.referrer:
				print(f'bad bad bad ({request.referrer})')
				abort(403)
			return make_response(f(*args, v=v, **kwargs))

		wrapper.__name__ = f.__name__
		return wrapper

	return wrapper_maker

@app.get('/testing/ratelimits/<value>')
@allowed_to_test()
def testing_clearratelimits(v: User, value: str):
	limiter.enabled = bool_from_string(value)
	return 'done!'

@app.get('/testing/environment')
@allowed_to_test()
def testing_environment(v: User):
	return f'{sys.version}'

@app.get('/testing/make_comments/<int:id>/')
@allowed_to_test()
def testing_make_comments(v: User, id: int):
	c: Comment = get_comment(id)
	count: int = request.values.get('count', 0, int) or 0
	for _ in range(0, count + 1):
		level: int = c.level + 1 # type: ignore
		reply = Comment(author_id=v.id,
				parent_submission=c.parent_submission,
				parent_comment_id=c.id,
				level=level,
				over_18=False,
				is_bot=False,
				app_id=v.client.application.id if v.client else None,
				body_html=f'<p>{level}</p>',
				body=str(level),
				ghost=False,
				filter_state='normal',
				top_comment_id=c.top_comment_id,
		)
		if reply.level == 1: reply.top_comment_id = reply.id
		else: reply.top_comment_id = c.top_comment_id
		g.db.add(reply)
		g.db.flush()
		comment_on_publish(reply)
		#print(f"making comment with level {reply.level} (TCID {reply.top_comment_id}, parent ID {reply.parent_comment_id})")
		c = reply
	g.db.commit()
	return f'<h1>done (level {c.level}, id {c.id}, count {count}).</h1><h1><a href="/testing/make_comments/{c.id}/?count={count}">make more comments (current id {c.id})</a></h1>'
