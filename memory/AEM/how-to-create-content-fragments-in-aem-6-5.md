---
type: Learning
title: How to create Content Fragments in aem 6.5
topic: AEM
tags:
  - aem
  - content-fragments
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:31.995Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:31.995Z'
---
Youtube Resource: 
- create content fragment: https://www.youtube.com/watch?v=7SFYjGjSveQ&t=9s&ab_channel=TechTalkwithRitesh
- create content fragment: https://www.youtube.com/watch?v=l9AIjvL_n8A&t=867s
- expose fragment via rest api: https://www.youtube.com/watch?v=92s3GwRISZQ&ab_channel=SankhamMarTechChannel

AEM Graphql package: 
- https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-with-aem-headless/how-to/install-graphiql-aem-6-5

**Note** - If you are looking for content fragment creation in 6.5 classic, pls check: https://www.youtube.com/watch?v=sftCl5y4GN4&ab_channel=AdobeExperienceManagerUserGroups

# How to create Content Fragments in aem 6.5 Cloud:

Content fragment structure is defined by Content fragment model. In normal FE dev terms, content fragment model is similar to typescript interface. 1st we define the interface and create the actual structure by leveraging the interface.

So first we should create the model and then actual content fragment. For that:

1. Create an aem app using mvn command. Login to aem dashboard. This should load the start page. An aem app should have permission to create the content fragment 
2. so to provide this permission, navigate to tools => general => configuration manager => <your-aem-app> => select => properties => check content fragment models and graphic => save.  
3. Post this we should create the content fragment model. For that, navigate to tools => general => content fragment models
4. Select <your-aem-app> and click create
5. Enter model title and save
6. Once successfully saved, click on open button. 
7. Select JSON Object type and enter the title of that json object and save the model. This model will define the structure of the upcoming content fragment
8. Once done, go to /aem/start.html
9. Select Assets => Files => <your-aem-app>
10. Click on create button and choose Content Fragment from the options
12. Select previously generated content fragment model and click on next
13. Enter title and description for this new content fragment and click on save.
14. Once successfully saved, click on open button. 
15. Here we should see the structure of JSON object that we defined in content model. Populate your data as json and click on save. This will create the new content fragment. 
16. Once saved, click on preview button on left side navbar to view the saved content fragment data. copy the `_path` attribute which we need to query via graphql.
  <img width="901" alt="image" src="https://gist.github.com/user-attachments/assets/ee10431a-ff68-46bd-b23c-a22684648cdf" />
16. Once saved, click on preview button on left side navbar to view the saved content fragment data. copy the `_path` attribute which we need to query via graphql.
17. When we call that content fragment using fetch call, the data that we populate for that content fragment will display under the structure  we defined in content model.
  
## How to consume content fragment:

Inorder to consume content fragment, we need to: 
- create a configuation for our app and then 
- create the graphql endpoint using that configuration.
- create persisted queries in graphiql editor to expose them as actual rest endpoints

### To create the configuration:
1. navigate to /aem/start.html.
2. click on tools => General => Configuration Browser
3. Select the app, and click create. 
4. Enter title and name of that configuration and also select Graphql persisted queries & content fragment models from the options.
5. Click on create to create the configuration

### Now, to create the endpoint:
1. navigate to /aem/start.html.
2. click on tools => General => Graphql
3. click on create
4. This should display a modal dialogue to enter the endpoint name. Choose the configuration that we created from above steps.
5. Save and publish the endpoint.

### To create the persisted queries (a.k.a saved queries):
1. navigate to /aem/graphiql.html and choose the endpoint that we created 
2. write a graphql query to call the content fragment by path (this is where the copied `_path` comes handy) as below:
  ```graphql
  // example path looks like this: /content/dam/aem-cloud-app/landing-page
  {
    <your-content-model-name>ByPath(_path: "<your-copied-path-of-content-fragment>") {
      item {
        <your-json-object-name-provided-in-content-fragment-model>
      }
    }
  }
  ```
3. executing above query should return the data that we saved in provided content fragment
4. copy the url of saved query and test it using postman as shown below:
![image](https://gist.github.com/user-attachments/assets/5f8ea54a-eae9-44ea-9767-bb7f28a75daf)

So either pass basic authentication or whitelist the api `/graphql/execute.json/*` in aem dispatcher
