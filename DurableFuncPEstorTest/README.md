**Storage Account**: [storageaccounttdpps93ab](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/tdppsfuncapp/providers/Microsoft.Storage/storageAccounts/storageaccounttdpps93ab/overview) \
**Function App**: [winnetdediDurableTableStorTest](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourcegroups/tdppsfuncapp/providers/Microsoft.Web/sites/winnetdediDurableTableStorTest/functionsList) \
**Basic Concept**: Durable Functions use queues, tables, and blobs to persist orchestration and entity state, they also use blobs and blob leases to manage partitions across a distributed set of nodes.
- **Starter Function**: [DurableFunctionsHttpStart1](https://ms.portal.azure.com/#blade/WebsitesExtension/FunctionMenuBlade/code/resourceId/%2Fsubscriptions%2F83e0d97e-09ce-4ef1-b908-b07072b805e3%2FresourceGroups%2Ftdppsfuncapp%2Fproviders%2FMicrosoft.Web%2Fsites%2FwinnetdediDurableTableStorTest%2Ffunctions%2FDurableFunctionsHttpStart1)
```cs
#r "Microsoft.Azure.WebJobs.Extensions.DurableTask"
#r "Newtonsoft.Json"

using System.Net;
using Microsoft.Azure.WebJobs.Extensions.DurableTask;

public static async Task<HttpResponseMessage> Run(
    HttpRequestMessage req,
    IDurableOrchestrationClient starter,
    string functionName,
    ILogger log)
{
    // Function input comes from the request content.
    dynamic eventData = await req.Content.ReadAsAsync<object>();

    // Pass the function name as part of the route 
    string instanceId = await starter.StartNewAsync(functionName, eventData);

    log.LogInformation($"Started orchestration with ID = '{instanceId}'.");

    return starter.CreateCheckStatusResponse(req, instanceId);
}
```
- **Orchestrator Function**: [DurableFunctionsOrchestrator1](https://ms.portal.azure.com/#blade/WebsitesExtension/FunctionMenuBlade/code/resourceId/%2Fsubscriptions%2F83e0d97e-09ce-4ef1-b908-b07072b805e3%2FresourceGroups%2Ftdppsfuncapp%2Fproviders%2FMicrosoft.Web%2Fsites%2FwinnetdediDurableTableStorTest%2Ffunctions%2FDurableFunctionsOrchestrator1)
```cs
/*
 * This function is not intended to be invoked directly. Instead it will be
 * triggered by an HTTP starter function.
 * 
 * Before running this sample, please:
 * - create a Durable activity function (default name is "Hello")
 * - create a Durable HTTP starter function
 */
#r "Microsoft.Azure.WebJobs.Extensions.DurableTask"

using Microsoft.Azure.WebJobs.Extensions.DurableTask;

public static async Task<List<string>> Run(IDurableOrchestrationContext context)
{
    var outputs = new List<string>();

    // Replace "Hello" with the name of your Durable Activity Function.
    outputs.Add(await context.CallActivityAsync<string>("Hello1", "Tokyo"));
    outputs.Add(await context.CallActivityAsync<string>("Hello1", "Seattle"));
    outputs.Add(await context.CallActivityAsync<string>("Hello1", "London"));

    // returns ["Hello Tokyo!", "Hello Seattle!", "Hello London!"]
    return outputs;
}
```
- **Activity Function**: [Hello1](https://ms.portal.azure.com/#blade/WebsitesExtension/FunctionMenuBlade/code/resourceId/%2Fsubscriptions%2F83e0d97e-09ce-4ef1-b908-b07072b805e3%2FresourceGroups%2Ftdppsfuncapp%2Fproviders%2FMicrosoft.Web%2Fsites%2FwinnetdediDurableTableStorTest%2Ffunctions%2FHello1)
```cs
/*
 * This function is not intended to be invoked directly. Instead it will be
 * triggered by an orchestrator function.
 * 
 * Before running this sample, please:
 * - create a Durable orchestration function
 * - create a Durable HTTP starter function
 */

#r "Microsoft.Azure.WebJobs.Extensions.DurableTask"

using System.Net;
using Microsoft.Azure.WebJobs.Extensions.DurableTask;

public static string Run(string name, ILogger log)
{
    log.LogInformation($"Hello {name}!");
    return $"Hello {name}!";
}
```
### Customer Error
**Error** ForbiddenDurableTask.AzureStorage.Storage.DurableTaskStorageException : Forbidden --> ... ... async Microsoft.WindowsAzure.Storage.**Table.CloudTable.CreateIfNotExistsAsync**(??)at ... ...

---
### My Repro
- Storage Account PEs enabled on both Files and Blobs, not on Tables in the initial setup:
![Storage Account PEs](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/StoragePEendpoints.png)
- Allowed Selected Network, integrated function app with the same Vnet:
![StorageFWsetup](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/StorageNetworkFW.png)
- Storage Endpoints contents Before table PE enabled: (default tables exist though not visible till whitelist client IP in FW)
![BeforeTablePEenabledBeforeClientIPWhitelist](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/BeforeTablePEenabledBeforeClientIPWhitelist.png)
- Durable Functions run as expected once starter is called:
![Starter Succeeded](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/StarterRunLog.png)
![Orchestrator Succeeded](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/OrchestratorRunLog.png)
![Activity Succeeded](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/ActivityRunLog.png)
- Once enabled PE on Tables and allowed client IP, I can see the 2 default tables created (no access policy in place by default):
![Default Tables Created](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/DefaultTablesCreated.png)

---
### Next Step
Since I am not able to repro customer error, suggesting to isolate the issue (either storage account side or Function App end) by running the same app against a new storage account / task hub without restrictions to see if the issue persists.
