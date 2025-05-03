from flask import Flask, render_template
import os

"""
from flask_cors import CORS
import sys
ROUTE_PATH = sys.path[1] if 2 == len(sys.path) else '.'
TEMPLATES_PATH = ROUTE_PATH + '/templates'
app = Flask(__name__, template_folder=TEMPLATES_PATH)
app.config['JSON_AS_ASCII'] = False
CORS(app)

print(os.getcwd())
root_folder = os.path.dirname(os.getcwd())
print(root_folder)
"""
app = Flask(__name__, static_folder = os.getcwd() + '\\static', template_folder = os.getcwd() + '\\templates')

"""
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/test")
def test():
    hello = "Hello world"
    return hello

if __name__ == "__main__":
    app.run()

"""

@app.route("/")
def test():
    hello = "Hello world"
    return hello


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)