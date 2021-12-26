# WeatherApp  (Sending Event Data To Azure Event Hub)

### \- Azure Resources:
- **EventHub Namespace**: [xingyiEH](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/testwindow-rg/providers/Microsoft.EventHub/namespaces/xingyiEH/overview)
- **Eventhub Entity**: [eh001tdptriggertest](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/testwindow-rg/providers/Microsoft.EventHub/namespaces/xingyiEH/eventhubs/eh001tdptriggertest/processdata)
- **Function App**: [XingyiFakeFuncApp](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/testwindow-rg/providers/Microsoft.Web/sites/XingyiFakeFuncApp/appServices) | WUS | Windows .Net | F1 ASP

### \- Eventhub Trigger function.json & run.csx
```json
{
  "bindings": [
    {
      "type": "eventHubTrigger",
      "name": "events",
      "direction": "in",
      "eventHubName": "samples-workitems-eh",
      "cardinality": "many",
      "connection": "xingyiEH_RootManageSharedAccessKey_EVENTHUB",
      "consumerGroup": "$Default"
    }
  ]
}
```
```cs
#r "Microsoft.Azure.EventHubs"


using System;
using System.Text;
using Microsoft.Azure.EventHubs;

public static async Task Run(EventData[] events, ILogger log)
{
    var exceptions = new List<Exception>();

    foreach (EventData eventData in events)
    {
        try
        {
            string messageBody = Encoding.UTF8.GetString(eventData.Body.Array, eventData.Body.Offset, eventData.Body.Count);

            // Replace these two lines with your processing logic.
            log.LogInformation($"C# Event Hub trigger function processed a message: {messageBody}");

            // eventData.Properties.Add("EventType", "com.microsoft.samples.hello-event");
            // eventData.Properties.Add("priority", 1);
            // eventData.Properties.Add("score", 9.0);

            // foreach(KeyValuePair<string, object> props in eventData.Properties)
            // {
            //     log.LogInformation($"Properties Key = {props.Key }");
            //     log.LogInformation($"Properties Value = {props.Value}");
            // }

            await Task.Yield();
        }
        catch (Exception e)
        {
            // We need to keep processing the rest of the batch - capture this exception and continue.
            // Also, consider capturing details of the message that failed processing so it can be processed again later.
            exceptions.Add(e);
        }
    }

    // Once processing of the batch is complete, if any messages in the batch failed processing throw an exception so that there is a record of the failure.

    if (exceptions.Count > 1)
        throw new AggregateException(exceptions);

    if (exceptions.Count == 1)
        throw exceptions.Single();
}

```

### \- Demo Instructions:
- Create EH namespace and EH entity, function app and eventhub trigger;
- Configure the EH connection (with the access key and entity name)
- Send data to Eventhub using the sample project code in this repo \[Be sure to change the event hub connection string to your own in the **Program.cs** file\]
- Run the project locally and monitor the Eventhub entity & Function executions.
