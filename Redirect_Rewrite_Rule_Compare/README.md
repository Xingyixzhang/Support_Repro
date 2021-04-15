### Project Purpose: Test out redirect vs rewrite rules in web.config + Startup health check
### References: 
####  - [Use of Redirect in AppInit -- Effect on Swap Operations](https://ruslany.net/2017/11/most-common-deployment-slot-swap-failures-and-how-to-fix-them/)
####  - [Health checks in ASP.NET Core | Microsoft Docs](https://docs.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks?view=aspnetcore-5.0)

### Web.Config File Structure Overview
Web.config file is structured using XML. The file contains tags and each tag can have sub-tags and attributes associated with it. Here is a sample web.config file with basic configuration settings done:

<?xml version=’1.0” encoding=”utf-8”?>
<span style="background-color: #BEFFCF"><configuration></span> <-- Root Element

<configSections> <-- Where you can define custom tags

<section name="SampleCustomTag" <-- custom tag that can define any # of key-value pairs as needed
type="System.Configuration.NameValueFileSectionHandler " />
</configSections>

<system.net>
<!—Include details about network classes, if any ?
</system.net>

<system.web> <-- Define the config settings required for your ASP.Net classes

<compilation defaultLanguage="c#" debug="false"/> <-- specify coding language and whether to enable debugging.
								This info will be used at compilation time, when debug is set to true, the app performance will be low comparably.
								
<customErrors mode="On" defaultRedirect="defaultCusErrPage.htm"/><-- when on, default error page specified in this tag 
										will display when any unhandled error occurs in app.
										Also allows custom error page based on error code by mentioning in this tag using <error> sub tag.
<authentication mode=”Forms”> <-- Determines auth mechanism and specific config details for that auth.
<forms loginUrl = "frmSampleLogin.aspx" timeout="20"/>
</authentication>

<authorization><-- Defines user's app/folder access permissions.
<allow users="User1, User2" />
<deny users=”*” />
</authorization>

<trace enabled="true" requestLimit="20" /><-- Trace log for the entire application can be viewed using trace.axd utility or 
						trace information can be viewed for each page by configuring in this tag.
<sessionState<-- Used to configure sessions. 
		HTTP protocol used for ASP.NET app is stateless, though here you can use sessions to maintain states.
mode="SQLServer"
stateConnectionString=”tcpip =127.0.0.1:8040”
sqlConnectionString="data source=127.0.0.1; Integrated Security=SSPI
Trusted_Connection=yes”;
cookieless="true"
timeout="40" >
</sessionState>

<httpModules><-- Configure any specific httpModules in app. 
		Type specifies both class name and assembly name (comma separated).
<add type="sampleClass,sampleAssembly" name="sampleModule" />
<remove name="modulename"/>
</httpModules>

<httpHandlers><--define any custom HTTP handler here. Type specifies handler type and assembly name (comma sep.)
<add verb="*" path="sampleFolder/*.aspx"
type="sampleHttpHandler,sampleAssembly" />
</httpHandlers>

<httpRuntime appRequestQueueLimit="200" executionTimeout="500" /><-- configure app runtime settings.
appRequestQueueLimit specifies the max# of requests that can be queued in memory waiting for the server to process.
executionTimeout specifies the timeout period in seconds.
</system.web>

<appSettings><-- Define specific data that's needed throughout the app.
<add key="DBConnString"
value="server=127.0.0.1;uid=usr;pwd=pwd; database=DBPerson" />
</appSettings >

<sampleCustomTag ><--Customized tags defined in configSections can be specified as an independent tag.
<add key="sampleKey" value="sample key value" />
The key “sampleKey” mentioned inside this custom tag can be accessed using the following line of code:
ConfigurationSettings.GetConfig("sampleCustomTag")("sampleKey")
</sampleCustomTag >
</configuration>
![image](https://user-images.githubusercontent.com/59896882/114816109-569b9e00-9d6c-11eb-9e3c-82cb43673ad2.png)
