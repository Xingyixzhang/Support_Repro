### Issue
Python 3.7 HTTP function intermittently fail with 400 Bad Request "HTTP request does not contain valid JSON data", even with the same valid JSON request body.

**Testing Function App**: [py37intermRBmissingRepro](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/EPlinux/providers/Microsoft.Web/sites/py37intermRBmissingRepro/appServices)
---

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
![Failed vs Successful Request Body print](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/failed_body_vs_successful.png)


**----- Looking at Transfer Encoding for both successful and failed responses/ requests -----**
```py
url = 'https://py37intermRBmissingRepro.azurewebsites.net/api/HttpTrigger1'

total_requests = 10
number_of_400 = 0

for number in range(total_requests):
    # request = requests.get(url)
    response = requests.post(url, data=gen())
    status = response.status_code
    if status == 400:
        number_of_400 += 1

    print(f'Response Code: {response.status_code}')
    print(f"Transfer Encoding: {response.headers['transfer-encoding']}\n")

    # print(f'headers: {request.headers.keys()}')
    # print(f"Transfer Encoding: {request.headers['transfer-encoding']}\n")
    # print(f'body: {response.text}')

print(f"Total Requests Count: {total_requests}")
print(f"Failed Requests Count: {number_of_400}")
```

![Transfer Encoding](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/TransferEncoding.png)

---

### Investigation In Progress
**----- Tested on an equivalent app implemented in PowerShell 7 for 1000 times, ALL were SUCCESSFUL-----**
``` ps
$body = @{
    'name' = 'xxxxxxxxxxxxxxxxxx'
    'description' = 'xxxxxxxxxxxxxx'
    "ownerID" = "8408xxxx-xxxx-xxxxxx"
    "memberID" = "7a96xxxx-xxxx-xxxxxx"
    "accountId" = "e733xxxx-xxxx-xxxxxx"
    "roleId" = 1001
    "roleName" = "AccountManager"
    "roleType" = "SelfAssigned"
    "environment" = "PROD"
}

$url = 'https://ps7intermrbmissingrepro.azurewebsites.net/api/httptrigger1'

$total_requests = 1000
$number_of_400 = 0

for ($i = 0; $i -lt $total_requests; $i++){
    $response = Invoke-WebRequest -Uri $url -Body $body -Method 'POST'

    $status_code = $response.StatusCode
    # $transfer_encoding = $response | Select-Object -Property TransferEncoding

    if ($status_code -eq 400){
        $number_of_400++
    }

    # Write-Host "Response Code: $status_code"
    # Write-Host "Transfer Encoding: $transfer_encoding"
}

Write-Host "Total Requests Count: $total_requests"
Write-Host "Failed Requests Count: $number_of_400"
```

![PowerShell App Tests are all Successful](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/PS7all_successful.png)

**----- Tested on an equivalent app implemented in PowerShell 7 for 10 times, with Status Code display-----**

![PowerShell App Tests return 200's](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/200SuccessWith10PSTests.png)

**----- Few more testing with Python req methods indicated same request body intermittently became empty when hitting Python Function endpoint -----**

**Successful Execution 200**
![Success with Request Body](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/Success_with_RequestBody.png)

**Failed with 400: Empty Body**
![Failed with empty body](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/Failed_with_empty_body.png)

### Additional Notes
- This issue seemed to be related to chunked encoding based on Network Trace / TCP dumps analysis.
- 30+ tests with the same request body from Portal Test/Run seemed to be all Successful for both Python and PowerShell functions.
- [Reported] For the same code, this issue only started happening on and after Early April 2021.

![Trace Comparison](https://github.com/Xingyixzhang/Support_Repro/blob/main/Py37Interm400rbMissingIssue/images/trace_comparison.png)

### Resolution / Workaround

**working App Service (Web App)**: [py37intermRBmissingWebApp](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/eplinux/providers/Microsoft.Web/sites/py37intermRBmissingWebApp/appServices)

**Creation Steps**
- Folloing [this doc](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask) and changed app.py code based on the http trigger in original concerning function app.

```cmd
C:\Users\xingyz\Desktop\XingyiTest\python-docs-hello-world>az webapp up --sku B1 --name py37intermRBmissingWebApp --resource-group eplinux --subscription Xingyi-Internal-Subscription
webapp py37intermRBmissingWebApp doesn't exist
Creating webapp 'py37intermRBmissingWebApp' ...
Configuring default logging for the app, if not already enabled
Creating zip with contents of dir C:\Users\xingyz\Desktop\XingyiTest\python-docs-hello-world ...
Getting scm site credentials for zip deployment
Starting zip deployment. This operation can take a while to complete ...
Deployment endpoint responded with status code 202
You can launch the app at http://py37intermrbmissingwebapp.azurewebsites.net
{
  "URL": "http://py37intermrbmissingwebapp.azurewebsites.net",
  "appserviceplan": "xingyz_asp_Linux_centralus_0",
  "location": "centralus",
  "name": "py37intermRBmissingWebApp",
  "os": "Linux",
  "resourcegroup": "eplinux",
  "runtime_version": "python|3.7",
  "runtime_version_detected": "-",
  "sku": "BASIC",
  "src_path": "C:\\Users\\xingyz\\Desktop\\XingyiTest\\python-docs-hello-world"
}
```

- Testing with the same python program to send 2000 requests --> All Successful

```py
url = 'https://py37intermrbmissingwebapp.azurewebsites.net'

headers = {
  'Content-Type': 'application/json'
}

total_requests = 2000
number_of_400 = 0

for number in range(total_requests):
    # request = requests.get(url)
    response = requests.request("POST", url, headers=headers, data=gen())
    status = response.status_code
    if status == 400:
        number_of_400 += 1

    print(f'Response Code: {response.status_code}')
    #print(f"Transfer Encoding: {response.headers['transfer-encoding']}\n")

    # print(f'headers: {request.headers.keys()}')
    # print(f"Transfer Encoding: {request.headers['transfer-encoding']}\n")
    print(f'body: {response.text}')

print(f"Total Requests Count: {total_requests}")
print(f"Failed Requests Count: {number_of_400}")
```
![All Successful executions for Linux Python Web App]()
