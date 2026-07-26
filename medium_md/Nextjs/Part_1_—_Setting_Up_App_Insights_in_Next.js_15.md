---
title: "Part 1 — Setting Up App Insights in Next.js 15"
url: https://medium.com/p/085b56149ceb
---

# Part 1 — Setting Up App Insights in Next.js 15

[Original](https://medium.com/p/085b56149ceb)

# **Part 1 — Setting Up App Insights in Next.js 15**

[![Ketan Chavan](https://miro.medium.com/v2/resize:fill:64:64/1*qI2oCa8bWY3MiXoXJeaYmQ.png)](https://ketan-chavan.medium.com/?source=post_page---byline--085b56149ceb---------------------------------------)

[Ketan Chavan](https://ketan-chavan.medium.com/?source=post_page---byline--085b56149ceb---------------------------------------)

9 min read

·

Mar 7, 2026

--

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D085b56149ceb&operation=register&redirect=https%3A%2F%2Fjavascript.plainenglish.io%2Fpart-1-setting-up-app-insights-in-next-js-15-085b56149ceb&source=---header_actions--085b56149ceb---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

## I Threw Away the App Insights SDK & Started Over. Here’s What Actually Works in Next.js 15.

> ***Series: App Insights in Next.js — From Zero to “Why Is My Error Rate 3.5%?”******Part 1: Setup & Instrumentation (you are here)***  *Part 2 —* [*Killing 95% of False Errors in App Insights*](https://ketan-chavan.medium.com/killing-95-of-false-errors-in-app-insights-94e37a9638a8) *Part 3 — WAF Rules That Actually Work for Next.js*

It was 11 PM on a Tuesday. I was staring at our Azure Application Insights dashboard, watching a flat line where traces should be. We’d just migrated from Pages Router to App Router. The old `@microsoft/applicationinsights-web` SDK? Dead. Server Components don't have a `window` object. Server Actions don't run in the browser. The entire rendering model had changed, and our observability was just... gone.

That was three months ago. Today, we’re tracking every server-rendered page, every Redis cache hit, every Strapi CMS call, and every exception — all flowing into App Insights with proper parent-child trace relationships. No legacy SDKs. No hacks. Just OpenTelemetry.

Here’s how we got there.

## Why the Old SDK Doesn’t Work Anymore

Let me save you the two days I spent trying to make it work.

`@microsoft/applicationinsights-web` was built for SPAs. It hooks into `XMLHttpRequest`, tracks page views via `history.pushState`, and lives entirely in the browser. Next.js 15's App Router is a fundamentally different animal:

* **Server Components** render on the server. There’s no browser. There’s no `window`. The SDK can't even initialize.
* **Server Actions** are RPC calls from client to server. They don’t show up as regular HTTP requests.
* **Streaming SSR** means the response isn’t a single payload — it’s chunks sent over time. The SDK has no concept of this.
* `instrumentation.ts` is the new hook. Not `_app.tsx`. Not a middleware. A dedicated file that runs once when the server starts.

The old approach of dropping a script tag or initializing in `_app.tsx` is dead. Full stop.

## The Stack That Actually Works

Here’s what we landed on after trying (and discarding) several approaches:

Press enter or click to view image in full size

![]()

```
npm install @vercel/otel @azure/monitor-opentelemetry-exporter \  
  @opentelemetry/api @opentelemetry/sdk-trace-base
```

Four packages. That’s it.

## The Part Nobody Tells You: `next.config.ts`

Before you write a single line of instrumentation code, you need to tell Next.js to stop trying to Webpack-bundle OpenTelemetry packages. They use native Node.js APIs (`diagnostics_channel`, `perf_hooks`, `async_hooks`) that Webpack can't handle.

I learned this the hard way. The error messages are *spectacular* in their unhelpfulness:

```
Module not found: Can't resolve 'diagnostics_channel'
```

Or my personal favorite:

```
TypeError: transformAlgorithm is not defined
```

The fix:

```
// next.config.ts  
const nextConfig: NextConfig = {  
  experimental: {  
    serverExternalPackages: [  
      "@azure/monitor-opentelemetry-exporter",  
      "@opentelemetry/sdk-node",  
      "@opentelemetry/sdk-trace-base",  
      "@opentelemetry/api",  
      "@vercel/otel",  
    ],  
  },  
  webpack: (config, { isServer }) => {  
    if (!isServer) {  
      config.externals = config.externals || [];  
      config.externals.push(  
        "@opentelemetry/api",  
        "@opentelemetry/sdk-trace-base",  
        "@azure/monitor-opentelemetry-exporter"  
      );  
    }  
    return config;  
  },  
};
```

`serverExternalPackages` tells Next.js: "Don't bundle these. Let Node.js require them at runtime." The webpack block ensures they're also excluded from client bundles — because importing OpenTelemetry in a React component is a path to suffering.

## The Instrumentation File

This is the core. `src/instrumentation.ts` exports a `register()` function that Next.js calls once when the server starts. Not on every request. Not in the browser. Once.

```
// src/instrumentation.ts  
import type { Context } from "@opentelemetry/api";  
import type { SpanProcessor, ReadableSpan } from "@opentelemetry/sdk-trace-base";  
import { registerOTel } from "@vercel/otel";  
import { PHASE_PRODUCTION_BUILD } from "next/constants";  
const SERVICE_NAME = "my-nextjs-app";
```

Nothing exciting yet. Let’s talk about the filter patterns.

## The Noise Problem

When I first got telemetry working, I was thrilled. Spans flowing into App Insights! Colors! Graphs! Then I looked at the bill.

A single page load in Next.js generates spans for:

* Every `.js` chunk loaded
* Every `.css` file
* Every font file (`.woff2`)
* Every image
* RSC payloads (`?_rsc=` or `?rsc=`)
* The favicon
* Next.js’s own telemetry ping to `telemetry.nextjs.org`

That’s 50–100 spans per page load. For a site with 100K daily users, you’re looking at millions of useless spans per day. Your App Insights instance becomes an expensive log of static asset deliveries.

```
const FILTER_PATTERNS = [  
  "/_next/static", "/_next/image", "/_next/data", "/__nextjs",  
  ".json", ".js", ".css", ".woff", ".woff2", ".svg", ".png",  
  ".jpg", ".jpeg", ".gif", ".webp", ".ico",  
  "?_rsc=", "?rsc=",  
  "/favicon.ico", "/robots.txt", "/sitemap",  
  "/api/health",          // K8s liveness probes — not interesting  
  "telemetry.nextjs.org", // Next.js phoning home  
];
```

## The FilteringSpanProcessor

The trick is to wrap the real `BatchSpanProcessor` with a custom processor that drops spans before they're exported. The OTEL SDK calls `onEnd()` for every span — we just don't forward the ones we don't care about.

```
function shouldFilterSpan(span: ReadableSpan): boolean {  
  const url = span.attributes["http.url"]  
    || span.attributes["url.full"]  
    || span.attributes["http.target"]  
    || span.name || "";  
  return FILTER_PATTERNS.some((p) => String(url).includes(p));  
}  
  
class FilteringSpanProcessor implements SpanProcessor {  
  constructor(private readonly _delegate: SpanProcessor) {}  
  forceFlush() { return this._delegate.forceFlush(); }  
  shutdown() { return this._delegate.shutdown(); }  
  onStart(span: ReadableSpan, parentContext: Context) {  
    // @ts-expect-error - type mismatch between Span and ReadableSpan  
    this._delegate.onStart?.(span, parentContext);  
  }  
  onEnd(span: ReadableSpan) {  
    if (shouldFilterSpan(span)) return;       // Static assets, RSC payloads - gone  
    if (span.kind === 1 && span.name.startsWith("metric.")) return; // Internal metric dupes  
    this._delegate.onEnd(span);               // Everything else goes to Azure  
  }  
}
```

That `span.kind === 1` check? That filters internal metric spans that are duplicates of dependency spans. Without it, every Redis operation shows up twice — once as a dependency span (useful) and once as an internal metric span (noise).

## Wiring It Up

```
export async function register() {  
  if (process.env.NEXT_RUNTIME !== "nodejs") return;  
  if (process.env.NEXT_PHASE === PHASE_PRODUCTION_BUILD) return;  
  
const connectionString = process.env.APPLICATIONINSIGHTS_CONNECTION_STRING;  
  if (!connectionString) {  
    console.log("[telemetry] No connection string - telemetry disabled");  
    return;  
  }  
  const { AzureMonitorTraceExporter } = await import(  
    "@azure/monitor-opentelemetry-exporter"  
  );  
  const { BatchSpanProcessor } = await import(  
    "@opentelemetry/sdk-trace-base"  
  );  
  const exporter = new AzureMonitorTraceExporter({ connectionString });  
  const processor = new BatchSpanProcessor(exporter, {  
    maxQueueSize: 2048,  
    maxExportBatchSize: 512,  
    scheduledDelayMillis: 5000,  
    exportTimeoutMillis: 30000,  
  });  
  registerOTel({  
    serviceName: SERVICE_NAME,  
    spanProcessors: [new FilteringSpanProcessor(processor)],  
  });  
}
```

Three guard clauses at the top. If you’re not on Node.js runtime (maybe edge), bail. If you’re in `next build`, bail — there's no server to talk to. If there's no connection string, bail — but log it so you're not debugging silence.

The dynamic imports are intentional. `AzureMonitorTraceExporter` pulls in a bunch of Azure SDK dependencies. We don't want those loaded during build or in edge runtime.

*Real talk:* The `BatchSpanProcessor` config numbers? I tuned those over a week of watching our pod memory usage. The defaults are fine for most apps. We run high traffic, so larger queues and batches made sense.

## Manual Instrumentation: The Stuff Auto-Instrumentation Can’t See

`@vercel/otel` auto-instruments `fetch()` calls. That's great — every API call, every CMS fetch shows up automatically. But it can't see:

* **Redis operations** (we use `ioredis` directly for our custom cache handler)
* **Business events** (user signed up, order placed)
* **Custom dependency types** (things that aren’t HTTP)

So we built a utility. The entire thing is marked `"server only"` — if anyone accidentally imports it in a client component, they get a clear error instead of a runtime crash.

```
// src/utils/telemetry/opentelemetry.ts  
"server only";  
import { trace, SpanStatusCode, SpanKind, context } from "@opentelemetry/api";  
const SERVICE_NAME = "my-nextjs-app";  
const TELEMETRY_ENABLED = !!process.env.APPLICATIONINSIGHTS_CONNECTION_STRING;  
function getTracer() {  
  return trace.getTracer(SERVICE_NAME);  
}
```

## The Safety Wrapper

Every telemetry call goes through this. If OTEL isn’t initialized, it’s a no-op. If it throws, we catch and move on. Telemetry must never crash the app.

```
function executeTelemetry(operation: () => void): void {  
  if (!TELEMETRY_ENABLED) return;  
  try {  
    const capturedContext = context.active();  
    context.with(capturedContext, () => {  
      try { operation(); } catch {}  
    });  
  } catch {}  
}
```

That `context.with(capturedContext, ...)` line is critical. Without it, your manual spans become orphans — they show up in App Insights but aren't linked to the request that triggered them. The trace waterfall looks broken. I spent a full day figuring out why my Redis spans weren't appearing under their parent HTTP request. This was it.

## Tracking Redis

```
export function trackDependency(  
  name: string, url: string, duration: number,  
  isSuccess: boolean, type?: string, properties?: Record<string, string>  
) {  
  executeTelemetry(() => {  
    const span = getTracer().startSpan(name, { kind: SpanKind.CLIENT });  
    span.setAttribute("dependency.type", type || "HTTP");  
    span.setAttribute("http.url", url);  
    if (properties) {  
      for (const [k, v] of Object.entries(properties)) span.setAttribute(k, v);  
    }  
    span.setStatus({  
      code: isSuccess ? SpanStatusCode.OK : SpanStatusCode.ERROR  
    });  
    span.end();  
  });  
}
```

Usage in our cache handler:

```
async function getFromCache(key: string) {  
  const start = Date.now();  
  try {  
    const result = await redis.get(key);  
    trackDependency("Redis-GET", redisHost, Date.now() - start, true, "Redis", {  
      operation: "GET", key,  
    });  
    return result;  
  } catch (error) {  
    trackDependency("Redis-GET", redisHost, Date.now() - start, false, "Redis", {  
      operation: "GET", key, errorMessage: error.message,  
    });  
    return null;  
  }  
}
```

## The Dependency Tracker Factory

For API calls where you want to track both success and failure with timing, this factory pattern saved us a ton of boilerplate:

```
export function createDependencyTracker(type: string, method: string, endpoint: string) {  
  const startTime = Date.now();  
  const spanName = `${type}-${method}-${endpoint}`;  
  
return {  
    success(url: string, props?: Record<string, string>) {  
      trackDependency(spanName, url, Date.now() - startTime, true, type, {  
        endpoint, method, ...props,  
      });  
    },  
    failure(url: string, error: Error | string, statusCode?: string) {  
      const duration = Date.now() - startTime;  
      const msg = error instanceof Error ? error.message : String(error);  
      trackDependency(spanName, url, duration, false, type, {  
        endpoint, method, statusCode: statusCode || "500", errorMessage: msg,  
      });  
      if (error instanceof Error) {  
        trackException(error, { endpoint, method, source: type.toLowerCase() });  
      }  
    },  
  };  
}
```

You create a tracker at the start of the call, and call `.success()` or `.failure()` at the end. The duration calculation is handled for you:

```
const tracker = createDependencyTracker("Strapi_CMS", "GET", "/api/funds");  
try {  
  const response = await fetch(url);  
  tracker.success(url, { statusCode: String(response.status) });  
} catch (error) {  
  tracker.failure(url, error, "500");  
}
```

## Enriching Auto-Instrumented Spans

Sometimes `@vercel/otel` creates the span for you (for `fetch()` calls), but you want to add context. That's what `enrichActiveSpan` does — it grabs the currently active span and adds attributes:

```
export function enrichActiveSpan(  
  properties?: Record<string, string | number | boolean>  
) {  
  executeTelemetry(() => {  
    const span = trace.getActiveSpan();  
    if (!span || !properties) return;  
    for (const [k, v] of Object.entries(properties)) span.setAttribute(k, v);  
  });  
}
```

We use this to add CMS endpoint names, HTTP status codes in multiple formats (because Azure and OTEL use different attribute names — don’t get me started), and caller information for audit trails.

## What You Actually See in App Insights

After deployment, your App Insights dashboard transforms. Here are the KQL queries I run daily:

## Slowest Routes

```
requests  
| where cloud_RoleName == "my-nextjs-app"  
| summarize p95=percentile(duration, 95), count() by name  
| top 10 by p95 desc
```

## Redis Health

```
dependencies  
| where cloud_RoleName == "my-nextjs-app"  
| where type == "Redis"  
| summarize total=count(), errors=countif(success == false) by bin(timestamp, 1h)  
| extend errorRate = errors * 100.0 / total
```

## Exception Breakdown

```
exceptions  
| where cloud_RoleName == "my-nextjs-app"  
| summarize count() by type, outerMessage  
| top 20 by count_
```

The Application Map is where it gets beautiful. Your Next.js app sits in the center, with arrows to Redis, Strapi CMS, backend APIs — each showing error rates and latency. When something goes wrong at 2 AM, you can see *where* in the chain the problem is, not just *that* there’s a problem.

## The Pitfalls I Hit So You Don’t Have To

**“It works locally but not in production”** — Check `APPLICATIONINSIGHTS_CONNECTION_STRING` in your pod/container env. The old `InstrumentationKey` alone doesn't work with OTEL.

**“Node.js 22 crashes on startup”** — Node 22 changed `ReadableStream` internals. If you see `transformAlgorithm` or `kState` errors, wrap your OTEL initialization in a try-catch and log a warning. It's a known compatibility issue.

**“instrumentation.ts runs during build and crashes”** — Guard with `PHASE_PRODUCTION_BUILD`. During `next build`, there's no running server.

**“My manual spans are orphans”** — You forgot `context.with(context.active(), ...)`. Without it, there's no parent-child link.

**“Client component crashes when importing telemetry”** — Add `"server only"` as the first line of your telemetry file. Not a comment. A string literal. Next.js will throw a build error if a client component tries to import it.

## What’s Next

This gets you clean, filtered telemetry flowing from your Next.js 15 app to Azure Application Insights. But here’s the thing — once you start looking at your production data, you’ll notice something disturbing.

Your error rate is 3.5%. Your exceptions dashboard shows 29,000 errors per day. You panic. You pull up the exception details and find… vulnerability scanner probes. Tenable. Nessus. SSTI payloads. Bots hammering your routes with `POST` requests where only `GET` is valid.

*95% of your “errors” aren’t errors at all. They’re noise.*

That’s what Part 2 is about.

*— Ketan Chavan*