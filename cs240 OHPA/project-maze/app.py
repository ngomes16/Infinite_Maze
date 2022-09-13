from flask import Flask, render_template, request, session, redirect, url_for
import requests, os, time, uuid

app = Flask(__name__)
app.secret_key = "34ed754dcd4546ab8dfdce7b6994f869"

from pymongo import MongoClient, DESCENDING
mongo = MongoClient('localhost', 8080)
db = mongo["db"]

# Route for "/" (frontend):
@app.route('/', methods=["GET"])
def index():
  return render_template("index.html")


@app.route('/login', methods = ['GET', 'POST'])
def login():
  if 'username' in session:
    username = session['username']
    return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
  if request.method == 'POST':
    session['username'] = request.form['username']
    db.users.replace_one(filter={'username': session['username']}, replacement={'username': session['username'], 'active': True}, upsert=True)
    return redirect(url_for('index'))
  return render_template('login.html')


@app.route('/logout')
def logout():
  if 'username' not in session:
    return 'Not logged in', 400
  # remove the username from the session if it is there
  db.users.replace_one(filter={'username': session['username']}, replacement={'username': session['username'], 'active': False})
  session.pop('username')
  return redirect(url_for('index'))

# Route for MG registry:
@app.route('/mg/register', methods=["PUT"])
def register_mg():
  json = request.json
  if 'name' not in json or 'author' not in json or 'url' not in json:
    return 'Bad registry', 400
  db.mg.insert_one(json)
  return f"Registered {json['name']} by {json['author']}", 200


cache_max_age = int(os.getenv('CACHE_MAX_AGE'))
mg_metadata_props = ["name","author","url","type"]

# Route for maze generation:
@app.route('/generateSegment', methods=["POST"])
def generate_segment():
  req_json = request.json
  segment = {
    "id": uuid.uuid4().hex,
    "origin": req_json['origin']
  }
  req_json.pop('origin')

  while db.mg.count_documents({}) > 0:
    mg_info = list(db.mg.aggregate([{"$sample":{"size":1}}]))[0]
    mg_info = {prop: mg_info[prop] for prop in mg_metadata_props}
    url = mg_info['url']
    mg_type = mg_info['type']

    if mg_type == 'static':
      doc = db.static_maze_cache.find_one({'metadata': mg_info})
      if doc is not None:
        age = int(time.time()) - doc['cached_at']
        if age < cache_max_age:
          segment['data'] = doc['data']
          segment['metadata'] = mg_info
          db.segments.insert_one(segment)
          segment.pop('_id')
          return segment, 200, {'cache-control':f'max-age={cache_max_age}', 'age': age}

    try:
      res = requests.post(f'{url}/generateSegment', json=req_json)
      segment['data'] = res.json()
      segment['metadata'] = mg_info
      db.segments.insert_one(segment)
      segment.pop('_id')
      if mg_type == 'static':
        db.static_maze_cache.replace_one(filter={'metadata': mg_info}, replacement={'metadata': mg_info, 'data': segment['data'], 'cached_at': int(time.time())}, upsert=True)
      return segment, 200, {'cache-control':f'max-age={cache_max_age}', 'age': 0}
    except requests.exceptions.ConnectionError:
      db.mg.delete_one(mg_info)
      print(f"Removed {mg_info['name']} by {mg_info['author']} (unreachable)")
  return "No maze generators", 500


@app.route('/visit', methods=["POST"])
def visit():
  form = request.form
  if 'username' not in session:
    return 'Not logged in', 400
  if 'locations' not in db.list_collection_names():
    result = db.locations.create_index([('version', DESCENDING)], unique=True)
  latest = db.locations.find_one(sort=[('version', DESCENDING)])
  version = 1 + (latest['version'] if latest is not None else 1)
  db.locations.insert_one({'username': session['username'], 'x': request.form['x'], 'y': request.form['y'], 'version': version})
  return 'Visited'


@app.route('/history/<username>', methods=["GET"])
def history(username):
  if db.users.find_one({'username':username}) is None:
    return 'Not a user', 400
  if 'locations' not in db.list_collection_names():
    return 'No history', 404
  locations = list(db.locations.find({'username': username},sort=[('version', DESCENDING)]).limit(50))
  history = [{'x': loc['x'], 'y': loc['y']} for loc in locations]
  return {'history': history}

@app.route('/render')
def render():
  segments = list(db.segments.find())
  for i, segment in enumerate(segments):
    segment.pop('_id')
  usernames = [user['username'] for user in db.users.find()]
  print(usernames)
  locations = list(filter(None, [db.locations.find_one({'username': username},sort=[('version', DESCENDING)]) for username in usernames]))
  for i, location in enumerate(locations):
    location.pop('_id')
    location.pop('version')
  return {"segments": segments, "locations": locations}

