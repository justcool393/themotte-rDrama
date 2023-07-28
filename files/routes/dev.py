from secrets import token_hex
from flask import session, redirect, request

from files.helpers.config.const import PERMS
from files.helpers.get import get_user
from files.helpers.wrappers import admin_level_required
from files.__main__ import app

if not app.debug:
	raise ImportError("Importing dev routes is not allowed outside of debug mode!")

@app.post('/dev/sessions/')
@admin_level_required(PERMS['DEBUG_LOGIN_TO_OTHERS'])
def login_to_other_account(v):
	u = get_user(request.values.get('username'))
	session.permanent = True
	session["lo_user"] = u.id
	session["login_nonce"] = u.login_nonce
	session["session_id"] = token_hex(49)
	return redirect('/')
