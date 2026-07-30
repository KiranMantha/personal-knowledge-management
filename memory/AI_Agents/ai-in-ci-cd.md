---
type: Learning
title: AI in CI/CD
topic: AI_Agents
tags:
  - ai
  - cicd
status: stable
generated:
  by: agent-kiran/seed-script
  at: '2026-07-30T07:06:33.746Z'
---
Original article: https://www.eficode.com/blog/mastering-devops-with-ai-building-next-level-ci/cd-pipelines

# Mastering DevOps with AI: Building next-level CI/CD pipelines
In an era where [AI-assisted programming](https://www.eficode.com/transforming-software-development-with-ai-and-devops?hsLang=en) is rapidly evolving, the importance of robust DevOps practices can’t be overstated. In this blog post, I will demonstrate the efficient utilization of AI in building and enhancing CI/CD pipelines, highlighting that while AI brings significant advancements, human expertise remains crucial.

Establishing a solid DevOps foundation is no longer a months-long endeavor. With the right approach and tools, even small projects can and should have proper DevOps in place within days or weeks. Now, let's shift our focus to the foundational aspects of CI/CD, starting with the Git workflow.

![image-1](https://www.eficode.com/hs-fs/hubfs/Eficode%202020%20site%20images/Blog%20images/image-1.png?width=4167&height=2084&name=image-1.png)

Git workflow: The basement for good CI/CD
-----------------------------------------

As we all know, clear and well-documented Git workflow practices are crucial for every successful development project, especially in DevOps. Here, I will demonstrate how one can be achieved from scratch with the help of ChatGPT 4. You may test the results by using the very same prompts I have used here (ChatGPT 4 version required).

Prompt #1

The first prompt typically serves as an introduction to the topic. This approach allows you to observe the initial response and understand the direction of the discussion. Single-shot prompts are seldom sufficient. Continue reading to see how I further guide the discussion. My first prompt is as follows:

_Please give me git workflow baseline so that I can later implement continuous integration and deployment pipelines on top of the workflow practices_

GPT response

_Creating a solid Git workflow baseline is essential for implementing continuous integration (CI) and continuous deployment (CD) pipelines effectively. Here's a suggested baseline workflow that you can use as a starting point:..._

#### _Branching Strategy:_

*   _**Main Branch:** This is the primary branch where the source code of HEAD always reflects a production-ready state._

*   _**Develop Branch:** This branch serves as an integration branch for features. It's always in a state with the latest delivered development changes for the next release._

*   _**Feature Branches:** Create these branches when you start work on a new feature. Branch off from 'develop' and merge back into 'develop' once the feature is complete._

*   _**Release Branches:** Branch off from 'develop' when you're ready to prepare a new production release. This allows one team to polish the current release while another team continues working on features for the next release._

_**Hotfix Branches:** These branches are used to quickly patch production releases. They are a lot like release branches and feature branches except they're based on 'main' and merged into both 'main' and 'develop'._

_Continuous Integration (CI):_

*   _Set up a CI pipeline that runs automated tests and other checks (like linting) every time a new commit is pushed to any branch, particularly 'develop' and 'feature' branches._

#### _Continuous Deployment (CD):_

*   _Once the CI pipeline passes and changes are merged into the main branch, automatically deploy to production if your setup allows for it._

*   _For more controlled environments, you might choose to manually trigger deployments from the main branch._

#### _Version Tagging:_

  

*   _After each release, tag the code in the main branch with a version number._

_Documentation:_

*   _Keep your project documentation up-to-date. This includes not only your code documentation but also your **workflow and pipeline processes.**_

In addition, there are sections to commit guidelines, core review, and merging, but we won’t focus on them in this blog post, even though they are important.

### Conclusion to using a Git workflow baseline

Even AI seems to emphasize the importance of Git workflows. It suggests having separate development and release branches, which is a good strategy when implemented correctly. But for the sake of demonstration, I will illustrate a more streamlined workflow that might be more optimal.

Note the important aspect: Document your workflow and pipeline! It seems like AI’s thought process is very well on the map here and better than reality most of the time.

Clear communication about these topics and retrospectives will ensure Developer Experience (DevEx) stays great.

Prompt #2

Now that we have the initial response and ChatGPT has a record of our discussion history for future prompts, I plan to request more specific details. It is advisable to evaluate the response after the first prompt and after each subsequent response, delving deeper into any new topics that arise if necessary.

Only then should you proceed with the next prompt to avoid disrupting the chat session, which can easily lead to undesirable outcomes with large language models (LLMs). 

_Please make the workflow more simple and remove develop and release branches, for those I will use git tagging._

GPT response

_Certainly! Simplifying the Git workflow by removing the develop and release branches and using Git tagging instead can make the process more streamlined, especially for smaller teams or projects. Here’s a revised version of the workflow:_

_Main Branch:_

*   _This is your primary and only long-lived branch. The main branch represents the production-ready state of your code._

*   _All features, bug fixes, and hotfixes are merged directly into this branch._

_Feature Branches:_

*   _Create a feature branch whenever you start work on a new feature or a bug fix._

*   _Branch off from main and, once the work is complete and tested, merge it back into main._

*   _Naming convention for feature branches can be like  `feature/<feature-name>` or `bugfix/<bug-name>`._

_Git Tagging for Releases:_

*   _When you're ready to release a new version, use Git tagging on the main branch._

*   _Name your tags with semantic versioning (e.g., v1.0.0, v1.0.1) to keep track of different releases._

*   _Tags can also be used to trigger specific CI/CD actions if necessary._

_Continuous Deployment (CD):_

*   _If your project setup allows, set up **CD to automatically deploy the main branch to production** after passing CI checks._

*   _For more controlled environments, you might choose to manually deploy tagged versions._

The other parts are very similar to before and need no repetition here.

### Conclusion to simplifying the workflow and removing develop and release branches

Okay, this now looks like what I requested. However, a concern arises when GPT suggests deploying the main branch to production automatically after CI.

We all know, for the sake of our sanity and system reliability, that we definitely need production-like environments, such as staging, for proper quality assurance (QA).

Running automated regression tests in production-like environments after any change is crucial. This includes not only code changes in the product but also those related to infrastructure (IaC), pipelines, and more.

Prompt #3

_For continuous deployment, I want to deploy the main only to production-like environments automatically, let it be staging. And a production deployment should happen by utilizing git tagging with prefix "release-" for example release-v1.0.0. For staging deployment the prefix would be rc- (release-candidate)._

GPT response

_Absolutely, your approach to continuous deployment using specific Git tagging conventions for staging and production environments is a great strategy. Here's how you can structure this workflow:_

_Main Branch as Staging Environment:_

*   _The main branch acts as a staging-like environment. Every merge into main triggers an automatic deployment to the staging environment._
*   _This allows you to test in an environment that closely resembles production._

_Git Tagging for Staging and Production:_

*   _Staging Tags: Use the prefix rc- (release candidate) for staging deployments. For example, rc-v1.0.0 indicates a release candidate for version 1.0.0. When you push a tag with this prefix, it triggers a deployment to the staging environment._
*   _Production Tags: Use the prefix release- for production deployments. Tags like release-v1.0.0 will be used to trigger manual deployments to the production environment. This gives you control over what and when something is deployed to production._

_Workflow Steps:_

*   _Development: Developers work on feature or bugfix branches branched from main._

*   _Code Review and Merging: Once work is completed, a pull request is created to merge changes into main. After code review and successful CI checks, the changes are merged._

*   _Automatic Staging Deployment: Merging into main automatically triggers deployment to the staging environment. This is for final testing and validation._

*   _Tagging for Release Candidates: When the team is satisfied with the changes in staging, a rc- tag is created to formally mark a release candidate._
*   _Production Deployment: Once the release candidate is thoroughly tested and approved, a release- tag is created. This tag is then used to manually trigger the deployment to the production environment._

_Continuous Integration and Deployment:_

*   _Set up CI/CD pipelines to handle different environments based on the tagging convention._
*   _Ensure that the CI pipeline includes all necessary tests and quality checks._

_Documentation:_

*   _Document this process clearly, including how and when to tag for staging and production deployments._

_This setup ensures a clear separation between staging and production deployments and gives your team control over the release process. By using different tags for staging (rc-) and production (release-), you can easily manage and track the progress of different releases through your environments._

### Conclusion to automating deployments to production-like environments

Now I am happy with my workflow. It is possible to work in a similar fashion to achieve the workflow you are happy to proceed with.

If you completely mess up the chat session with AI, it may be better to start a new one from scratch to prevent misleading responses.

This time, I managed to get results in the first chat session, but many times it was not so easy. Next, I will proceed with the actual pipeline generation as code by using Atlassian Bitbucket pipelines as the underlying technology.

Generative AI for DevOps pipelines
----------------------------------

In this section, we will see how Chat GPT-4 can generate a Bitbucket pipeline description file to implement the above.

Prompt #4

Here, I will continue prompting in the same chat session so that there is relevant context in the background for the LLM.

_Now I want you to provide me bitbucket-pipelines.yaml out of the latest workflow you recently responded to. Provide the pipeline for my backend service that is implemented with python flask, and I want to deploy to Google Kubernetes on GCP._

Here, I received a high-level implementation where most of the details were moved to separate shell script files. This was not my intention, so I won’t show the response here. However, after following rounds of discussions, I received what I was looking for.

Prompts from #5 to #8

Multiple prompts are common when engaging with generative AI on complex topics. The AI cannot infer your exact needs from a single, detail-limited prompt. Furthermore, it is essential to divide larger tasks into smaller, manageable segments. This process also necessitates a comprehensive understanding of DevOps to guide the conversation effectively. You shouldn’t expect to get good results easily.

_#5 - Okay this is a bit too high level. I want you to include docker image building and pushing images to Google Cloud Repository gcr.io. In addition include also gcloud cli and kubectl commands. Also placeholders for environment variables and secrets where needed._

_#6 - That is good, but how does it work if release-\* tag is triggered with manual?_

_#7 - I want to take into use bitbucket deployment environments, would you please give me the most recent bitbucket-pipelines.yaml file with the modifications that have this information._

_#8 - I want to change the pipeline so that docker image is built only once, which can be later retagged. There should be no need to build it all over again._

GPT-4 response

_To modify your pipeline so that the Docker image is built only once and then retagged for different environments, you'll need to make a few adjustments to your bitbucket-pipelines.yml. The idea is to build the Docker image once, push it to Google Container Registry (GCR) with a generic tag, and then retag it for staging or production deployments as needed._

_Here’s an updated version of your bitbucket-pipelines.yml file with these changes:_

```yaml
image: atlassian/default-image:2
pipelines:
  default:
    - step:
        name: Build and Test
        caches:
          - pip
        script:
          - pip install -r requirements.txt
          - python -m unittest discover tests
  branches:
    main:
      - step:
          name: Build and Push Docker Image
          script:
            - echo $GCLOUD_SERVICE_KEY | base64 --decode --ignore-garbage > ${HOME}/gcloud-service-key.json
            - docker build -t gcr.io/$GCLOUD_PROJECT/your-app:latest .
            - gcloud auth configure-docker --quiet
            - docker push gcr.io/$GCLOUD_PROJECT/your-app:latest
      - step:
          name: Deploy to Staging
          deployment: staging
          script:
            - echo "Deploying to Staging Environment"
            - ./deploy-staging.sh # This script should handle the retagging for staging
  tags:
    'rc-*':
      - step:
          name: Retag and Deploy to Staging
          deployment: staging
          script:
            - echo "Retagging and Deploying Release Candidate to Staging"
            - ./retag-deploy-staging.sh # Script to retag the image for staging
    'release-*':
      - step:
          name: Retag and Deploy to Production
          deployment: production
          trigger: manual
          script:
            - echo "Retagging and Deploying to Production Environment"
            - ./retag-deploy-production.sh # Script to retag the image for production
definitions:
  caches:
    pip: ~/.cache/pip
```

_Key Changes_

_Single Image Build: The Docker image is built and pushed only once on commits to the main branch. It is tagged as latest._

_Retagging for Staging and Production:_

*   _The ./deploy-staging.sh script is used for deploying the latest tag to the staging environment directly._
*   _For the rc-\* and release-\* tags, separate scripts (./retag-deploy-staging.sh and ./retag-deploy-production.sh) are used. These scripts should handle retagging the Docker image with the appropriate tag (based on the commit or release tag) and then deploying it to the respective environment._

_Scripts for Retagging and Deploying_

*   _./deploy-staging.sh should deploy the latest image to staging without retagging._

*   _./retag-deploy-staging.sh and ./retag-deploy-production.sh should:_
    *   _Pull the latest image from GCR._
    *   _Retag it with the specific commit or release tag._
    *   _Push the retagged image back to GCR._
    *   _Update the Kubernetes deployment to use the new tag._

_This approach ensures that the Docker image is built only once, saving time and resources. The retagging scripts offer flexibility in managing different environments without needing to rebuild the image. Remember to ensure that your GCP service account has the necessary permissions and to replace placeholders with your actual project details._

### Conclusion for final output from LLM

Repeat these steps for each component of your system, be it a service, UI, or application. Drawing on my experience with Bitbucket pipelines, I can evaluate responses with a fair degree of confidence and understand what's needed to make this operational. However, if I were unfamiliar with the technologies, I would anticipate encountering some unexpected challenges.

As LLMs become more advanced and specialized versions are developed, the quality of responses will certainly improve. AI will greatly speed up the process of taking the new technologies and processes into use in the field of DevOps.

Achieving a DevOps baseline in practice with AI
-----------------------------------------------

So there you have it, my demonstration of how a DevOps baseline can be achieved in practice with the help of AI. To get started with prompting, advanced skills are not required, but, as with any sport, better results are achieved with practice.

There are still several things to improve from the baseline, for example, comprehensive Continuous Integration, including DevSecOps and IaC, among others.

With the help of AI, onboarding to DevOps topics becomes easier. There is so much good material available on the internet, and it appears to be well integrated into LLMs. However, it's important to understand that design discussions of this kind are more effective with the most advanced LLMs. The same discussion with GPT-3.5, for example, would be very different.

Often, it is thought that CI/CD represents too significant an investment for smaller projects. However, it easily outweighs the costs that would arise if neglected or implemented at a later stage. There should no longer be any reason to hesitate in investing in DevOps from the start.

As time passes, I anticipate the rise of increasingly comprehensive development platforms where many processes are automated, making development and DevOps more abstract. Nonetheless, problem-solving skills and a deep understanding of the underlying principles will remain important.
