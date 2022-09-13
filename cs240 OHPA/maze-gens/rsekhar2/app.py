from flask import Flask, request
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

# Static route:
@app.route('/generate', methods=["GET"])
def GET_maze_segment():
    args = request.args

    return {
        "geom": ["9a80e9c", "5d57d34", "75180a6", "84571e9", "555b284", "536dd75", "3aa43a6"]
    }
