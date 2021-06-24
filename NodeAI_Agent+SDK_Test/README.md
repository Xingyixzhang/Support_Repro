Deployed the test code with both AI resources all in the same resource group & region. 

Node Version: v14.16.1 \
Linux Function App: [node12AIsdkfuncApp](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/EPlinux/providers/Microsoft.Web/sites/node12AIsdkfuncApp/functionsList) \
Agent-Based Application Insights Resource: [node12AIsdkfuncApp](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/EPlinux/providers/microsoft.insights/components/node12AIsdkfuncApp/overview) \
SDK-Based Application Insights Resource: [node12AIsdkfuncApp-sec](https://ms.portal.azure.com/#@microsoft.onmicrosoft.com/resource/subscriptions/83e0d97e-09ce-4ef1-b908-b07072b805e3/resourceGroups/EPlinux/providers/microsoft.insights/components/node12AIsdkfuncApp-sec/overview)


	traces 
	| where timestamp > ago(1h) 
	| order by timestamp desc

---
1st attempt with Both AI resources enabled <b>\[Agent based AI generated logs but SDK based AI did not.]</b>
#### Primary AI:
![Primary AI First Test](https://github.com/Xingyixzhang/Support_Repro/blob/main/NodeAI_Agent%2BSDK_Test/images/Primary_AI_1.gif)
#### Secondary AI:
![Secondary AI First Test](https://github.com/Xingyixzhang/Support_Repro/blob/main/NodeAI_Agent%2BSDK_Test/images/Secondary_AI_1.gif)

---
2nd attempt with disabled the agent-based AI by adding ‘_DELETE’ to their app setting names, second AI resource remains untouched <b>\[no logs from the primary but I do see logs generated in the secondary AI]</b>
#### Primary AI: (logs stopped at 2:49)
![Primary AI Second Test](https://github.com/Xingyixzhang/Support_Repro/blob/main/NodeAI_Agent%2BSDK_Test/images/Primary_AI_2.gif)
#### Secondary AI:
![Secondary AI Second Test](https://github.com/Xingyixzhang/Support_Repro/blob/main/NodeAI_Agent%2BSDK_Test/images/Secondary_AI_2.gif)

---
3rd attempt with both AI resources enabled <b>\[They both successfully log the correct information] </b>
#### Primary AI:
![Primary AI Third Test](https://github.com/Xingyixzhang/Support_Repro/blob/main/NodeAI_Agent%2BSDK_Test/images/Primary_AI_3.gif)
#### Secondary AI:
![Secondary AI Third Test](https://github.com/Xingyixzhang/Support_Repro/blob/main/NodeAI_Agent%2BSDK_Test/images/Secondary_AI_3.gif)

Fix for the customer:
- Connecting to the secondary Application Insights Resource by connection string instead of instrument key.
- Not so sure of why, since I am able to have successful workflow using Instrument Key in my repro.
