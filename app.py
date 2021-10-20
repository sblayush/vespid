import os
from flask import Flask, request, render_template
import json
import subprocess

_PWD = os.path.dirname(os.path.abspath(__file__))

application = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
application.config['UPLOAD_FOLDER'] = _PWD

_TEMP_PATH = "{}/temp".format(_PWD)
_CODE_PATH = "{}/virts/c".format(_PWD)
_EXEC_PATH = "{}/virts/exec".format(_PWD)


def insert_code(vname, vcode):
    func_code = None
    with open("{}/func_temp.c".format(_TEMP_PATH), 'r') as f:
        func_code = f.read()
    func_code = func_code.replace("####vcode####", vcode)
    func_code = func_code.replace("####vname####", vname)
    with open("{}/func_{}.c".format(_CODE_PATH, vname), 'w') as f:
        f.write(func_code)
    
    with open("{}/{}.h".format(_CODE_PATH, vname), 'w') as f:
        f.write(vcode.split('{')[0] + ";")

    with open("{}/main_temp.c".format(_TEMP_PATH), 'r') as f:
        main_code = f.read()
    main_code = main_code.replace("####vname####", vname)
    with open("{}/main_{}.c".format(_CODE_PATH, vname), 'w') as f:
        f.write(main_code)

def compile_code(vname):
    subprocess.call(['vcc', '{}/func_{}.c'.format(_CODE_PATH, vname), '{}/main_{}.c'.format(_CODE_PATH, vname), '-o', '{}/{}'.format(_EXEC_PATH, vname)])


def execute_code(vname, args):
    args = args.split()
    p = subprocess.Popen(["{}/{}".format(_EXEC_PATH, vname)]+args, stdout=subprocess.PIPE)
    out, err = p.communicate()
    if not err:
        return out.decode()
    else:
        return err.decode()


@application.route("/register", methods=["POST"])
def register():
    if request.method == 'POST':
        if "vname" not in request.form:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
        if "vcode" not in request.form:
            resp = {"resp": "No code data"}
            return json.dumps(resp)
        vname = request.form["vname"]
        vcode = request.form["vcode"]
		
        insert_code(vname, vcode)
        compile_code(vname)

        resp = {"resp": "{} registered successfully".format(vname)}
        return json.dumps(resp)


@application.route("/execute", methods=["POST"])
def execute():
    if request.method == 'POST':
        if "vname" not in request.form:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
        if "args" not in request.form:
            resp = {"resp": "No args data"}
            return json.dumps(resp)
        vname = request.form["vname"]
        args = request.form["args"]
		
        res = execute_code(vname, args)

        resp = {"resp": res}
        return json.dumps(resp)


@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0',  port=8989)
