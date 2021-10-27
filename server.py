from flask import Flask, send_from_directory,request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('public', path)


@app.route("/rand")
def hello():
    return str(random.randint(0, 100))



@app.route("/execute_order",methods=["POST"])
def execute():
    print(request.get_json())
    return "success"
if __name__ == "__main__":
    app.run(debug=True)