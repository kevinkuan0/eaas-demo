from flask import Flask
from flask import request
from flask.ext.cors import CORS
import json

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

    return "Hello World!\n"
@app.route("/", methods=['GET'])
def test():
    return "Hello world!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=23456)
