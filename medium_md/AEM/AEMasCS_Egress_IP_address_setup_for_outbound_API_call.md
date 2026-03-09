---
title: "AEMasCS : Egress IP address setup for outbound API call"
url: https://medium.com/p/45ae7e4e0d39
---

# AEMasCS : Egress IP address setup for outbound API call

[Original](https://medium.com/p/45ae7e4e0d39)

Member-only story

# AEMasCS : Egress IP address setup for outbound API call

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--45ae7e4e0d39---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--45ae7e4e0d39---------------------------------------)

2 min read

·

Apr 28, 2025

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

Non members can access from [here](/@angadi.saa/aemascs-egress-ip-address-setup-for-outbound-api-call-45ae7e4e0d39?sk=0546211f77d2aefae7a290f2489b1521)

In one of our requirement , we need to call 3rd party api from AEMasCS.

From the api side they will use only IP address to whitelist not domains.

From AEMasCS we will not get static IP to whitelist. We need to use egress Ip address and share the IP address to 3rd party API.

1. Log in to the [Adobe Experience Manager Cloud Manager](https://experience.adobe.com/cloud-manager/) as a Cloud Manager Business Owner.
2. Navigate to the desired Program.
3. In the left menu, navigate to **Services > Network Infrastructures**.
4. Select the **Add network infrastructure** button.

Press enter or click to view image in full size

![]()

5. In the **Add network infrastructure** dialog, select the **Dedicated egress IP address** option, and select the **Region** to create the dedicated egress IP address.

Press enter or click to view image in full size

![]()

6. Select **Save** to confirm the addition of the dedicated egress IP address.

Press enter or click to view image in full size

![]()

7. Wait for the network infrastructure to be created and marked as **Ready**. This process can take up to 1 hour.

Press enter or click to view image in full size

![]()

>nslookup p{programId}.external.adobeaemcloud.com

![]()

Share this 30.213.41.79 with API provider to whitelist

In the java code where your making call you need to use below code .

This will ensure system configurations related to proxies

```
 int connectTimeout = 5000;  
        int connectionRequestTimeout = 5000;  
        int socketTimeout = 10000;  
  
        RequestConfig config = RequestConfig.custom()  
                .setConnectTimeout(connectTimeout)  
                .setConnectionRequestTimeout(connectionRequestTimeout)  
                .setSocketTimeout(socketTimeout)  
                .build();  
  
        // HttpClients.createSystem() uses system properties (e.g., proxy settings)  
        return HttpClients.custom()  
                .setDefaultRequestConfig(config)  
                .useSystemProperties() // important: applies system proxy/etc.  
                .build();  
/* or below line*/  
HttpClients.createSystem()
```

Reference: <https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/networking/dedicated-egress-ip-address>

Please feel free to leave a comment for any suggestions, improvements, or clarifications