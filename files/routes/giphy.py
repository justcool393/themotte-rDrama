from flask import request, jsonify
from os import environ
import requests
from files.helpers.wrappers import auth_required

from files.__main__ import app

GIPHY_KEY = environ.get('GIPHY_KEY').rstrip()


@app.get("/giphy")
@app.get("/giphy<path>")
@auth_required
def giphy(v, path=None):

	searchTerm = request.values.get("searchTerm", "").strip()
	limit = int(request.values.get("limit", 48))
	if searchTerm and limit:
		url = f"https://api.giphy.com/v1/gifs/search?q={searchTerm}&api_key={GIPHY_KEY}&limit={limit}"
	elif searchTerm and not limit:
		url = f"https://api.giphy.com/v1/gifs/search?q={searchTerm}&api_key={GIPHY_KEY}&limit=48"
	else:
		url = f"https://api.giphy.com/v1/gifs?api_key={GIPHY_KEY}&limit=48"
	return jsonify(requests.get(url, timeout=5).json())
