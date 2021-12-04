There are two default tables created under the Function App Storage Account: **History** & **Instances**

### To view the contents in the History table
- Generate a SAS token and URL for access:
![ToViewHistoryTable](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/ViewHistoryTable.png)
**My sample History Table Contents (in .xml file) uploaded in project**

### To view the contents in the Instances table
![ViewInstancesTable](https://github.com/Xingyixzhang/Support_Repro/blob/main/DurableFuncPEstorTest/images/ViewInstancesTable.png)
**This table contains the following properties and their values:**
- Partition Key (cannot be deleted nor moved)
- Row Key
- Timestamp
- Completed Time
- Created Time
- Custom Status
- Execution ID
- Input
- Last Updated Time
- Name
- Output
- Runtime Status
- Taskhub Name
- Version
