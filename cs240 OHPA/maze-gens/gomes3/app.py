from flask import Flask, render_template, request
import requests,os


def setup():
  name = os.getenv("MG_NAME")
  author = os.getenv("AUTHOR")
  url = os.getenv("URL")
  mw_url = os.getenv("MW_URL")
  mg_type = os.getenv("MG_TYPE")
  r = requests.put(f'{mw_url}/addMG', json={'name':name,'author':author,'url':url})
  print(r.text)

app = Flask(__name__)
setup()

# Route for maze generation:
@app.route('/generate', methods=["GET"])
def GET_maze_segment():
  args = request.args

  return {
    "geom": ["988288c", "1228224", "59a0ac5", "41d5b41", "53a0a65", "1a82a84", "32a8a26"]
  }
