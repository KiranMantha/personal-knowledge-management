---
title: "Get User Postal Code, Latitude, Longitude etc from AWS"
url: https://medium.com/p/ddb09743eb16
---

# Get User Postal Code, Latitude, Longitude etc from AWS

[Original](https://medium.com/p/ddb09743eb16)

Member-only story

# Get User Postal Code, Latitude, Longitude etc from AWS (cloudfront-viewer-postal-code, cloudfront-viewer-latitude, cloudfront-viewer-longitude etc)

[![Bishon Bopanna](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*-hxMvsHXWXc-D16b)](/?source=post_page---byline--ddb09743eb16---------------------------------------)

[Bishon Bopanna](/?source=post_page---byline--ddb09743eb16---------------------------------------)

6 min read

·

Feb 22, 2021

--

Listen

Share

More

Requirement — Get user postal code/zip (and/or Latitude, Longitude) to localize user content.

Option 1 — Go the Google geocoding route : [https://bishonbopanna.medium.com/google-maps-api-for-postal-code-lookup-5a58495e0ef3](/google-maps-api-for-postal-code-lookup-5a58495e0ef3)

Option 2 : Use the AWS’s lambda edge to get geo location headers (Faster!).

AWS does such an AMAZING job (sarcastic) at putting out documents that span multiple services to resolve a simple use case like — get a user’s postal code!

After reading : [Amazon CloudFront adds additional geolocation headers for more granular geotargeting](https://aws.amazon.com/about-aws/whats-new/2020/07/cloudfront-geolocation-headers/) was super excited just to be later buried in countless readings and explorations to get to figuring out the setup for this simple use case was a pain. And after more readings and many trial and errors below in the solution, but go over these links as they have good content:

[1] [Using the CloudFront HTTP headers](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-cloudfront-headers.html)

[2] [Amazon CloudFront Announces Cache and Origin Request Policies](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-cloudfront-announces-cache-and-origin-request-policies/)

Solution [In this article we will look into only cloudfront-viewer-postal-code header, but below config will be same for all cloudfront-viewer-\* headers] :

Step 1 : Add a S3 bucket with static hosting enabled and an empty json file with below specifics :

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Upload an empty json file (this can be any file, we just need a resource in the S3 bucket to request for)

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Step 2 :

Configure CloudFront for this custom endpoint, so that we can add the headers from origin request policy

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Step 3 : Create Lambda edge function with CloudFront distribution association to collect the header cloudfront-viewer-postal-code and put it on the body of the response.

Before that, quick understanding of the 4 different cloud front events. These events or triggers can happen at 4 cases as below

Press enter or click to view image in full size

![]()

**Viewer Request :**The function executes when CloudFront receives a request from a viewer, before it checks to see whether the requested object is in the CloudFront cache.

**Origin Request :** The function executes *only* when CloudFront forwards a request to your origin. When the requested object is in the CloudFront cache, the function doesn’t execute.

**Origin Response :** The function executes after CloudFront receives a response from the origin and before it caches the object in the response. Note that the function executes even if an error is returned from the origin.

**Viewer Response :** The function executes before returning the requested file to the viewer. Note that the function executes regardless of whether the file is already in the CloudFront cache.

We need to create a Lambda function and link it to the above created CloudFront distribution which makes this Lambda a Lambda Edge and for the event “Origin Request”, meaning to say when our empty json file in the S3 bucket is accesses through the CloudFront distribution link like : <http://d3p4rywdzrdqip.cloudfront.net/cloudfront-viewer_postalcode.json> , the lambda edge function is triggered which will contain the cloudfront-viewer-\* headers for us to use.

For this step you will \_have\_ to be in N.Virginia only which us-east-1, yes you read this right, this is one of the gotchas. Lambda functions should be created in us-east-1 region to be attached to CloudFront Distributions. And the second gotcha is no environment variables.. there are a few more.

You can add triggers only for a numbered version, not for $LATEST or for aliases.

To add triggers, the IAM execution role associated with your Lambda function must be assumable by the service principals lambda.amazonaws.com and edgelambda.amazonaws.com. For more information, Setting IAM Permissions and Roles for Lambda@Edge.

Read more [here](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-requirements-limits.html)

So switch to N.Virginia (us-east-1) if you are not already in that region.

Create a lambda function from the blueprint : cloudfront-http-redirect

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

```
'use strict';  
  
exports.handler = (event, context, callback)  => {  
      
    console.log("medium-aws-edge-headers-function triggered");  
      
    var request = event.Records[0].cf.request;  
    const requestHeaders = request.headers;  
    const requestHeadersCloudfrontViewerPostalCodeValue = requestHeaders['cloudfront-viewer-postal-code'][0].value;  
      
    console.log("Request Headers cloudfront-viewer-postal-code value : ", requestHeadersCloudfrontViewerPostalCodeValue);  
    
  
    const response = {  
        status: '200',  
        statusDescription: 'OK',  
        headers: {  
            'cache-control': [{  
                key: 'Cache-Control',  
                value: 'max-age=100'  
            }],  
            'content-type': [{  
                key: 'Content-Type',  
                value: 'text/html'  
            }],  
            'access-control-allow-origin': [{  
                key: 'Access-Control-Allow-Origin',  
                value: '*'  
            }]  
        },  
        body: `{  
                  "cloudfront-viewer-postalcode" : ${requestHeadersCloudfrontViewerPostalCodeValue}  
      
                }`,  
    };  
      
    callback(null, response);  
};
```

Above code is not complex, it is just reading the cloudfront-viewer-postal-code from the header and adding the body of the response. So the content of the json file was immaterial and hence we used and empty one — extend this idea to look up for any resource and play with the geo coding headers.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Now the magic :)

Press enter or click to view image in full size

![]()

We are done! Now how you consume this data of users postal code is upto you. Extend the same logic for any cloudfront-viewer-\* headers for the below list :

*CloudFront-Viewer-City — Contains the name of the viewer’s city.*

*CloudFront-Viewer-Country — Contains the two-letter country code for the viewer’s country. For a list of country codes, see ISO 3166–1 alpha-2.*

*CloudFront-Viewer-Country-Name — Contains the name of the viewer’s country.*

*CloudFront-Viewer-Country-Region — Contains a code (up to three characters) that represent the viewer’s region. The region is the most specific subdivision of the ISO 3166–2 code.*

*CloudFront-Viewer-Country-Region-Name — Contains the name of the viewer’s region. The region is the most specific subdivision of the ISO 3166–2 code.*

*CloudFront-Viewer-Latitude — Contains the viewer’s approximate latitude.*

*CloudFront-Viewer-Longitude — Contains the viewer’s approximate longitude.*

*CloudFront-Viewer-Metro-Code — Contains the viewer’s metro code. This is present only when the viewer is in the United States.*

*CloudFront-Viewer-Postal-Code — Contains the viewer’s postal code.*

*CloudFront-Viewer-Time-Zone Contains the viewer’s time zone, in IANA time zone database format (for example, America/Los\_Angeles).*

Few trouble shooting tips :

1. Check CloudWatch log for the lambda to see if you get any logs or exceptions
2. Sometimes cloudfront caches the response which you will need to invalidate
3. Go to Behaviour of your cloudfront distribution and check if the Lambda function associations have the right version of the Lambda function — Note the number after : below

Press enter or click to view image in full size

![]()

PS — While testing the cloudfront-viewer-\* headers found that the values do not values reflect correct values, in this case postal code for many countries, while it does correctly for USA.