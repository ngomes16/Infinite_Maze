from flask import Flask, render_template, request
import requests,os


def setup():
  name = os.getenv("MG_NAME")
  author = os.getenv("AUTHOR")
  url = os.getenv("URL")
  mw_url = os.getenv("MW_URL")
  mg_type = os.getenv("MG_TYPE")
  print(mg_type)
  r = requests.put(f'{mw_url}/addMG', json={'name':name,'author':author,'url':url})
  print(r.text)

app = Flask(__name__)
setup()

# Route for maze generation:
@app.route('/generate', methods=["GET"])
def GET_maze_segment():
  args = request.args

  return {
    "geom": ["9aa2aac", "59aaaa4", "51aa8c5", "459a651", "553ac55", "559a655", "3638a26"]
  }
