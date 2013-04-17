from flask import Flask, request, abort, jsonify


# Create the application
app = Flask(__name__)


@app.route('/')
def api_root():
    abort(401)


@app.route('/auth')
def auth():
    if request.args.get('key') == "TESTAUTHCODE":
        success_auth_correct = {"code": 200, "message": "Authorization successful"}
        return jsonify(success_auth_correct)
    else:
        error_auth_req = {"code": 401, "message": "Authentication required"}
        return jsonify(error_auth_req), 401


@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    if request.args.get('key') == "TESTAUTHADMINCODE":
        accounts = {"accounts": []}
        return jsonify(accounts)
    else:
        error_auth_req = {"code": 401, "message": "Authentication required"}
        return jsonify(error_auth_req), 401
