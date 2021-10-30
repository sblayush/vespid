import os
from flask import Flask, request, render_template
from api.actions.CAction import CAction
from api.actions.JSAction import JSAction
import json

application = Flask(__name__, static_url_path="/static")


@application.route("/actions/create", methods=["POST"])
def create():
    if request.method == 'POST':
        if "vname" not in request.form:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
        if "vcode" not in request.form:
            resp = {"resp": "No code data"}
            return json.dumps(resp)
        vname = request.form["vname"]
        vcode = request.form["vcode"]
        language = 'c'
		
        if vname in actions_map:
            resp = {"resp": "Action already exists"}
            return json.dumps(resp)

        if language == 'c':
            act = CAction()
        else:
            act = JSAction()
        res = act.create(vname, vcode)

        actions_map[vname] = act

        resp = {"resp": res}
        return json.dumps(resp)


@application.route("/actions/invoke", methods=["POST"])
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
		
        if vname not in actions_map:
            resp = {"resp": "Action '{}' does not exist".format(vname)}
            return json.dumps(resp)

        act = actions_map[vname]
        res = act.invoke(args)

        resp = {"resp": res}
        return json.dumps(resp)

@application.route("/actions/get", methods=["GET"])
def get():
    if request.method == 'GET':
        if "vname" not in request.form:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
        vname = request.form["vname"]
		
        if vname not in actions_map:
            resp = {"resp": "Action '{}' does not exist".format(vname)}
            return json.dumps(resp)

        act = actions_map[vname]
        res = act.get()

        resp = {"resp": res}
        return json.dumps(resp)


@application.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    from api.initialize import initialize
    actions_map = {}
    application.debug = True
    application.run(host='0.0.0.0',  port=8989)
