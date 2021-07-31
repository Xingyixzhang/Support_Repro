from flask import Flask, request
app = Flask(__name__)

# GET requests will be blocked
# @app.route('/', methods=['POST'])
@app.route("/", methods=['GET', 'POST'])
def json_test():
    request_data = request.get_json()

    name = None
    memberID = None
    accountId = None
    roleName = None
    roleType = None

    if request_data:
        if 'name' in request_data:
            name = request_data['name']

        if 'memberID' in request_data:
            memberID = request_data['memberID']

        if 'accountId' in request_data:
            accountId = request_data['accountId']

        if 'roleName' in request_data:
            roleName = request_data['roleName']

        if 'roleType' in request_data:
            roleType = request_data['roleType']

    return '''
           Hi {}, your Member ID is {},
           Account ID {}
           You are a {} {}.
           '''.format(name, memberID, accountId, roleType, roleName)
