---
title: "Docker, Jenkins, Prometheus, locally?! Here’s the stack that finally worked for me"
url: https://medium.com/p/61c62167f66f
---

# Docker, Jenkins, Prometheus, locally?! Here’s the stack that finally worked for me

[Original](https://medium.com/p/61c62167f66f)

Member-only story

# Docker, Jenkins, Prometheus, locally?! Here’s the stack that finally worked for me

## *I spent weeks testing Jenkins, Prometheus, and Docker locally; here’s* 👇 *the setup that finally worked.*

[![<devtips/>](https://miro.medium.com/v2/resize:fill:64:64/1*_uB1tyY74dvRdj0J6DQyxQ.png)](https://medium.com/@dev_tips?source=post_page---byline--61c62167f66f---------------------------------------)

[<devtips/>](https://medium.com/@dev_tips?source=post_page---byline--61c62167f66f---------------------------------------)

6 min read

·

Jun 30, 2025

--

1

Listen

Share

More

> Want to read this article for free? You can find the full version on my website → [runitbare.com](https://runitbare.com/docker-jenkins-prometheus-locally-heres-the-stack-that-finally-worked-for-me/)

## ✨ TL;DR — Local DevOps Stack That Actually Works

**The Problem**: Cloud-based DevOps is expensive, slow to iterate, and hard to debug.  
**The Fix**: A full-featured DevOps stack you can run locally with Docker Compose.

### Core Stack Includes:

* Jenkins (CI/CD)
* Prometheus + Grafana (Monitoring)
* Loki + Promtail (Logs)
* NGINX / Traefik (Reverse Proxy)
* Mailhog (Email testing)
* Postgres + Redis (App support)

### Lessons Learned:

* Start small, stack later.
* Pin your versions.
* Healthchecks = sanity.
* Docker Compose > premature Kubernetes.
* Keep a “stack journal.”

I didn’t need much.

Just a CI pipeline that wouldn’t crash, some metrics I could actually understand, and a way to test everything locally before the cloud burned another hole in my wallet.

What I got instead?

A Jenkins instance that kept dying on startup, Prometheus scraping air, and Docker Compose logs that looked like they were trying to write a novel.

I almost gave up

but after weeks of trial, error, breaking my laptop (twice), and rage-Googling every DevOps blog on the internet, I finally landed on a local setup that just… worked.

**No Kubernetes. No AWS bills. No 4am Slack messages asking, “why is staging down?”**

This isn’t a tutorial. It’s a survival guide I battle-tested myself and one you can copy. 🤝

## What even is a DevOps stack (locally, not in theory)?

When most people talk about DevOps, they’re picturing cloud-native setups with autoscaling Kubernetes clusters and fancy dashboards that cost more than your rent. But when you’re working solo, experimenting, or just trying to learn without breaking production, **you need something you can run on your own machine.**

Here’s what a **local-first DevOps stack** looks like to me:

* **Docker:** The container backbone. Everything lives in a container, including Jenkins and Prometheus.
* **Jenkins:** Still the most flexible CI/CD engine. Yes, it’s old-school. Yes, it still slaps, when it works.
* **Prometheus + Grafana:** For metrics and monitoring. Prometheus scrapes, and Grafana makes it pretty.
* **Loki:** Log aggregation. Because `docker logs` isn’t enough after 5 containers.
* **NGINX** or **Traefik:** For reverse proxy and routing multiple services under one localhost domain.
* **Mailhog/Redis/Postgres:** Optional services I spin up when testing email, caching, or database flows.

That’s the baseline.

No AWS. No GCP. No EKS. Just **containers, ports, and the occasional terminal tantrum**.

Press enter or click to view image in full size

![]()

## The `docker-compose.yml` Setup That Finally Clicked

You can’t talk local DevOps without talking `docker-compose.yml`. This file is your command center the difference between a one-liner setup and hours of manual madness.

Here’s a simplified version of what I use:

```
version: "3.8"  
  
services:  
  jenkins:  
    image: jenkins/jenkins:lts-jdk17  
    ports:  
      - "8080:8080"  
    volumes:  
      - jenkins_home:/var/jenkins_home  
  
  prometheus:  
    image: prom/prometheus  
    ports:  
      - "9090:9090"  
    volumes:  
      - ./prometheus.yml:/etc/prometheus/prometheus.yml  
  
  grafana:  
    image: grafana/grafana  
    ports:  
      - "3000:3000"  
    volumes:  
      - grafana_data:/var/lib/grafana  
  
  loki:  
    image: grafana/loki:2.9.0  
    ports:  
      - "3100:3100"  
    command: -config.file=/etc/loki/local-config.yaml  
  
  nginx:  
    image: nginx:stable  
    ports:  
      - "80:80"  
    volumes:  
      - ./nginx.conf:/etc/nginx/nginx.conf  
  
  mailhog:  
    image: mailhog/mailhog  
    ports:  
      - "8025:8025"  
      - "1025:1025"  
  
  redis:  
    image: redis  
    ports:  
      - "6379:6379"  
  
  postgres:  
    image: postgres:14  
    ports:  
      - "5432:5432"  
    environment:  
      POSTGRES_USER: dev  
      POSTGRES_PASSWORD: dev  
      POSTGRES_DB: app_db  
    volumes:  
      - pgdata:/var/lib/postgresql/data  
  
volumes:  
  jenkins_home:  
  grafana_data:  
  pgdata:
```

### Notes That Saved Me

* **Separate** `.env` **file**: Don't hardcode secrets or ports.
* **Mount your configs**: Prometheus and NGINX configs are easier to tweak this way.
* **Use volumes for stateful services**: Jenkins, Grafana, Postgres keep their state between restarts.
* **Avoid** `depends_on` **when possible**: It doesn't wait for service readiness. Use `restart: unless-stopped` and health checks instead.

This config gave me something I could build on and break without stress. Every piece lives in a container. If something goes wrong, I nuke and rebuild in seconds.

## My Local DevOps Folder Structure (a.k.a. the Sanity Layout)

After several Frankenstein setups, I landed on a structure that made sense, kept things modular, and let me debug fast.

```
/devops-stack  
├── docker-compose.yml  
├── .env  
├── README.md  
├── prometheus/  
│   └── prometheus.yml  
├── grafana/  
│   └── provisioning/  
│       ├── datasources/  
│       └── dashboards/  
├── loki/  
│   └── local-config.yaml  
├── nginx/  
│   └── nginx.conf  
├── jenkins/  
│   └── jobs/  
│       └── sample-job.groovy  
├── volumes/  
│   ├── grafana/  
│   ├── jenkins/  
│   └── postgres/  
└── logs/  
    └── stack.log
```

## Why This Setup Works

### 🔹 `prometheus/`

Custom scrape configs live here. I version them in Git so I know what changed and when.

### 🔹 `grafana/provisioning/`

This lets me preconfigure dashboards + data sources on startup no more manual clicking every time I rebuild.

### 🔹 `loki/`

Central place for Loki’s `local-config.yaml`. You’ll tweak this a lot if you’re aggregating logs from multiple containers.

### 🔹 `nginx/`

Keeps proxy configs out of the root. Lets me reload and test routing changes quickly.

### 🔹 `jenkins/jobs/`

Stores pipeline definitions, groovy scripts, or seed jobs. Easier than dealing with Jenkins UI every time.

### 🔹 `volumes/`

Optional, but useful for mounting persistent data. You can inspect/debug stateful services here without diving into Docker internals.

### 🔹 `logs/`

Redirected container or custom logs for quick debugging. Especially useful when Promtail isn’t playing nice.

## *What I’d Do Differently If I Started Today*?

### 1. Don’t Start with Jenkins

Jenkins is powerful but heavy. If you just want to learn CI/CD, start with something lighter like **GitHub Actions** (locally with [act](https://github.com/nektos/act)) or **Drone CI**. Jenkins comes with baggage plugins, config groans, and XML nightmares.

### 2. Don’t Over-Engineer Monitoring

You don’t need Prometheus + Grafana + Loki + Tempo just to run a blog. Start with logs (`docker logs`, maybe `Mailhog`) and add metrics when you have something worth monitoring.

### 3. Stick to Docker Compose

I wasted days experimenting with Minikube, Kind, and Kubernetes when all I needed was a solid `docker-compose.yml`. Unless you're prepping for a cloud deployment or certification, **K8s will slow you down** early on.

### 4. Keep a “Stack Journal”

Every time I broke something or fixed a weird bug, I wrote it down. That journal became my survival guide and later, this blog post. Start one. Seriously.

## Copy-Paste Starter: A Minimal Local DevOps Stack

If you’re reading this and thinking “Okay but I just want to try something quick,” here’s your **minimum viable DevOps** stack:

```
mkdir devops-mini && cd devops-mini  
touch docker-compose.yml  
yaml  
Copy  
Edit
```

```
# docker-compose.yml  
version: '3.8'  
  
services:  
  jenkins:  
    image: jenkins/jenkins:lts-jdk17  
    ports:  
      - "8080:8080"  
    volumes:  
      - jenkins_home:/var/jenkins_home  
  
  grafana:  
    image: grafana/grafana  
    ports:  
      - "3000:3000"  
  
volumes:  
  jenkins_home:
```

```
docker compose up -d
```

Boom. CI + Monitoring, no cloud needed.

Add Postgres, Redis, Loki, Prometheus, or NGINX only when you feel like breaking things again. And trust me you will.

## Wrapping Up: Build It. Break It. Own It.

Setting up a local DevOps stack wasn’t easy. It wasn’t elegant. It definitely wasn’t fast.

But it taught me more about how real systems work than any cloud dashboard or YouTube tutorial ever could.

When you’re forced to run Jenkins on your own machine, wire up Grafana dashboards from scratch, and untangle why your containers can’t talk to each other **you stop being a script-runner and start thinking like a systems engineer**.

So if you’re stuck waiting for your CI to deploy, or tired of debugging in a black-box cloud environment…

🔥 **Spin up your own stack. Break things. Fix them. Learn loud.**

And hey if this article helped even a little,  
 **Clap, Comment, Share.**  
 Let’s help more devs get over the fear of building infra from scratch.

## Continue Reading…

[## Self-hosting like a final boss: what I actually run on my home lab (and why)

### Forget the hype. Here’s what you can realistically self-host in 2025 without losing your mind or your network.

medium.com](https://medium.com/devlink-tips/self-hosting-like-a-final-boss-what-i-actually-run-on-my-home-lab-and-why-ee6dc7404400?source=post_page-----61c62167f66f---------------------------------------)

[## Zero Trust, One Router: Hardening Your Home Lab Like a Cyber Fortress.

### Build military-grade security into your weekend home lab without turning your hallway into a datacenter.

medium.com](https://medium.com/@devlink/zero-trust-one-router-hardening-your-home-lab-like-a-cyber-fortress-567fc3bdf880?source=post_page-----61c62167f66f---------------------------------------)

[## Burned out, done, ready to quit coding, but a 5-minute habit changed everything

### When even Stack Overflow couldn’t save me, a single sticky note did. It was Minimum Viable Effort → Consistency →…

medium.com](https://medium.com/devlink-tips/burned-out-done-ready-to-quit-coding-but-a-5-minute-habit-changed-everything-a9fc77ab1a7b?source=post_page-----61c62167f66f---------------------------------------)