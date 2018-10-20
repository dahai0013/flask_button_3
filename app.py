import threading
import subprocess
import uuid
from flask import Flask
from flask import render_template, url_for, abort, jsonify, request
app = Flask(__name__)

background_scripts = {}

def run_script(id):
    subprocess.call(["/path/to/yourscript.py", "argument1", "argument2"])
    background_scripts[id] = True

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
        return render_template('command.html', command=command )
    return render_template('index.html')

@app.route('/generate')
def generate():
    id = str(uuid.uuid4())
    background_scripts[id] = False
    threading.Thread(target=lambda: run_script(id)).start()
    return render_template('processing.html', id=id)

@app.route('/is_done')
def is_done():
    id = request.args.get('id', None)
    if id not in background_scripts:
        abort(404)
    return jsonify(done=background_scripts[id])

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(debug=True, port=80)

