---
title: "9 Commands I Run in the First 3 Minutes of Every Production Incident"
url: https://medium.com/p/33819c35de43
---

# 9 Commands I Run in the First 3 Minutes of Every Production Incident

[Original](https://medium.com/p/33819c35de43)

# 9 Commands I Run in the First 3 Minutes of Every Production Incident

## After 11 years on-call, these are the only ones that matter when the pager wakes me up.

[![Bug to Solution](https://miro.medium.com/v2/resize:fill:64:64/1*6bumuD_nTGP4wnyWr9-Dzw.png)](https://medium.com/@BugToSolution?source=post_page---byline--33819c35de43---------------------------------------)

[Bug to Solution](https://medium.com/@BugToSolution?source=post_page---byline--33819c35de43---------------------------------------)

3 min read

·

May 25, 2026

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D33819c35de43&operation=register&redirect=https%3A%2F%2Faws.plainenglish.io%2F9-commands-i-run-in-the-first-3-minutes-of-every-production-incident-33819c35de43&source=---header_actions--33819c35de43---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

I don’t guess. I don’t join Slack calls first. I run commands.

Here is exactly what I type when production breaks. No fluff. No theory. Just the sequence that consistently gives me signal fastest.

## 1. Global Health Check (30 seconds)

```
uptime && free -h && df -h && ss -s
```

This tells me if the machine itself is dying. Disk full, OOM, or too many connections. I have seen dozens of “application bugs” that were actually disk full.

## 2. Which Service Is Actually Broken?

```
kubectl get pods -A --sort-by=.status.startTime  
kubectl top pods -A
```

Or for Docker:

```
docker stats --no-stream
```

## 3. Application Logs (Never Skip)

```
kubectl logs <pod> --tail=200 | tail -50  
journalctl -u <service> -xe --since "15 min ago"
```

## 4. Database Is Usually Guilty

```
psql -c "SELECT pid, query, state, wait_event FROM pg_stat_activity WHERE state != 'idle';"  
psql -c "SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 8;"
```

When it’s bad, I open the **PostgreSQL War Room** and follow the exact decision tree for runaway queries or lock contention.

→ [**PostgreSQL War Room**](https://yusufseyitoglu.gumroad.com/l/postgresql-war-room)

## 5. Redis Reality Check

```
redis-cli INFO memory  
redis-cli INFO stats | grep -E "keyspace|evicted|rejected"  
redis-cli CLIENT LIST | wc -l
```

Cache stampede or memory pressure is behind more outages than people admit. **Redis War Room** has the 10 fix patterns I actually use.

→ [**Redis War Room**](https://yusufseyitoglu.gumroad.com/l/redis-war-room)

## 6. Docker/Container Level

```
docker ps -a  
docker inspect <container> | grep -E "OOMKilled|RestartCount|ExitCode"
```

I keep **Docker War Room** ready for the exact commands on CrashLoopBackOff and volume failures.

→ [**Docker War Room**](https://yusufseyitoglu.gumroad.com/l/docker-war-room)

## 7. Linux Server Deep Dive

```
dmesg -T | tail -30  
cat /proc/meminfo | grep -E "MemTotal|MemAvailable|Committed"  
iotop -o -b -n 3
```

**Linux War Room** covers the exact fix patterns for OOM killer, disk exhaustion, and high load.

→ [**Linux War Room**](https://yusufseyitoglu.gumroad.com/l/linux-war-room)

## 8. Network & Connectivity

```
ss -plant | head -20  
curl -I -m 5 https://internal-service/health
```

## 9. The Master Playbook

When it’s bigger than one service, I go straight to the full incident protocol.

→ [**Production Incident War Room**](https://yusufseyitoglu.gumroad.com/l/production-war-room)

## The Bundle I Actually Use

I keep all of them open during every rotation:

* Production Incident War Room (overall command)
* PostgreSQL War Room
* Redis War Room
* Docker War Room
* Linux War Room

The **DevOps War Room Bundle** is the only purchase I have never regretted.

→ [**DevOps War Room Bundle — All 4 Guides**](https://yusufseyitoglu.gumroad.com/l/devops-war-room-bundle)

## Final Truth

Most incidents are not complex. They are simple things that were ignored until they weren’t.

The engineers who resolve fastest don’t know more secrets. They just look in the right order.

Run these 9 commands next time you get paged. You will thank yourself at 3:47 AM.

**Froquiz** has 10,000+ questions across SQL, Docker, Git, AWS, JavaScript, Java, Python, React, Microservices and more — plus a Senior Dev Challenge with real scenario-based questions, not syntax drills. → [**Froquiz**](https://froquiz.com/)