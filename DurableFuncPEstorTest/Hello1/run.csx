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