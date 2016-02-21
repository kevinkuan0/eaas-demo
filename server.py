from flask import Flask
from flask import request
from flask.ext.cors import CORS
import json
import untitled0

app = Flask(__name__)
CORS(app)

@app.route("/energy", methods=['POST'])
def hello():
    try:
        post_data =  json.dumps(request.json)
        data = json.loads(post_data)
    except Exception as e:
        print (str(e))

    src = data['src']
    dst = data['dst']
    energy_j = untitled0.getAll(src['lat'], src['lng'], dst['lat'], dst['lng'], False)
    
    return energy_j
@app.route("/", methods=['GET'])
def test():
    return "Hello world!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=23456)
