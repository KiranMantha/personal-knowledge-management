---
title: "How to Learn DevOps & Cloud from Scratch in 2026 (A Practical, Job-Ready Roadmap)"
url: https://medium.com/p/0ce8d2f62293
---

# How to Learn DevOps & Cloud from Scratch in 2026 (A Practical, Job-Ready Roadmap)

[Original](https://medium.com/p/0ce8d2f62293)

Member-only story

# How to Learn DevOps & Cloud from Scratch in 2026 (A Practical, Job-Ready Roadmap)

[![Aman Pathak | DevOps | AWS | K8s | Terraform | ML](https://miro.medium.com/v2/resize:fill:64:64/1*QTUQTXb3JRN2Z33yuvB-Gw.jpeg)](https://amanpathakdevops.medium.com/?source=post_page---byline--0ce8d2f62293---------------------------------------)

[Aman Pathak | DevOps | AWS | K8s | Terraform | ML](https://amanpathakdevops.medium.com/?source=post_page---byline--0ce8d2f62293---------------------------------------)

11 min read

·

Dec 22, 2025

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

Not a Medium member? [*Click here to read this story for free.*](/how-to-learn-devops-cloud-from-scratch-in-2026-a-practical-job-ready-roadmap-0ce8d2f62293?sk=6a7ed7fbeca894b5a239e6ccef7ab8cf)

I have covered the same thing in my YouTube video. If you want, you can watch it here:

I’ve seen many people stuck learning random tools without direction, and I’ve been there myself. This roadmap is based on real projects, real interviews, and real mistakes I’ve made while growing in DevOps and Cloud over the last few years.

Hi Everyone, I hope you are doing well and that you are finishing up 2025 with many good memories. If not, I hope you will follow through on the resolutions you made for the coming year, which is 2026.  
I am also preparing my resolutions for the coming year.

Today, I am not going to discuss any advanced or hands-on topics. I would like to discuss what it would be like if I had to start my career in DevOps & Cloud in 2026.

## Why am I doing this?

We have seen in DevOps & Cloud that there are multiple tools and multiple alternatives for every tool.  
But for a beginner, it’s very hard to understand where to start and when.

So, I would like to share my plan to become a DevOps & Cloud Engineer in a more practical way to become Job-Ready for the 2026 Market because in the end, we are all doing hard work for one good job and many more things to unveil beyond doing a single Job.

So, let’s jump into my Practical Guide to help you become a Job-Ready DevOps & Cloud Engineer.

## Split the Plan

We will divide this plan into 4 Phases, and in each phase, we will learn tools and try to understand the DevOps ecosystem and its culture.

## Phase-1

* **Linux & Networking Fundamentals**
* **Learn any Cloud with Projects**

If you skip Linux and networking fundamentals, cloud services will feel like magic, and magic breaks easily. Spend real time here. It pays dividends later.

*Now, let’s understand one by one.*

## Linux and Networking Fundamentals

To become a good DevOps Engineer, you have to know the basics of Linux and Networking fundamentals.  
The important topics you can cover which following are:

* Basic Linux commands
* Shell Scripting
* IP classes
* CIDR Range and CIDR Blocks

This is not enough, but if you try to climb to these topics, you will learn all the other things that would require you to do work as a DevOps Engineer.

## Cloud

Then, we have to pick any cloud and start learning it. I would recommend AWS. But you can choose any of the Clouds from below.

* AWS
* GCP
* Azure

After choosing any Cloud, you can start learning basic and mandatory services of that cloud, like EC2, VPC, EKS, ECS, RDS, S3, Lambda function, etc.  
I have talked about the necessary AWS services that you must know in a separate article. Feel free to check it out. It will definitely help you, and the reason behind it,

[## Top 10 AWS Services to Kickstart Your Cloud Career

### Discover the top 10 AWS services every beginner must know. Learn how EC2, S3, RDS, EKS & more power the cloud with…

aws.plainenglish.io](/top-10-aws-services-to-kickstart-your-cloud-career-0de3ff3f3a37?source=post_page-----0ce8d2f62293---------------------------------------)

After learning about the cloud services, you have to do a lot of hands-on work by doing Big Projects, like Two-Tier, Three-Tier Architecture creation using Cloud services. If you want, you can also deploy the applications on those machines to gain more understanding. But this is a must before jumping into any tools.

## Phase-2

* **Terraform**
* **Continuous Integration and Continuous Delivery/Deployment (CI/CD)**
* **Docker**

## Terraform

In this phase, we will increase our speed to learn multiple tools.  
As in the previous phase, we learnt how to create AWS services manually and use them. Now, we have to learn how to create or configure AWS services via Infrastructure as Code(IaC).  
In today’s AI world, you must know how to work with tools to configure Infrastructure. For IaC, you need to start learning about Terraform.  
Now, let’s understand the topics that we need to cover.

* Terraform resource and data block to create resources and gather the resources
* Terraform meta arguments
* Terraform State Management, locking & collaboration mindset
* Terraform Modular Approach
* Terraform workspace
* Terraform Best Practices

These topics will help you to master Terraform if you spend enough time and do multiple projects.

### Few resources for Terraform

[## 10 Terraform Commands Every DevOps Engineer Wishes They Knew Earlier

### Discover 10 powerful Terraform commands beyond init and plan that every DevOps engineer must know to debug, import, and…

blog.stackademic.com](https://blog.stackademic.com/10-terraform-commands-every-devops-engineer-wishes-they-knew-earlier-3825f0761fbb?source=post_page-----0ce8d2f62293---------------------------------------)

[## 10 Terraform Best Practices Every DevOps Engineer Must Follow

### By AmanPathak — DevOps & Cloud Specialist | Understand Terraform Best Practices

blog.stackademic.com](https://blog.stackademic.com/10-terraform-best-practices-every-devops-engineer-must-follow-7f96d5532538?source=post_page-----0ce8d2f62293---------------------------------------)

[## How to Use Terraform Meta Arguments Like a Pro: Practical Examples & Interview Tips

### By Aman Pathak — DevOps & Cloud Specialist | Understand Meta Arguments With Practical Examples

blog.stackademic.com](https://blog.stackademic.com/how-to-use-terraform-meta-arguments-like-a-pro-practical-examples-interview-tips-d6ba9c27073d?source=post_page-----0ce8d2f62293---------------------------------------)

### Project Recommendation

* Create multiple AWS services using Terraform in two environments (Dev and QA).
* If you have to create 5 Virtual Machines or any Cloud services, dont write the same code 5 times. Use meta arguments and a modular approach
* Use a remote location to store your Terraform state files.

## Continuous Integration and Continuous Delivery/Deployment (CI/CD)

CICD is very important for a DevOps Engineer. So, there are multiple options available for CICD like GitHub Actions, Jenkins, and GitLab. But I would recommend Jenkins. It might not be trending, but still, 50–60% organisations are using Jenkins, and from the learning perspective, you will learn how to manage a CICD tool to build, test and deploy the applications. Once you learn Jenkins, it will be easy to jump on any other CICD tool like GHA.  
**CI/CD isn’t just about faster deployments; it’s about failing fast, rolling back safely, and avoiding human mistakes.**  
Topics that you should cover for any CICD tools:

* Basic Pipelines or freestyle projects
* Self-hosted runners(If you are learning GitHub Actions or GitLab)
* Secrets Management
* Parallel Jobs
* Caching to reduce the Job time

### Project Recommendation

* Create the entire Infrastructure on AWS(Any Cloud) using Terraform. Then, Automate via Jenkins/GitHub Actions
* After creating the Infrastructure, deploy an application via CICD tool.

## Docker

A lot of people have heard about Kubernetes, and they might have an aspiration to learn Kubernetes. So this is your time.  
To learn Kubernetes, you must know about Docker and should know how to work with containers.  
You have to cover the following topics in Docker:

* Docker Containers, Images
* How to write Dockerfiles?
* Docker volumes
* Docker network
* How to write multi-staging Dockerfiles to reduce the size of Docker images?
* Docker security by running containers as a non-root user
* Docker-Compose to deploy multiple Docker containers

### Project Recommendation

### Project-1

* Deploy a Three-Tier Application using Docker

### Project-2

Once you have completed the above Project, you have to deploy the same application on the cloud. But you have to use a managed service like ECS on AWS, ACA on Azure. So, the workflow for this project would be:

* Create ECS and other required AWS services via Terraform and automate via CICD tools
* Use Dockerfile to create Docker Images and use any container registry like Dockerhub, ECR(create this via Terraform) to store your Docker Images
* Create CICD Pipelines to test, build and deploy your three-tier application.
* Use SonarQube for Code Quality Analysis, Trivy File scan for vulnerable files, scan the Docker images via tools like trivy, Docker Scout, ECR scan, etc.

## **Phase-3**

## **Kubernetes**

Now, we are jumping into the most trending tool in DevOps, which is Kubernetes. So, we will give enough time to learn about Kubernetes, as it includes multiple topics and multiple tools to upskill yourself as a Kubernetes Engineer. Kubernetes is powerful, but overwhelming. Don’t try to memorise YAML, focus on understanding how traffic flows, how pods restart, and how failures are handled.   
Now, let’s understand what topics we have to cover in Kubernetes:

* Kubernetes Architecture & Components, including Scheduler, Kube-proxy, core-DNS, etc.
* Configure Kubernets cluster the hard way. Instead of using any Cloud Managed Kubernetes Cluster like EKS from AWS.
* Kubernetes Resources: Pods, ReplicaSets, Deployments, Services, StatefulSets, Headless Service, DaemonSet.
* Kubernetes Ingress
* Kubernetes Certificates
* Kubernetes Networking Concepts
* Kubernetes Volumes, including PVs and PVCs
* Kubernetes ConfigMaps & Secrets
* Kubernetes Jobs, SideCar Containers, and InitContainers.
* Kubernetes ResourceQuota, Probes.
* Kubernetes Node Scaling
* Kubernetes Application Scaling
* Kubernetes Network Policies
* Kubernetes Deployment Strategy
* Explore Cloud Managed Kubernetes like EKS, AKS, GKE, etc.

After writing multiple concepts of Kubernetes, we skip other concepts. But to start with Kubernetes and have knowledge like an intermediate level of experience in DevOps, you should learn and do hands-On for all these topics.

If you want, you can follow one of my challenges that I did 2 years back, and it’s still relevant as a current Kubernetes learning resource. Feel free to check it out.

[## GitHub - AmanPathak-DevOps/30DaysOfKubernetes: Embark on a 30-day journey to master Kubernetes…

### Embark on a 30-day journey to master Kubernetes. Explore its architecture, set up clusters, deploy apps, and delve into…

github.com](https://github.com/AmanPathak-DevOps/30DaysOfKubernetes?source=post_page-----0ce8d2f62293---------------------------------------)

### **Project Recommendations:**

1. Configure a Kubernetes Cluster with 1 Master and at least 2 worker Nodes

2. Use Minikube or KinD to configure a Kubernetes cluster with any number of worker nodes and 1 Master Node.

3. Deploy a three-tier application on an unmanaged Kubernetes Cluster and access outside of the cluster via Ingress

4. Configure High available Kubernetes cluster by increasing the number of Master Nodes from 1 to at least 3 and use HA-Proxy for load balancing. You can create any number of worker nodes.

## **End-to-End DevSecOps Project**

It’s time to integrate everything that you have learnt so far. You have to do at least 4–5 End-to-End Projects. Now, let's understand the benefit of these projects:

* It helps you to understand how to work with multiple tools
* It helps you to understand howan application is deployed from scratch, like creating infra, etc in the industry.
* It helps you to understand the culture and ecosystem of DevOps.
* Sometimes, we forget previous tool concepts when we move to the next tool. The reason behind this is that you are doing less hands-on. Because if you do enough hands-on, you might forget the YAML or scripts syntax, but you never forget the concept and workflow. So, if you do End-to-End Projects, it will remind you of things again, and ultimately, things will stay in your subconscious mind(Not a Philosopher).
* **[NOTE]:** But don’t just finish projects, write about what broke, what you fixed, and what you’d do differently next time.

### **Project Recommendations**

I will share the resources and do those projects, but if you think you can enhance those projects. So, feel free to do that.

[## Advanced End-to-End DevSecOps Kubernetes Three-Tier Project using Terraform, AWS EKS, ArgoCD…

### Project Introduction:

blog.stackademic.com](https://blog.stackademic.com/advanced-end-to-end-devsecops-kubernetes-three-tier-project-using-aws-eks-argocd-prometheus-fbbfdb956d1a?source=post_page-----0ce8d2f62293---------------------------------------)

[## I Built a Fault-Tolerant Kubernetes Cluster So You Don't Have To

### I built a Fault-Tolerant highly available Kubernetes Cluster So You Don't Have To. Introduction We've all been there …

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/i-built-a-fault-tolerant-kubernetes-cluster-so-you-dont-have-to-efc4d2b9879b?source=post_page-----0ce8d2f62293---------------------------------------)

[## Building a Complete DevSecOps Project (Part 1) - Automating AWS Infrastructure with Terraform...

### Building a Complete DevSecOps Project (Part 1) - Automating AWS Infrastructure with Terraform Cloud & GitHub Actions…

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/building-a-complete-devsecops-project-part-1-automating-aws-infrastructure-with-terraform-cloud-a51e98b95783?source=post_page-----0ce8d2f62293---------------------------------------)

[## Advanced End-to-End DevSecOps Kubernetes Three-Tier Project using Terraform, Azure AKS, fluxCD...

### "" is published by Aman Pathak | DevOps | AWS | K8s | Terraform | ML in Stackademic.

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/advanced-end-to-end-devsecops-kubernetes-three-tier-project-using-azure-aks-fluxcd-prometheus-cca3c5e61953?source=post_page-----0ce8d2f62293---------------------------------------)

[## DevSecOps Mastery: A Step-by-Step Guide to Deploying Tetris on AWS EKS with Jenkins and ArgoCD

### "" is published by Aman Pathak | DevOps | AWS | K8s | Terraform | ML in Stackademic.

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/devsecops-mastery-a-step-by-step-guide-to-deploying-tetris-on-aws-eks-with-jenkins-and-argocd-3adcf21b3120?source=post_page-----0ce8d2f62293---------------------------------------)

[## Configure RBAC on Production Ready EKS Cluster

### Configure RBAC on Production Ready EKS Cluster Introduction Managing user roles and permissions is a critical part of…

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/configure-rbac-on-production-ready-eks-cluster-fb7d86f861db?source=post_page-----0ce8d2f62293---------------------------------------)

[## Deploy a Go Application on an EKS Cluster using GitHub Actions, Terraform, Helm, and ArgoCD

### Advanced End-to-End real-time Kubernetes Terraform DevSecOps and DevOps Project

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/deploy-go-application-on-eks-cluster-using-github-actions-terraform-helm-and-argocd-3f76c447dacd?source=post_page-----0ce8d2f62293---------------------------------------)

[## How to Package and Publish Your Custom Helm Charts- A Hands-On Tutorial

### How to Package and Publish Your Custom Helm Charts- A Hands-On Tutorial Introduction In this guide, we will explore how…

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/how-to-package-and-publish-your-custom-helm-charts-a-hands-on-tutorial-c922c54f94a4?source=post_page-----0ce8d2f62293---------------------------------------)

[## Configure ArgoCD, Prometheus, Grafana & AWS Load Balancer Controller on EKS Cluster using Terraform

### Configure ArgoCD, Prometheus, Grafana & AWS Load Balancer Controller on EKS Cluster using Terraform. Introduction In…

amanpathakdevops.medium.com](https://amanpathakdevops.medium.com/configure-argocd-prometheus-grafana-aws-load-balancer-controller-on-eks-cluster-using-terraform-831d46068b1b?source=post_page-----0ce8d2f62293---------------------------------------)

## **Best Practices**

Once you complete all the above projects. Now you are one step away from a Job-ready DevOps & Cloud Engineer, which is Best Practices.

You have to remember one thing that creating EC2 deploy the multiple applications can do for anyone. But if you are not following the best practices while doing all the above, then you never become a Job-Ready Engineer.

**Best practices are patterns that reduce pain, not rules you blindly follow.**

A lot of people ask me, “Aman, Best Practices always come from Industry Projects,” and my reply is, “Yes, definitely. But there are a few practices that a beginner must know about, like Dockerfile best practices, CICD pipelines optimisation, etc On the Internet, there are multiple articles available that help you to understand the perspective of a particular person, and in the end, the article should influence you to follow the same practices when you are doing any activities in your Projects. Start talking to people in the community and take the feedback on your learning or on their learning in the post’s comments or wherever possible.

If you need my help, feel free to reach out to me. I will talk about community and network engagements in the Bonus Tip.

## **Phase-4**

## **Job-Hunting & Upskilling**

It’s enough to learn now as you have the basic to intermediate level of knowledge for a Job-Ready DevOps Engineer.

Now you have to create your resume, update your LinkedIn Profile and start applying for Jobs on Naukri[India], Indeed and LinkedIn. You have to remember one thing about these two platforms:

* On Naukri/Indeed, recruiters are looking for candidates
* On LinkedIn, Candidates have to reach out to recruiters and ask them for the Openings and share their fields of expertise, etc.  
  Try to get referrals, if possible.
* Now, we have to talk about one of the important things, which is how much time we should spend on applying for the Jobs.  
  A lot of people apply for the job the entire day and overthink or wait for the calls. But please don’t do that. Please don’t waste your whole day applying and thinking about the company’s response. Just apply and move forward.  
  2–3 hours would be enough for applying the job. After that, keep learning and upskilling, as DevOps is all about upskilling.  
  As we skipped a few tools like Ansible and Monitoring tools. So Monitoring and configuration management tools can be added later once the core foundation is strong. And if you follow this plan with no desperation and with lots of dedication. **I can definitely say you can crack 8 out of 10 interviews easily for a fresher level or intermediate level roles.**

**Rejections are normal. Silence is normal. It’s not a reflection of your worth or skill; it’s part of the process.**

I wish you the best for the coming year 2026. I have my own resolutions for the coming year. I have to upskill myself a lot and have to share my learning with the community and with you guys.

I hope my insights and recommendations will help you in your career and that you achieve a lot.

### Let’s make 2026 amazing.

Feel free to reach out to me on Discord. I will respond to you as soon as possible.

**If you’re starting DevOps in 2026, bookmark this roadmap, follow it phase by phase, and don’t rush. Consistency beats intensity every single time.**

*Signing off*

*Aman Pathak*

🚀 **Enjoyed this content?**  
If you found it useful, don’t forget to **👏 clap, 🔄 share, and 💬 follow** for more DevOps & Cloud insights.

💡 Want to discuss **trending technologies in DevOps & Cloud**?

* 👥 **Join the community** on [Discord](https://discord.gg/jdzF8kTtw2)
* 🎥 **I am** **on** [YouTube](https://www.youtube.com/@aman-pathak/)
* 🌐 **Explore all my socials & blogs** → [Linktree](https://linktr.ee/Aman_Pathak)

🤝 **1:1 Mentorship**  
If you’re looking for personalised guidance in DevOps & Cloud (career growth, projects, real-world problem-solving), I’m opening limited slots for **1:1 mentorship**. Drop me a DM to know more.

👉 Keep experimenting. Keep learning. Keep growing!