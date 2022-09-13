from flask import Flask, render_template, request
import requests, os, random


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

def lay(a, b, top, left):
  b = [list(row) for row in b]
  for i in range(len(a)):
    for j in range(len(a[0])):
      b[i+top][j+left] = hex(int(b[i+top][j+left], 16) | int(a[i][j], 16))[2]
  b = [''.join(row) for row in b]
  return b



# Route for maze generation:
@app.route('/generate', methods=["GET"])
def GET_maze_segment():
  args = request.args
  
  topleft = random.randint(1,4)
  width = random.randint(2, 6 - topleft)
  rect = ['1'+'0'*(width-2)+'4']*width
  rect[0] = '9' + '8'*(width-2) + 'c'
  rect[-1] = '3' + '2'*(width-2) + '6'
  base = ["988088c", "1000004", "1000004","0000000", "1000004", "1000004", "3220226"]

  return {
    "geom": lay(rect,base,topleft,topleft)
  }
