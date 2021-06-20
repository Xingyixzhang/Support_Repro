### Issue
Python 3.7 HTTP function intermittently fail with 400 Bad Request "HTTP request does not contain valid JSON data", even with the same valid JSON request body.

**Testing Function App**: [py37intermRBmissingRepro](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/EPlinux/providers/Microsoft.Web/sites/py37intermRBmissingRepro/appServices)

### Demo
**----- Hardcoded Valid JSON Request Body for all tests -----**
```JSON
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
```

**----- Normally about 10 out of 50 requests fail with 400 Bad Requests -----**
```py
# edit this to point to your endpoint
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
```
