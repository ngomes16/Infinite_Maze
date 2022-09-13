import random
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
    strings = ["988088c", "1000004", "1000004",
               "0000000", "1000004", "1000004", "3220226"]
    random_string = random.randint(1, 5)
    random_char = random.randint(0, 5)
    intify = int(strings[random_string][random_char])
    intify += 8
    final_char = str(intify)
    strings[random_string] = strings[random_string][:random_char] + \
        final_char + strings[random_string][random_char+1:]

    return {
        "geom": strings
    }
