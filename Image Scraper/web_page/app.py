import os
import subprocess
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/submit-form", methods=["POST"])
def submit_form():
    # get values from form
    x1 = request.form["x1"]
    z1 = request.form["z1"]
    x2 = request.form["x2"]
    z2 = request.form["z2"]

    # display loading icon
    response = jsonify({"message": "Running program"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'no-cache')
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('X-Accel-Buffering', 'no')
    return response

    # run Python program
    subprocess.call(["python", "program.py", x1, z1, x2, z2])

    # get output file name
    files = os.listdir(".")
    files.sort(key=os.path.getmtime) # sort by modification time
    last_file = files[-1]

    # return output file
    return send_file(last_file)