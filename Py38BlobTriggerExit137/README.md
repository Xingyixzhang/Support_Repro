## Issue
Blob trigger function logs the uploaded blob's information to storage queue. 
Function works well with small-sized blobs but experience the following error with ~1 GB size file uploads:
- Microsoft.Azure.WebJobs.Host.FunctionInvocationException : Exception while executing function: Functions.<*Blob_Trigger_Name*> ---> Microsoft.Azure.WebJobs.Script.Workers.WorkerProcessExitException : **python exited with code 137**

## Demo

## Bonus Point

### Python Functions Memory Profiling
**Reference Links**: 

- [Profile Python apps memory usage in Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/python-memory-profiler-reference)

- [memory_profiler Python Package](https://pypi.org/project/memory-profiler/): provides line-by-line memory consumption analysis of your functions as they execute.
