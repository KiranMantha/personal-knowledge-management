Original Issue Link: https://github.com/vercel/next.js/issues/47516

# Fixing Next.js + Cloudflare caching issue for `_next/data` with `x-middleware-prefetch`

When using **Next.js Pages Router with `getServerSideProps`** behind **Cloudflare CDN**, I ran into an issue where client-side navigations were repeatedly hitting the origin and, in some cases, rendering blank pages.

This was especially visible for routes backed by **AEM Sling Models** using a **catch-all slug page**.

---

## Problem

The initial HTML page load was working as expected, but the associated JSON prefetch requests were not behaving correctly.

Example request:

```text
/_next/data/<build-id>/index.json
```

Instead of returning the actual page props JSON, the prefetch request was returning:

```json
{}
```

with:

```text
status: 200
content-length: 2
```

This caused two major issues:

- **Cloudflare was not caching the correct payload**
- **client-side navigation broke because the browser cached an empty object**

---

## User-facing impact

This was more than just a caching issue.

Because the response status was still:

```text
200 OK
```

the browser treated the prefetch response as valid and cached it.

That means the browser stored:

```json
{}
```

for the `_next/data` request.

On subsequent client-side navigations, Next.js reused the cached response.

This resulted in:

- blank page rendering
- broken CSR navigation
- missing page props
- components failing due to undefined data
- page appearing empty until hard refresh

---

## Root cause

The issue was caused by the presence of the following request header:

```text
x-middleware-prefetch
```

When this header exists:

- Next.js treats the request as a **middleware prefetch**
- the request **does not always fully execute `getServerSideProps`**
- `_next/data` may return an empty object (`{}`)
- proper cache headers are not returned
- Cloudflare does not cache the response as expected

This results in:

- no browser cache reuse
- no CDN edge cache hit
- repeated AEM origin fetches
- broken client-side navigation

This behavior becomes more visible when using:

- middleware
- catch-all routes
- `getServerSideProps`
- AEM model fetching

---

## Fix

Inside middleware, explicitly remove the `x-middleware-prefetch` header.

### Middleware fix

```ts
export function middleware(req: NextRequest) {
  const requestHeaders = new Headers(req.headers);

  if (requestHeaders.get('x-middleware-prefetch')) {
    requestHeaders.delete('x-middleware-prefetch');
  }
  
  ....

  return NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * 1. /api/healthCheck (Exactly this API route)
     * 2. Next.js internals (_next)
     * 3. Any file ending in common image extensions
     * */
    '/((?!_next|.*\\.(?:png|jpg|jpeg|gif|svg|webp|ico|txt|xml)$).*)',
  ],
};
```

---

## Why this works

Removing this header forces Next.js to treat prefetch requests as **normal data requests**.

That means `_next/data` requests now correctly flow into:

```ts
getServerSideProps()
```

This allows the server to:

- return actual serialized page props
- return cache headers
- enable browser cache
- enable Cloudflare cache

Once cache headers are present:

- **browser cache works**
- **Cloudflare edge cache works**
- **client-side navigations reuse valid JSON**
- **blank page issue is resolved**

---

## Important cache headers added in `getServerSideProps`

On successful AEM model fetch:

```ts
export async function getServerSideProps(context: NextPageContext) {
  const { req, res, query } = context;
  ....

  res.setHeader(
    'Cache-Control',
    'public, s-maxage=300, stale-while-revalidate=60'
  );

  res.setHeader(
    'CDN-Cache-Control',
    'public, s-maxage=300, stale-while-revalidate=60'
  );

  ....
}
```

---

## Header purpose

### `Cache-Control`

Used by browser + shared caches:

```text
public, s-maxage=300, stale-while-revalidate=60
```

Meaning:

- cache for **5 minutes**
- serve stale for **60 seconds while refreshing**

---

### `CDN-Cache-Control`

Explicitly helps CDN layers like Cloudflare respect cache rules.

This is useful when CDN behavior differs from browser caching.

---

## Request flow before fix

```text
Link prefetch
   ↓
_next/data returns {}
   ↓
Browser caches {}
   ↓
User clicks link
   ↓
Next.js reuses cached {}
   ↓
Blank page / broken CSR navigation
```

---

## Request flow after fix

### First request

```text
Browser → Cloudflare → Next.js → getServerSideProps → AEM
```

Response cached at:

- browser
- Cloudflare

---

### Subsequent navigation

```text
Browser → Cloudflare cache hit
```

or even:

```text
Browser memory/disk cache hit
```

No AEM hit.

---

## Why this matters for AEM integration

Because the catch-all slug dynamically builds the AEM page path:

```ts
const pagePath = `${aemRoot}/${path}`
```

Every cache miss triggers:

```ts
fetchModel(...)
```

That directly impacts:

- AEM load
- TTFB
- origin costs
- page navigation speed

This fix significantly reduces all of that.

---

## How to verify browser cache + Cloudflare cache

Use the following steps to validate that `_next/data` prefetch requests are being cached correctly at both the **browser** and **Cloudflare CDN** levels.

---

### 1) Initial page load

Load the page normally for the first time.

Example:

```text
https://your-domain.com
```

At this stage, the browser makes the initial HTML request and the associated `_next/data` prefetch JSON calls.

Example request:

```text
/_next/data/<build-id>/index.json
```

This request will usually hit the origin on first load.

---

### 2) Verify browser disk cache

Open **DevTools → Network tab** and refresh again **without enabling “Disable cache”**.

Expected result:

- `_next/data` calls should be served from **Disk Cache**
- browser should not hit the network

Chrome DevTools should show:

```text
(from disk cache)
```

This confirms **browser-level caching is working**.

---

### 3) Verify Cloudflare MISS / EXPIRED

Enable:

```text
Disable cache
```

in the Network tab and refresh.

Expected result:

- browser cache is bypassed
- request goes to Cloudflare
- Cloudflare may fetch from origin if cache is cold

Check response header:

```text
cf-cache-status
```

Expected:

```text
MISS
```

or

```text
EXPIRED
```

This confirms the request is reaching CDN/origin correctly.

---

### 4) Verify Cloudflare HIT

With **Disable cache still enabled**, refresh again.

Expected:

```text
cf-cache-status: HIT
```

This confirms:

- browser cache is bypassed
- Cloudflare edge cache is serving the response
- origin is not being hit again

This is the strongest confirmation that CDN caching is working.

---

## Expected lifecycle

```text
1st load        → origin hit
2nd load        → browser disk cache
disable cache   → Cloudflare MISS
next refresh    → Cloudflare HIT
```

---

## Final takeaway

> Removing `x-middleware-prefetch` in middleware ensures `_next/data` requests execute `getServerSideProps`, return valid JSON instead of `{}`, and enables proper browser + Cloudflare caching.

This completely resolved both the **caching issue** and the **blank page CSR navigation issue** for AEM Sling Model pages served through a Next.js catch-all route.