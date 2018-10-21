import threading
import subprocess
import uuid
from flask import Flask
from flask import render_template, url_for, abort, jsonify, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#when the html page send the GET IP@/send, if will be capture by this one
@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST':
        ipaddress = request.form['ipaddress']
        script_name = request.form['script_name']
        argument1 = request.form['argument1']
        argument2 = request.form['argument2']
        command = 'python ' + script_name +' '+ ipaddress +' '+ argument1 +' '+ argument2

        #
        script_output = subprocess.call("python hello_world.py")

        return render_template('index.html', script_output=script_output , command=command )
    return render_template('index.html')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(debug=True, port=80)

