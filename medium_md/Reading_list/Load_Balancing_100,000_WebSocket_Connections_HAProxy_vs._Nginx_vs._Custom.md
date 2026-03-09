---
title: "Load Balancing 100,000 WebSocket Connections: HAProxy vs. Nginx vs. Custom"
url: https://medium.com/p/4fe78f68c1ce
---

# Load Balancing 100,000 WebSocket Connections: HAProxy vs. Nginx vs. Custom

[Original](https://medium.com/p/4fe78f68c1ce)

Member-only story

# Load Balancing 100,000 WebSocket Connections: HAProxy vs. Nginx vs. Custom

[![Yash Batra](https://miro.medium.com/v2/resize:fill:64:64/1*qzg4k1dbmci1Z47Qm6BTsQ@2x.jpeg)](/@yashbatra11111?source=post_page---byline--4fe78f68c1ce---------------------------------------)

[Yash Batra](/@yashbatra11111?source=post_page---byline--4fe78f68c1ce---------------------------------------)

5 min read

·

May 26, 2025

--

15

Listen

Share

More

*What I learned after three sleepless nights scaling real-time chat for 100,000 concurrent users*

The notification came at 2:47 AM. Our real-time chat application was buckling under the weight of 80,000 concurrent WebSocket connections, and users were experiencing dropped messages and connection timeouts. By morning, we needed to handle 100,000+ connections reliably. This is the story of how we solved it, and the hard-learned lessons about WebSocket load balancing at scale.

![]()

## The Problem: When Simple Solutions Break Down

Traditional HTTP load balancing seems straightforward — distribute requests across servers, and you’re done. WebSocket connections are different beasts entirely. They’re persistent, stateful, and sticky. When a user connects, they maintain that connection for the duration of their session, sometimes hours at a time.

Our initial setup was embarrassingly simple: a single Node.js server handling all connections. It worked beautifully for our first 10,000 users. At 50,000, we started seeing memory pressure. At 80,000, the entire system became unstable.

The wake-up call came when our biggest client — a financial trading platform — couldn’t get real-time price updates during market open. Every second of downtime translated to real money lost.

## Round One: HAProxy (The Old Reliable)

HAProxy felt like the obvious choice. It’s battle-tested, handles millions of connections daily across the internet, and has excellent WebSocket support. Our configuration was straightforward:

```
frontend websocket_frontend  
    bind *:80  
    default_backend websocket_servers  
  
backend websocket_servers  
    balance source  
    server ws1 10.0.1.10:3000 check  
    server ws2 10.0.1.11:3000 check  
    server ws3 10.0.1.12:3000 check
```

The `balance source` directive ensures that connections from the same IP address always route to the same backend server—crucial for maintaining WebSocket session state.

**The Results:**

* Successfully handled 100,000+ concurrent connections
* CPU usage remained below 15% on our load balancer
* Memory footprint was surprisingly small (~2GB)
* Connection establishment time: ~45ms average

**The Gotchas:** HAProxy’s session persistence based on source IP became problematic when users connected from behind corporate NATs. We’d see thousands of connections funneled to a single backend server while others sat idle.

The solution required switching to cookie-based persistence and modifying our WebSocket handshake to include session tokens. This added complexity but distributed load more evenly.

Press enter or click to view image in full size

![]()

## Round Two: Nginx (The Swiss Army Knife)

Nginx’s appeal was its versatility. We were already using it for HTTP traffic, and consolidating our load balancing seemed logical. The configuration required the `stream` module:

```
stream {  
    upstream websocket_backend {  
        ip_hash;  
        server 10.0.1.10:3000;  
        server 10.0.1.11:3000;  
        server 10.0.1.12:3000;  
    }  
  
    server {  
        listen 80;  
        proxy_pass websocket_backend;  
        proxy_timeout 1s;  
        proxy_responses 1;  
    }  
}
```

**The Results:**

* Handled 100,000 connections with room to spare
* Better integration with our existing infrastructure
* Built-in health checking and failover
* Connection establishment time: ~52ms average

**The Surprise:** Nginx consumed significantly more memory than HAProxy for the same workload — about 40% more. This wasn’t documented anywhere we could find, but our monitoring made it clear. For every 10,000 concurrent connections, Nginx used approximately 800MB more RAM than HAProxy.

The `ip_hash` directive provided better distribution than HAProxy's default source balancing, but we still encountered the corporate NAT problem.

## Round Three: Custom Solution (The Nuclear Option)

After wrestling with session persistence issues in both HAProxy and Nginx, we decided to build our own WebSocket-aware load balancer. The idea was simple: instead of relying on IP-based routing, we’d implement application-layer routing based on user sessions.

Using Go, we built a lightweight proxy that:

1. Intercepts WebSocket handshakes
2. Extracts user authentication tokens
3. Routes connections based on consistent hashing of user IDs
4. Maintains a real-time map of user-to-server assignments

```
type ConnectionRouter struct {  
    servers []string  
    userMap sync.Map  
    hashRing *consistent.Map  
}  
  
func (cr *ConnectionRouter) RouteConnection(userID string) string {  
    return cr.hashRing.Get(userID)  
}
```

**The Results:**

* Perfect load distribution — no more NAT problems
* Connection establishment time: ~38ms average
* Lowest memory usage of all three solutions
* Built-in connection tracking and analytics

**The Cost:** Development time was substantial — three weeks for the initial version, ongoing maintenance, and the responsibility of maintaining critical infrastructure. Every bug became our problem to solve.

## Performance Comparison: The Numbers

After running identical workloads across all three solutions:

Press enter or click to view image in full size

![]()

## The Hidden Costs Nobody Talks About

Beyond raw performance numbers, each solution carried different operational burdens:

**HAProxy** required deep understanding of its configuration syntax. Documentation is excellent, but the learning curve is steep. Debugging connection issues often meant diving into HAProxy logs and correlating them with application logs.

**Nginx** felt familiar but had subtle differences in WebSocket handling compared to HTTP. The stream module configuration is less documented than the HTTP module, leading to trial-and-error debugging sessions.

**Custom solution** gave us complete control but made us responsible for edge cases we hadn’t considered. Handling connection timeouts, server failures, and graceful shutdowns required careful thought and testing.

## Real-World Lessons

Three months later, here’s what actually mattered in production:

**Monitoring is everything.** Regardless of which load balancer you choose, you need visibility into connection counts, distribution, and health checks. We built custom dashboards showing real-time connection maps and server load.

**Plan for failure.** All three solutions handle server failures, but they behave differently. HAProxy and Nginx immediately redirect new connections but may drop existing ones. Our custom solution could gracefully migrate connections, but this required additional complexity.

**Network topology matters more than you think.** Corporate firewalls, NAT configurations, and proxy servers all affect WebSocket connections differently than HTTP requests. Test with real user networks, not just your development environment.

## The Recommendation

For most teams facing this challenge, **start with HAProxy**. It’s the most proven solution for high-connection-count scenarios, has excellent documentation, and a large community. The configuration complexity is worth the reliability.

Consider Nginx if you’re already heavily invested in the Nginx ecosystem and can accept the higher memory usage. The operational simplicity of managing one load balancer type might outweigh the resource costs.

Build a custom solution only if you have specific requirements that neither HAProxy nor Nginx can meet, a strong development team, and the resources to maintain custom infrastructure. The performance gains are real, but they come at a significant operational cost.

## Six Months Later

Our HAProxy solution has been running in production for six months, handling peak loads of 180,000 concurrent connections during major market events. The 2:47 AM alerts have stopped, and our trading platform client renewed their contract.

Sometimes the boring, proven solution is the right choice. But understanding the alternatives — and their trade-offs — made us better engineers and helped us make an informed decision rather than just following tutorials.

The next time you’re facing a similar scaling challenge, remember that the best solution isn’t always the most technically impressive one. It’s the one your team can implement, monitor, and maintain reliably in production.

*If you’re dealing with WebSocket scaling challenges, I’d love to hear about your experiences. The real-world performance characteristics often differ significantly from theoretical benchmarks, and sharing these stories helps the entire community build better systems.*