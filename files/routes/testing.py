from flask import abort, g, request

from files.classes.comment import Comment
from files.classes.user import User
from files.helpers.comments import comment_on_publish
from files.helpers.get import get_comment
from files.helpers.wrappers import admin_level_required
from files.__main__ import app, cache

@app.get('/testing/make_comments/<int:id>/')
@admin_level_required(3)
def testing_make_comments(v: User, id: int):
	if v.id != 11: abort(403, 'nope lol')

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
		print(f"making comment with level {reply.level} (TCID {reply.top_comment_id}, parent ID {reply.parent_comment_id})")
		c = reply
	g.db.commit()
	cache.
	return 'done...'
