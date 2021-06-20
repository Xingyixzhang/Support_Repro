### Issue
Python 3.7 HTTP function intermittently fail with 400 Bad Request "HTTP request does not contain valid JSON data", even with the same valid JSON request body.

**Testing Function App**: [py37intermRBmissingRepro](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/EPlinux/providers/Microsoft.Web/sites/py37intermRBmissingRepro/appServices)

### Demo
**----- Hardcoded Valid JSON Request Body for all tests -----**
```JSON
body = {
        "name": "xxxxxxxxxxxxxxxxxx",
        "description": "xxxxxxxxxxxxxx \"AccountManager\" (773) in xCloud account \"prod_account\" (xxxx-xxxx-xxxxxx)",
        "ownerIDs": [
            "8408xxxx-xxxx-xxxxxx",
            "095bxxxx-xxxx-xxxxxx"
        ],
        "memberIDs": [
            "7a96xxxx-xxxx-xxxxxx"
        ],
        "comcast_xcloudroles": {
            "accountId": "e733xxxx-xxxx-xxxxxx",
            "roleId": 1001,
            "roleName": "AccountManager",
            "roleType": "SelfAssigned",
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
![Failed Requests Count Demo](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/failed_requests_count.png)

**----- Comparing the responses of 400 and 200 requests -----**
``` py
url = 'https://py37intermRBmissingRepro.azurewebsites.net/api/HttpTrigger1'

total_requests = 10
number_of_400 = 0

for number in range(total_requests):
    response = requests.post(url, data=gen())
    status = response.status_code
    if status == 400:
        number_of_400 += 1

    print(f'response: {response.status_code}')
    print(f'body: {response.text}')

print(f"Total Requests Count: {total_requests}")
print(f"Failed Requests Count: {number_of_400}")
```
![Failed vs Successful Request Body print](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/failed_message_vs_successful_body.png)

### Additional Notes
- This issue seemed to be related to chunked encoding based on Network Trace / TCP dumps analysis.
- [Reported] For the same code, this issue only started happening on and after Early April 2021.
