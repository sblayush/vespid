import os
from flask import Flask, request, render_template
from api.actions.CAction import CAction
from api.actions.JSAction import JSAction
import json

application = Flask(__name__, static_url_path="/static")


@application.route("/actions/<vname>/create", methods=["POST"])
def create(vname):
    if request.method == 'POST':
        if not vname:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
        if "vcode" not in request.form:
            resp = {"resp": "No code data"}
            return json.dumps(resp)
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


@application.route("/actions/<vname>/invoke", methods=["POST"])
def invoke(vname):
    if request.method == 'POST':
        if not vname:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
        if "args" not in request.form:
            resp = {"resp": "No args data"}
            return json.dumps(resp)
        args = request.form["args"]
		
        if vname not in actions_map:
            resp = {"resp": "Action '{}' does not exist".format(vname)}
            return json.dumps(resp)

        act = actions_map[vname]
        res = act.invoke(args)

        resp = {"resp": res}
        return json.dumps(resp)

@application.route("/actions/<vname>/get", methods=["GET"])
def get(vname):
    if request.method == 'GET':
        if not vname:
            resp = {"resp": "No vname data"}
            return json.dumps(resp)
		
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
