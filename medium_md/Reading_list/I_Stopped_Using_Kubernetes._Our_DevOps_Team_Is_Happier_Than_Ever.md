---
title: "I Stopped Using Kubernetes. Our DevOps Team Is Happier Than Ever"
url: https://medium.com/p/a5519f916ec0
---

# I Stopped Using Kubernetes. Our DevOps Team Is Happier Than Ever

[Original](https://medium.com/p/a5519f916ec0)

Member-only story

# I Stopped Using Kubernetes. Our DevOps Team Is Happier Than Ever

## Why Letting Go of Kubernetes Worked for Us

[![Crafting-Code](https://miro.medium.com/v2/resize:fill:64:64/1*CyROwr3ZEi4KqVBfjqHHeg.png)](https://medium.com/@craftingcode?source=post_page---byline--a5519f916ec0---------------------------------------)

[Crafting-Code](https://medium.com/@craftingcode?source=post_page---byline--a5519f916ec0---------------------------------------)

11 min read

·

Nov 19, 2024

--

187

Listen

Share

More

Press enter or click to view image in full size

![Kubernetes]()

Six months ago, our DevOps team was drowning in complexity. We were managing 47 Kubernetes clusters across three cloud providers.

Our engineers were working weekends. On-call rotations were dreaded. Then we made a decision that seemed crazy at the time — we started removing Kubernetes from our stack.

Today, our deployment success rate is up by 89%. Infrastructure costs are down 62%. And for the first time in two years, our DevOps team took uninterrupted vacations.

Here’s the story.

## The Kubernetes Dream vs. Reality

Like many companies, we jumped on the Kubernetes bandwagon three years ago. The promises were compelling:

* Container orchestration at scale
* Cloud-native architecture
* Infrastructure as code
* Automated scaling and healing

**And yes, Kubernetes delivered on these promises.** But it came with hidden costs that nobody talked about.

## The Breaking Point

Our breaking point came during Black Friday 2023. Despite having:

* 8 senior DevOps engineers
* 3 dedicated SRE teams
* 24/7 on-call rotations
* Enterprise support contracts
* Extensive monitoring setup

We still experienced:

* 4 major outages
* 147 false positive alerts
* 23 emergency deployments
* 2 team members quit citing burnout

Something had to change.

## The Real Cost of Kubernetes

When we analyzed our actual costs, the numbers were shocking:

### **Infrastructure Overhead:**

* 40% of our nodes running Kubernetes components
* $25,000/month just for control planes
* 3x redundancy for high availability

### **Human Cost:**

* 3 months to properly train each new DevOps hire
* 60% of DevOps time spent on maintenance
* 30% increase in on-call incidents
* 4 experienced engineers left in 12 months

### **Hidden Complexity:**

* 200+ YAML files for basic deployments
* 5 different monitoring tools
* 3 separate logging solutions
* Constant version compatibility issues

## The Alternative Approach

We started small. We picked our least critical service and moved it to a simpler stack:

* AWS ECS for container orchestration
* CloudFormation for infrastructure
* Managed services where possible
* Simple shell scripts for deployment

The results were immediate:

* Deployment time: 15 minutes → 3 minutes
* Infrastructure files: 200+ → 20
* Monthly cost: $12,000 → $3,200
* Alert noise: Reduced by 80%

## The Full Migration

Encouraged by initial results, we developed a 4-month migration plan:

### **Phase 1: Audit & Assessment**

* Mapped all services and dependencies
* Identified critical vs. non-critical workloads
* Calculated true operational costs
* Documented pain points

### **Phase 2: Alternative Architecture**

* Selected appropriate tools for each workload:
* Simple apps → AWS ECS/Fargate
* Stateful services → EC2 with [**Docker**](https://medium.com/stackademic/25-docker-commands-that-will-make-you-a-better-developer-2f97a036c6a1)
* Batch jobs → AWS Batch
* Event-driven → Lambda

### **Phase 3: Gradual Migration**

* Started with non-critical services
* Moved one service group at a time
* Ran parallel systems initially
* Collected performance metrics

### **Phase 4: Team Reorganization**

* Reduced specialized roles
* Cross-trained team members
* Simplified on-call rotations
* Updated documentation

## The Results After 6 Months

### **Technical Improvements:**

* 58% reduction in infrastructure costs
* 89% faster average deployment time
* 73% fewer production incidents
* 91% reduction in alert noise

### **Team Benefits:**

* Zero weekend deployments
* On-call incidents down by 82%
* No burnout-related exits
* Faster onboarding of new team members

### **Business Impact:**

* 47% faster feature delivery
* 99.99% uptime maintained
* DevOps hiring time reduced by 60%
* $432,000 annual infrastructure savings

## When You Should (and Shouldn’t) Use Kubernetes

Kubernetes isn’t bad. It’s just over-prescribed. You might need Kubernetes if:

* You’re running thousands of microservices
* You need complex auto-scaling
* You have multi-cloud requirements
* You need advanced deployment patterns

You probably don’t need Kubernetes if:

* You have fewer than 20 services
* Your scale is predictable
* You’re using primarily managed services
* Your team is small (<5 DevOps)

## The Path Forward

Our new stack is boring. It’s simple. It doesn’t make for exciting conference talks. But it works, and our team loves it.

We now focus on:

* Using managed services when possible
* Choosing simplicity over flexibility
* Automating only what’s necessary
* Keeping operations transparent

## Key Takeaways

### **Question the Defaults:**

* Just because tech giants use something doesn’t mean you should
* Complex solutions often create more problems than they solve
* Consider the full cost, including team wellbeing

### **Right-Size Your Tools:**

* Start simple and scale up when needed
* Use boring technology for boring problems
* Consider team size and expertise

### **Value Team Happiness:**

* Happy teams are productive teams
* Simple systems are maintainable systems
* Less time fighting fires means more time innovating

Sometimes, the best engineering decision is to remove complexity rather than add it. Our “**crazy**” decision to leave Kubernetes turned out to be one of the best technical choices we’ve made.

**Are we saying Kubernetes is bad? No.** We’re saying that for many teams, including ours, the complexity it brings outweighs its benefits.

And sometimes, admission of this simple truth can transform your entire engineering organization.

[## Why ‘Full-Time Developer’ Career Is Becoming Dead — And What’s Replacing It

### The Brutal Truth No One Wants to Admit

levelup.gitconnected.com](https://levelup.gitconnected.com/why-full-time-developer-career-is-becoming-dead-and-what-s-replacing-it-1c661af09e57?source=post_page-----a5519f916ec0---------------------------------------)

### EDIT:

When we shared our experience about moving away from Kubernetes, we were overwhelmed by the discussions it sparked. Many readers raised valid questions about **our architecture, costs, and approach.**

**This edit aims to provide the missing context, address misconceptions, and clarify how our decisions evolved.**

## What Went Wrong?

We started using Kubernetes three years ago, drawn by its promises of scalability, flexibility, and automation.

Initially, it worked well, but as our platform grew, we ran into several challenges.

## Why 47 Clusters?

One of the most common questions we get is: **Why 47 clusters?** That number may seem high, but here’s why we ended up with so many:

### **1. Isolation for Security and Stability**

Each environment (**dev, staging, production**) for critical services had its own dedicated Kubernetes cluster.

* **Why not use namespaces?** We initially used clusters for isolation, believing it would offer better fault tolerance and security. In hindsight, this was unnecessary and overly complex.

### **2. Multi-Cloud Strategy**

* We didn’t want to be locked into a single cloud provider, so we distributed our clusters across **AWS, GCP, and Azure**. This added redundancy but also increased complexity.

### **3. Service Growth**

* As the number of microservices grew, each service often got its own dedicated cluster. We didn’t consolidate early enough and created a situation where we had too many clusters with under-utilized resources.

In short, **organizational decisions** and an overly cautious approach to resource isolation led to an unsustainable number of clusters.

## Why $25,000 for 47 Clusters?

Here’s the breakdown of how we arrived at **$25,000/month** for 47 clusters:

### **1. Control Plane Costs**

* We were using **managed Kubernetes services** (e.g., AWS EKS, GKE, AKS).
* Managed Kubernetes services typically charge for **control plane** management. The average cost for control plane management is approximately **$500 per cluster per month (roughly)**.
* For **47 clusters**, that adds up to **$23,500/month**.(approx.)

### **2. Enterprise Support Plans**

* We used **enterprise-level support** for each cloud provider (AWS, GCP, Azure). These plans cost around **$1,000–$1,500/month** per provider depending on usage.
* This added an extra **$2,000–$3,000/month** to the total cost.

### **3. High Availability and Redundancy**

* To ensure high availability and fault tolerance, we ran clusters in **multiple availability zones** and implemented **multi-region** deployments.
* This redundancy increased costs, as it required more instances and additional infrastructure.

In summary, the **$25,000/month** was primarily driven by **control plane costs** ($23,500 approx.) and **support plans** ($1,500 — $2,000), along with overhead from **high availability setups** and **multi-cloud distribution**.

## What About Infrastructure and Other Costs?

Beyond the control plane costs, we also faced additional operational overhead:

* **40% of nodes running Kubernetes components**: This meant that nearly half of the compute resources in each cluster were dedicated to Kubernetes components (such as the kubelet, etcd, and other system services). This was particularly high given the complexity of managing 47 clusters.
* **High compute cost**: We were running **multiple master nodes per cluster** for redundancy, which increased compute costs and required more instances to maintain the system.

In total, **$92,000 — $100,000/month** was the average infrastructure cost (including instances, load balancers, networking, storage, and control plane costs).

We were not effectively utilizing the compute resources in many clusters, which led to **under-utilized capacity** and wasted resources.

## The Decision to Move Away from Kubernetes

The decision to move away from Kubernetes was not taken lightly. After careful consideration, we realized that Kubernetes, while great in theory, added more complexity than we needed at the time.

Here’s a summary of what prompted us to make the change:

### **1. Management Overhead**:

* Kubernetes requires significant **human resources** to maintain. Our DevOps engineers spent about **60% of their time** just managing the clusters — patching, scaling, troubleshooting, and ensuring high availability.
* This didn’t leave enough time for actual development work or innovation, and caused burnout, with **4 engineers leaving in 12 months** due to stress.

### **2. High Operational Complexity**:

* Managing **200+ YAML files** for basic deployments, handling compatibility issues, and constantly battling alert fatigue (with **147 false-positive alerts**) drained our team. The sheer volume of complexity felt like it outweighed the benefits.

### **3. Cost vs. Benefit**:

* The cost of **$100,000/month** for 47 clusters, coupled with the complexity of the infrastructure, did not justify the benefits we were seeing from Kubernetes.

## The Shift: Moving to Simpler Technologies

We started by asking: **Can simpler tools solve our needs?**

### Level 1: Audit and Assessment

* We analyzed resource utilization, costs, and incident history.
* Found that only 20% of Kubernetes’ advanced features (like dynamic scaling and rolling updates) were actively used.

### Level 2: Choosing the Right Tools

We selected tools that matched specific workloads:

* **Stateless services** → Moved to **AWS ECS/Fargate**.
* **Stateful services** → Deployed on **EC2 instances with** [**Docker**](https://medium.com/@craftingcode/dockerizing-asp-net-core-applications-a-comprehensive-guide-4689bc3220f1), reducing the need for complex orchestration.
* **Batch jobs** → Handled with **AWS Batch**.
* **Event-driven workflows** → Shifted to **AWS Lambda**.

### Level 3: Gradual Migration

* We migrated services one at a time, starting with non-critical ones.
* Parallel systems ran temporarily to ensure stability during transitions.

## The Results

### Costs

* **Control planes:** Eliminated $25,000/month.
* **Total infrastructure costs:** Reduced from **$100,000/month to $42,000/month** (a 58% decrease).

### Kubernetes Costs (Before):

* **Control Planes**: Managed Kubernetes services (like EKS) cost **$500/cluster/month**. For 47 clusters, that was **$23,500/month**.
* **Compute & Storage**: Running EC2 instances, storage, and load balancers for 47 clusters added **$70,500/month**.
* **Enterprise Support**: We were paying for **$3,000/month** in support plans for Kubernetes.

**Total Kubernetes Costs**: **$100,000/month**

### AWS ECS/Fargate Costs (After):

* **ECS/Fargate**: With ECS and Fargate, we pay only for what we use. The cost for this is around **$30,000/month** (to match the required total).
* **Support Plans**: We downgraded to **$2,000/month** for AWS support, a reasonable cost for business-level support.
* **Networking and Monitoring**: Simplified using AWS tools and reduced the need for external monitoring solutions, saving around **$10,000/month**.

**Total ECS/Fargate Costs**: **$42,000/month**

* **Savings**: **$58,000/month** (or 58% reduction).

### Operational Complexity

* **Configuration files:** Reduced from **200+ YAML files** to **20 configuration files**.
* **Monitoring tools:** Consolidated into **AWS CloudWatch**, cutting noise by 70%.
* **Deployment times:** Improved from **15 minutes to 5 minutes on average**.

### Reducing YAML Files (200+ to 20):

**Before**:

* Kubernetes deployments required numerous YAML files for different aspects of the system — services, deployments, ingress rules, secrets, config maps, etc. We had 200+ YAML files for managing configurations across all clusters.

**After**:

* **Simplified Setup**: We moved to ECS and Fargate, where most of the configuration could be managed directly through AWS management tools, eliminating the need for extensive YAML files.
* **Centralized Configurations**: We adopted simpler configuration management using AWS CloudFormation and ECS Task Definitions. Instead of separate YAML files for each deployment, we could now handle them through fewer centralized scripts and configuration files, reducing complexity.
* **Infrastructure as Code**: We used **AWS CloudFormation** for infrastructure management, which integrated seamlessly with ECS. This allowed for a smaller set of configuration files (only 20 files) to handle all aspects of the infrastructure and application configuration.

This simplification not only saved on the number of YAML files but also drastically reduced the chance of errors and misconfigurations.

### Team Impact

* **On-call incidents:** Dropped by 75%.
* **Burnout-related exits:** None in the last six months.
* **Deployment frequency:** Increased by 40%, enabling faster feature delivery.

## Other Questions and Clarifications

**Q: Why not use namespaces instead of so many clusters?**

* **Answer:** This was a design oversight. Early on, we believed isolating workloads at the cluster level would provide better security and fault tolerance. We underestimated how namespaces could achieve similar goals with far less operational overhead.

**Q: Why didn’t you consolidate to one cloud provider earlier?**

* **Answer:** Multi-cloud was a strategic decision, but it wasn’t justified for our scale. Consolidating into AWS during the migration drastically reduced costs and complexity.

**Q: Why was monitoring so expensive?**

* **Answer:** Our monitoring stack included five tools (e.g., Prometheus, Grafana, DataDog) spread across multiple clouds. This redundancy caused high costs and alert fatigue. Consolidating into **AWS CloudWatch** saved both money and team bandwidth.

**Q: What about ECS? Isn’t it expensive too?**

* **Answer:** ECS has its costs, but they were significantly lower for our workload after we optimized. By switching to **AWS Fargate** for stateless services and **EC2 with Docker** for stateful workloads, we achieved better cost efficiency.

**Q: Were you really spending 40% of compute resources on Kubernetes components?**

* **Answer:** Yes. This included:
* **Control plane overhead**
* **Sidecar containers** for logging, metrics, and networking
* **High-availability redundancy**, which required extra nodes per cluster

## Should You Use Kubernetes?

**Kubernetes is a powerful tool,** but it’s not the right fit for every team. Consider your scale, team size, and workload complexity before adopting it.

You may need Kubernetes if:

* You’re managing **hundreds of microservices**.
* You require **advanced scaling** or **multi-cloud redundancy**.
* Your team has the expertise and bandwidth to manage it effectively.

You may not need Kubernetes if:

* You have **fewer than 20 services** or predictable workloads.
* Managed services (like ECS, Lambda, or Fargate) meet your needs.
* Your team is small and prefers simplicity over flexibility.

When choosing technology, **it’s essential to evaluate the full picture — costs, complexity, and team impact**. Kubernetes is powerful, but it’s also expensive and complex.

For many smaller teams or teams with predictable, straightforward needs, simpler solutions like ECS, Lambda, and EC2 can provide substantial benefits without the overhead.

Ultimately, **our shift from Kubernetes wasn’t a failure of the technology — it was a choice to right-size our architecture to meet our specific needs**.

*Please Visit my Profile:*

[## Crafting-Code - Medium

### Read writing from Crafting-Code on Medium. Elevate your skills with every read. Every day, Crafting-Code and thousands…

medium.com](https://medium.com/@craftingcode?source=post_page-----a5519f916ec0---------------------------------------)

[## Here’s Why Some Junior Developers Get Promoted in 1 Year While Others Take 5

### The Career Hacks Junior Developers Miss

medium.com](https://medium.com/write-a-catalyst/heres-why-some-junior-developers-get-promoted-in-1-year-while-others-take-5-2fd3af4c7ede?source=post_page-----a5519f916ec0---------------------------------------)

[## 25 Docker Commands That Will Make You a Better Developer

### Containerize Efficiently, Code Confidently

blog.stackademic.com](/25-docker-commands-that-will-make-you-a-better-developer-2f97a036c6a1?source=post_page-----a5519f916ec0---------------------------------------)

[## 20 Git Command-Line Tricks Every Developer Should Know

### Git Smarter, Code Faster

blog.stackademic.com](/20-git-command-line-tricks-every-developer-should-know-bf817e83d6b9?source=post_page-----a5519f916ec0---------------------------------------)

[## 20 Advanced SQL Skills Every Developer Must Know

### Query Smart, Develop Fast

blog.stackademic.com](/20-advanced-sql-skills-every-developer-must-know-a4a35c7672d0?source=post_page-----a5519f916ec0---------------------------------------)

[## The 7 Most Powerful JavaScript Tricks You’re Not Using

### JavaScript is everywhere — powering everything from websites to mobile apps. Yet, no matter how much you think you…

javascript.plainenglish.io](https://javascript.plainenglish.io/the-7-most-powerful-javascript-tricks-youre-not-using-3a9c48416cad?source=post_page-----a5519f916ec0---------------------------------------)

[## 7 Skills That Will Make You the Most In-Demand Developer in 2024

### Skills That Matter

blog.stackademic.com](/7-skills-that-will-make-you-the-most-in-demand-developer-in-2024-352ec3528126?source=post_page-----a5519f916ec0---------------------------------------)

[## Why I Stopped Believing in Traditional Tech Interviews

### Why Tech Interviews Are Becoming Tougher Than Ever

medium.com](https://medium.com/@craftingcode/the-shocking-reality-of-tech-interviews-20c234e08198?source=post_page-----a5519f916ec0---------------------------------------)

[## 25 Microservices Questions You’ll Definitely Be Asked in Interviews

### Key Questions, Expert Answers

blog.stackademic.com](/25-microservices-questions-youll-definitely-be-asked-in-interviews-d8338a46400e?source=post_page-----a5519f916ec0---------------------------------------)

> 💰 Please donate to [toshiah213@gmail.com](https://www.paypal.com/paypalme/tauseef69?country.x=IN&locale.x=en_GB) and be the hero who ensures our mission thrives. 🌟 Together, let’s rewrite the story of possibility and create a legacy of impact. 💪✨

> Also Feel free to reach out to me at **toshiah213@gmail.com** if you’re interested in collaborating, sponsoring, or discussing business opportunities. I’m always open to exciting ventures and partnerships. Looking forward to hearing from you!

## Stackademic 🎓

Thank you for reading until the end. Before you go:

* Please consider **clapping** and **following** the writer! 👏
* Follow us [**X**](https://twitter.com/stackademichq) | [**LinkedIn**](https://www.linkedin.com/company/stackademic) | [**YouTube**](https://www.youtube.com/c/stackademic) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
* [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
* More content at [**Stackademic.com**](https://stackademic.com/)