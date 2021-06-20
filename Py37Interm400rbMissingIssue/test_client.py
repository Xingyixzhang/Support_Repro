
import logging
import requests
import json

logging.basicConfig(filename='output.log', level=logging.DEBUG)


def gen():
    """Generator function that is used to force chunked encoding per
    https://docs.python-requests.org/en/master/user/advanced/#chunk-encoded-requests
    """

    body = {
        "name": "xCloud-e73333a5-c1bc-42b1-bb54-e64c0b6cd542-773",
        "description": "Members of this group have permissions with AstroRole_SelfAssigned role \"AccountManager\" (773) in xCloud account \"oli-test-non-prod-5\" (e73333a5-c1bc-42b1-bb54-e64c0b6cd542)",
        "ownerIDs": [
            "8408c18e-3705-47f6-abd3-222aa8448170",
            "095b32af-1ca7-4ff4-a01e-1d8ad3dccb04"
        ],
        "memberIDs": [
            "7a96a927-e7e4-4dfc-9079-114f9b55e92f"
        ],
        "comcast_xcloudroles": {
            "accountId": "e73333a5-c1bc-42b1-bb54-e64c0b6cd542",
            "roleId": 773,
            "roleName": "AccountManager",
            "roleType": "AstroRole_SelfAssigned",
            "environment": "PROD"
        }
    }
    j = json.dumps(body).encode('utf-8')
    # can be used to split the request into 2 pars if desired
    split_len = round(len(j) / 2)
    pt1 = j[0:split_len]
    pt2 = j[split_len:] # remove -1 in [split_len:-1]
    yield pt1
    yield pt2

    # yield j
    # yield ''


# edit this to point to your endpoint
# url = 'https://aadgroupcreateprod.azurewebsites.net/api/createGroups_copy' # Customer testing endpoint.
url = 'https://py37intermRBmissingRepro.azurewebsites.net/api/HttpTrigger1'

total_requests = 50
number_of_400 = 0

for number in range(total_requests):
    response = requests.post(url, data=gen())
    status = response.status_code
    if status == 400:
        number_of_400 += 1

    # print(f'response: {response.status_code}')
    # print(f'body: {response.text}')

print(f"Total Requests Count: {total_requests}")
print(f"Failed Requests Count: {number_of_400}")