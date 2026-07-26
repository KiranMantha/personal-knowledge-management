---
title: "Nginx vs Caddy vs Traefik in 2026 — I Ran All Three Under Real Production Load"
url: https://medium.com/p/64e412f4062b
---

# Nginx vs Caddy vs Traefik in 2026 — I Ran All Three Under Real Production Load

[Original](https://medium.com/p/64e412f4062b)

# Nginx vs Caddy vs Traefik in 2026 — I Ran All Three Under Real Production Load

## Same Kubernetes cluster, same microservices, same TLS requirements. One proxy broke during ingress-nginx migration week. Guess which.

[![Yusuf Seyitoğlu](https://miro.medium.com/v2/resize:fill:64:64/1*TEJlOrcmm7RSveCt-72nPg.jpeg)](https://medium.com/@developeryusuf?source=post_page---byline--64e412f4062b---------------------------------------)

[Yusuf Seyitoğlu](https://medium.com/@developeryusuf?source=post_page---byline--64e412f4062b---------------------------------------)

7 min read

·

Jul 12, 2026

--

3

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D64e412f4062b&operation=register&redirect=https%3A%2F%2Fblog.stackademic.com%2Fnginx-vs-caddy-vs-traefik-in-2026-i-ran-all-three-under-real-production-load-64e412f4062b&source=---header_actions--64e412f4062b---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

I’ve terminated more TLS than I care to admit. Reverse proxies are the part of the stack everyone forgets until certificates expire, upstreams go silent, or — in March 2026 — your ingress controller hits end-of-life and compliance asks what your migration plan is.

A logistics client ran ingress-nginx on EKS for four years. Fine until it wasn’t supported. They asked me to compare **Nginx (F5 NIC)**, **Caddy**, and **Traefik** on the same cluster before picking a path forward. Same twelve microservices. Same cert issuer. Same load tests. I ran each as the edge for **six weeks**.

RKE2 v1.36 making Traefik the default ingress is not abstract news if you operate Rancher clusters. It is a migration ticket with a deadline.

## The Test Bed: Production Shape, Controlled Variables

Cluster: EKS, **12 services**, **~35,000 requests/minute** average, **~61,000** peak during dispatch windows. Mix of REST JSON, WebSocket tracking, and one large CSV export (15–40 MB responses).

Each proxy setup:

* Automatic TLS (Let’s Encrypt / ACME)
* HTTP/2 and HTTP/3 where supported
* Rate limiting on public endpoints
* Prometheus metrics scraped the same way
* Same pod resource requests: 2 CPU / 2Gi per ingress controller replica

I tracked: p50/p99 proxy latency, memory at idle and at 10k connections, config reload behavior, and **operator time per new service route**.

Six-week rotation schedule:

* **Weeks 1–2:** Nginx F5 NIC baseline, cert-manager ClusterIssuer validation, wrk suite calibration
* **Weeks 3–4:** Caddy on a parallel ingress class, HTTP/3 A/B on internal clients
* **Weeks 5–6:** Traefik with ingress-nginx annotation bridge, migration dry-run on two non-critical services
* **Week 6 cutover:** 60/40 Traefik/legacy split, incident on day three (documented below)

Corporate L4 load balancer in front: AWS NLB, **three AZs**, **~2.1 million connections/day** at peak. Every proxy had to honor `X-Forwarded-For` correctly or rate limits and audit logs lied. That constraint eliminated more "simple" configs than any benchmark did.

Operator time log (median over six weeks, **14 route changes**): Nginx **23 minutes**, Caddy **9 minutes**, Traefik **4 minutes** once label conventions landed — **38 minutes** on the first Traefik route before we wrote the schema doc.

## Throughput vs Operator Time — Pick Your Poison

**Nginx (F5 NIC ingress on Kubernetes):**

* Proxy throughput: **~46,000 req/s** in our wrk suite (2 KB JSON upstream) — highest of the three
* p99 proxy overhead: **~0.9ms** at median load
* Idle memory: **~35 MB** per controller pod; **~120 MB** at 10k connections
* New service route: **manual Ingress YAML + annotation review** — ~25 minutes including PR
* Strength: raw performance, massive community knowledge, every senior SRE has scars here

**Caddy 2.11 (standalone ingress on VMs + DaemonSet edge):**

* Proxy throughput: **~41,000 req/s** — **~11% behind** Nginx on pure JSON proxying
* p99 overhead: **~1.2ms** — TLS termination gap narrowed; automatic HTTPS is not a gimmick
* Idle memory: **~28 MB**; **~95 MB** at 10k connections
* New route: **12-line Caddyfile block** or JSON API push — ~8 minutes for a standard service
* HTTP/3 on by default. ECH support mattered for a client with aggressive TLS inspection policies.

**Traefik 3.7 (Kubernetes CRD + IngressRoute):**

* Proxy throughput: **~36,000 req/s** — lowest raw number, still **3x headroom** over peak traffic
* p99 overhead: **~1.6ms** under burst; token-bucket rate limiting smoother than Nginx leaky bucket for our spike pattern
* Idle memory: **~48 MB**; **~135 MB** at 10k connections
* New route: **label on Deployment** — often **zero** manual steps after conventions exist
* ingress-nginx annotation compatibility layer saved **two weeks** on migration — `rewrite-target`, `proxy-body-size`, most of what they already had

## TLS, Reloads, and the Config Formats You’ll Maintain at 2 AM

**Nginx:** Cert rotation via cert-manager worked. Config reload via `nginx -s reload` is battle-tested. When we fat-fingered a `proxy_pass` typo, Nginx refused reload and kept the old config — annoying in CI, lifesaving in prod.

**Caddy:** Automatic HTTPS is the real product. Two lines, cert appears, HTTP/3 works. JSON API reload with zero downtime felt like cheating on a homelab. In Kubernetes we still needed to wire cert storage — not hard, but not literally zero config at scale.

**Traefik:** Watching Docker/K8s events and building routes dynamically is magic until it isn’t — a mislabeled pod got public traffic for **eleven minutes** before we caught it in access logs. Convention documentation became mandatory: label schema, entrypoint names, middleware chains.

## Get Yusuf Seyitoğlu’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

WebSocket tracking for the fleet GPS service: all three handled it. Nginx needed explicit `Upgrade` headers. Caddy worked out of the box. Traefik needed the right entrypoint middleware — one wrong toggle and connections dropped every **45 seconds**.

Certificate lifecycle numbers: **47 active certs** across subdomains, Let’s Encrypt rate limit headroom mattered during migration. cert-manager renewal failures: **zero** on Nginx, **one** transient DNS propagation blip on Caddy (self-healed in **11 minutes**), **two** on Traefik when a misconfigured `dns01` solver stalled a wildcard — caught by Prometheus alert `certmanager_certificate_expiration_timestamp_seconds < 7 days`.

Monthly cost for three ingress controller replicas (compute only): Nginx NIC **~$186**, Caddy **~$142**, Traefik **~$198** (higher idle RSS). None of these move the CFO’s needle. **Operator hours** do — we estimated **~6 hours/month** saved on route churn with Traefik versus Nginx YAML surgery, roughly **$900/month** at loaded contractor rates. That’s the number that closed the deal.

## The Migration Week Incident

Cutover Tuesday, **09:40 local** — dispatch managers start their morning export ritual. Traefik at 60% traffic, ingress-nginx still handling legacy annotations on two services. A deployment rolled out with a malformed `Ingress` annotation — `nginx.ingress.kubernetes.io/proxy-read-timeout` set to `"30"` (seconds) on an export service that needed **300**.

Nginx ingress honored the low timeout. Traefik’s translated middleware did too — correctly, per config. Large CSV exports died at **30 seconds** flat. Users saw **502 Bad Gateway**. Error rate: **0% → 8%** in **three minutes**.

Support blamed “the new proxy.” Engineering blamed “the export service got slower.” Both wrong.

I started with → [**Production Incident War Room — The Step-by-Step Response Playbook**](https://yusufseyitoglu.gumroad.com/l/production-war-room) — the diagnosis tree for exactly this kind of “which layer is actually broken” triage, status codes included. **502** from the proxy: bad gateway, upstream closed or timed out. We extended the timeout annotation, confirmed upstream p99 was **42 seconds** for huge exports, set **300s** with a async export fallback on the roadmap.

Secondary issue: Traefik access logs went to stdout but **client IP was wrong** behind the corporate L4 load balancer until we set `forwardedHeaders.trustedIPs`. Mobile clients hit the wrong rate-limit bucket for **20 minutes** before we noticed.

For the node-level debugging — `journalctl`, connection tracking, file descriptor limits — → [**Linux War Room: 12 Fix Patterns for Disk-Full, OOM Killer & SSH Lockouts at 3 AM**](https://yusufseyitoglu.gumroad.com/l/linux-war-room) has the diagnosis tree I use when the proxy looks guilty but the kernel is lying. Turned out `nf_conntrack` table was **92% full** on two nodes from the export spike. Not a Traefik bug. A **connection tracking** budget we had never sized for long-lived downloads.

## When I Would Choose Nginx

* You terminate **massive** traffic on dedicated edge nodes and need every req/s
* Large-file streaming (GB-scale) where Nginx’s buffer tuning still wins
* Team has a decade of Nginx config and F5 support contract
* You are standardizing on F5 NIC post ingress-nginx EOL and want vendor continuity

## When I Would Choose Caddy

* Small cluster or VM fleet — **TLS just works** with minimal config
* Developer velocity over raw throughput; HTTP/3 and ECH matter
* You hate maintaining Certbot sidecars and annotation archaeology
* **<10 services**, mostly stable routes, homelab-to-production pipeline

## When I Would Choose Traefik

* Kubernetes-native stack with **frequent service churn** — labels beat YAML surgery
* Migrating off ingress-nginx in 2026 — annotation compatibility is real
* RKE2 / Rancher shops where Traefik is already the default path
* You want dynamic upstreams without reloading the world

## Verdict

There is no “best” proxy — only the one that matches your **operational model**.

For this client’s EKS fleet with weekly deploys and a migration deadline, **Traefik won** — not because it was fastest, but because **operator time** and ingress-nginx compatibility beat **11% throughput** we weren’t using. We kept **Nginx** on a dedicated edge VM for the CSV export CDN path where buffer tuning and raw streaming matter. **Caddy** runs my personal staging cluster because I refuse to maintain Certbot on a Saturday.

ingress-nginx EOL in March 2026 is not a reason to panic-migrate to the shiniest logo. It is a reason to **test** Traefik’s annotation bridge on your real Ingress objects, measure operator time per route, and keep Nginx where raw throughput still pays rent.

Pick the proxy you can debug at 2 AM. Then read the HTTP status codes and kernel limits that make every proxy look broken.

We didn’t stop at the bake-off. After Traefik won for the EKS fleet, I still migrated one low-risk internal service to Caddy on a VM edge — mostly to kill a Certbot timer that kept silently dying. The surprise wasn’t automatic HTTPS. It was the reload model.

→ [We Moved One Service From nginx to Caddy. Deleting the Certbot Timer Wasn’t the Win — the Reload Model Was](https://medium.com/p/247efe64b3cb)

## What You Should Do This Week

1. **If you still run ingress-nginx**, inventory annotations and test Traefik’s compatibility layer on a non-prod namespace. March 2026 EOL is not a surprise anymore — it’s a calendar event.
2. **Log** `X-Forwarded-For` **and upstream status** on every 502. Half of "proxy broke" is timeout misconfig.
3. **Check** `nf_conntrack` **usage** before blaming the ingress controller for connection drops on large downloads.
4. **Write a rate-limit test** that hits the same endpoint from two IP paths — corporate LB misconfig shows up before customers complain.
5. **Document your label/schema conventions** before Traefik auto-discovery becomes auto-misrouting.

Proxies do not create outages. They reveal the config you did not test. Make sure you know what’s on the other side.

Your reverse proxy is the door everyone walks through. Make sure you know what’s on the other side.

**How fast can you tell a gateway timeout from a conntrack table exhaustion?** That’s the real skill — not memorizing status codes, but recognizing failure patterns before the postmortem.

That’s exactly why I started building [**The Production Engineering Library**](https://yusufseyitoglu.gumroad.com/l/production-engineering-library).

Instead of isolated tutorials, it’s a growing collection of practical books covering production debugging, incident response, Kubernetes, system design, distributed systems, backend architecture, performance engineering, databases, APIs, Linux, Docker, Git, and the engineering decisions that only become visible in production.

If you enjoy articles that compare real production trade-offs instead of repeating documentation, you’ll probably find something valuable inside.

→ [**The Production Engineering Library**](https://yusufseyitoglu.gumroad.com/l/production-engineering-library)