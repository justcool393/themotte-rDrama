from flask import abort, g, request

from files.classes.comment import Comment
from files.classes.user import User
from files.helpers.get import get_comment
from files.helpers.wrappers import admin_level_required
from files.__main__ import app

@app.get('/testing/make_comments/<int:id>/')
@admin_level_required(3)
def testing_make_comments(v: User, id: int):
	if v.id != 11: abort(403, 'nope lol')
	c: Comment = get_comment(id)
	count: int = request.values.get('count', 0, int) or 0
	for _ in range(count, 0, -1):
		level: int = c.level # type: ignore
		c = Comment(author_id=v.id,
				parent_submission=c.parent_submission,
				parent_comment_id=c.id,
				level=level + 1,
				over_18=False,
				is_bot=False,
				app_id=v.client.application.id if v.client else None,
				body_html=f'<p>{level + 1}</p>',
				body=level + 1,
				ghost=False,
				filter_state='normal'
		)
		g.db.add(c)
	g.db.commit()
	return 'done...'
