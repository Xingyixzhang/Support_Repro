const appInsights = require("applicationinsights");
appInsights.setup(process.env.SECONDARY_APP_INSIGHTS)
                .setAutoDependencyCorrelation(true)
                .setAutoCollectRequests(true)
                .setAutoCollectPerformance(true)
                .setUseDiskRetryCaching(true)
 
appInsights.defaultClient.context.tags[appInsights.defaultClient.context.keys.cloudRole] = "TEST";
appInsights.defaultClient.context.tags[appInsights.defaultClient.context.keys.applicationVersion] = "1.0";
appInsights.start();
 
module.exports = async function (context, req) {
    const client = appInsights.defaultClient;
    client.trackTrace({message:'AppInsights test message ' + req.params.message});
    context.res = {
        body: "OK"
    };
}