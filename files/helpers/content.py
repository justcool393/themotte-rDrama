from typing import Optional
from files.helpers.const import PERMS

def censored_text(target, v) -> Optional[str]:
	'''
	Returns text to be used in place of a removed or deleted comment.
	'''
	if v and (v.admin_level >= PERMS['POST_COMMENT_MODERATION'] or v.id == target.author_id):
		return None
	if target.deleted_utc: return "[Deleted by user]"
	if target.author.shadowbanned: return "[Deleted by user]"
	if target.is_banned or target.filter_state in ('filtered', 'removed',): 
		return "[Removed by admins]"
	return None

def is_publicly_visible(target):
	if target.deleted_utc: return False
	if target.is_banned or target.filter_state in ('filtered', 'removed',):
		return False
	if target.author.shadowbanned: return False
	return True
