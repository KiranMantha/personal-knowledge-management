---
title: "I Made Zod 64x Faster by Compiling Schemas at Build Time"
url: https://medium.com/p/be5de452b5e9
---

# I Made Zod 64x Faster by Compiling Schemas at Build Time

[Original](https://medium.com/p/be5de452b5e9)

# I Made Zod 64x Faster by Compiling Schemas at Build Time

[![Tetsuya Wakita](https://miro.medium.com/v2/resize:fill:64:64/1*4bp21Hww3XjblYAZNEDGGg.jpeg)](/@wakita181009?source=post_page---byline--be5de452b5e9---------------------------------------)

[Tetsuya Wakita](/@wakita181009?source=post_page---byline--be5de452b5e9---------------------------------------)

6 min read

·

Mar 4, 2026

--

2

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dbe5de452b5e9&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40wakita181009%2Fi-made-zod-64x-faster-by-compiling-schemas-at-build-time-be5de452b5e9&source=---header_actions--be5de452b5e9---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

Zod v4 is fast. But what if you could skip schema traversal entirely? I built a compiler that turns your Zod schemas into plain JavaScript validation functions at build time — and it’s 2–64x faster.

## The Problem: Runtime Schema Traversal Is Inherently Slow

Zod is everywhere. With over 100 million weekly npm downloads, it’s the de facto standard for runtime validation in TypeScript. The API is beautiful — you define a schema, and you get both runtime validation and static types for free.

But that elegance has a cost.

Every time you call `.parse()`, Zod walks the entire schema tree at runtime. It checks each node type, applies constraints, collects errors, and constructs the result. For a simple `z.string()`, the overhead is negligible. But for a nested object with arrays, unions, and dozens of fields? That tree walk adds up fast.

```
// Every .parse() call traverses this entire tree — every time  
const UserSchema = z.object({  
  id: z.string().uuid(),  
  name: z.string().min(1).max(100),  
  email: z.string().email(),  
  role: z.enum(["admin", "user", "viewer"]),  
  preferences: z.object({  
    theme: z.enum(["light", "dark"]),  
    notifications: z.boolean(),  
    language: z.string().length(2),  
  }),  
  tags: z.array(z.string()).max(20),  
});  
  
// This traverses ~15 schema nodes on every single call  
UserSchema.parse(data);
```

This matters in real production scenarios:

* **API servers** validating every incoming request body
* **Edge functions** where cold-start budgets are measured in milliseconds
* **Form validation** running on every keystroke on mobile devices

The schema never changes. But Zod re-discovers its structure on every single parse call.

## The Insight: Schemas Are Static — Validation Can Be Compiled

Here’s the key observation: most Zod schemas are defined once at module scope and never change at runtime. The tree walk produces the same sequence of operations every time. It’s pure overhead.

This is exactly the problem compilers solve — move repeated work from runtime to build time.

What if instead of walking a schema tree at runtime, you could generate a plain function that does the exact same validation — but with zero traversal overhead?

```
// What Zod does at runtime (simplified):  
function parse(schema, data) {  
  switch (schema.type) {  
    case "object": return parseObject(schema, data);  
    case "string": return parseString(schema, data);  
    case "array":  return parseArray(schema, data);  
    // ... recursive traversal continues  
  }  
}  
  
// What AOT compilation produces:  
function validateUser(data) {  
  if (typeof data !== "object" || data === null) return error("Expected object");  
  if (typeof data.id !== "string") return error("Expected string");  
  if (!UUID_REGEX.test(data.id)) return error("Invalid uuid");  
  if (typeof data.name !== "string") return error("Expected string");  
  if (data.name.length < 1) return error("String must contain at least 1 character(s)");  
  // ... flat, linear, no traversal  
}
```

The second function does the same thing, but there’s no schema tree to walk. No type switches. No recursive calls. Just straight-line validation code.

## Introducing zod-aot

That’s what `zod-aot` does. It reads your Zod schemas at build time, compiles them into optimized validation functions, and replaces the runtime parsing with generated code.

## Installation

```
npm install zod-aot zod@^4
```

## Usage — wrap with `compile()`

```
import { z } from "zod";  
import { compile } from "zod-aot";  
  
const UserSchema = compile(  
  z.object({  
    id: z.string().uuid(),  
    name: z.string().min(1).max(100),  
    email: z.string().email(),  
    role: z.enum(["admin", "user", "viewer"]),  
  })  
);  
  
// Same API — .parse(), .safeParse(), .is()  
const user = UserSchema.parse(data);
```

In development, `compile()` passes through to Zod as-is. In production builds, the bundler plugin replaces it with the generated validation function. Zero code changes to your existing schemas.

## Build integration

**Vite** (4 lines):

```
// vite.config.ts  
import { zodAot } from "zod-aot/vite";  
  
export default defineConfig({  
  plugins: [zodAot()],  
});
```

**CLI** for non-bundler workflows:

```
npx zod-aot generate src/ -o dist/
```

The compiled validators expose the same interface: `.parse()` throws on invalid input, `.safeParse()` returns a result object, and `.is()` acts as a type guard.

## Transform and Refine: Partial Compilation

Here’s where it gets interesting. Not everything in a Zod schema can be compiled ahead of time.

Zod’s `.transform()`, `.refine()`, `.superRefine()`, and `z.custom()` accept arbitrary JavaScript functions. These are opaque at build time — there's no way to statically analyze what `(val) => val.toUpperCase()` does without executing it.

So `zod-aot` doesn't try to compile them. Instead, it uses **partial compilation**.

```
const ProfileSchema = compile(  
  z.object({  
    name: z.string().min(1),                          // ✅ AOT compiled  
    email: z.string().email(),                         // ✅ AOT compiled  
    age: z.number().int().min(0).max(150),             // ✅ AOT compiled  
    bio: z.string().transform((s) => s.trim()),        // ⚠️ Falls back to Zod  
    score: z.number().refine((n) => isPrime(n)),       // ⚠️ Falls back to Zod  
  })  
);
```

In this schema, 3 out of 5 fields get full AOT compilation. The remaining 2 delegate to Zod at runtime — only for those specific fields. The compiler decides this automatically at extraction time. No annotations, no configuration, no manual intervention.

> ***This is the key design decision****: compile what you can, fall back gracefully for the rest. A schema that’s 80% compilable still gets 80% of the performance benefit.*

This means you never have to worry about whether your schema is “compatible” with zod-aot. Every Zod v4 schema works. The question is only how much of it gets compiled.

## Benchmark Results

Theory is nice. Let’s see actual numbers.

I benchmarked `zod-aot` compiled validators against Zod v4's native `.parse()` across a range of schema complexities. Each benchmark runs 100,000 iterations with warmup, using `performance.now()` for timing.

```
Schema                              |   Zod v4   | zod-aot    | Speedup  
------------------------------------|------------|------------|---------  
Simple string (z.string().email())  | 1.2M ops/s | 2.1M ops/s |  ~1.8x  
Medium object (valid input)         | 480K ops/s | 2.4M ops/s |  ~5x  
Medium object (invalid input)       | 210K ops/s | 4.8M ops/s |  ~23x  
Large nested object (100 items)     | 12K  ops/s | 780K ops/s |  ~64x  
Discriminated union (5 variants)    | 320K ops/s | 3.2M ops/s |  ~10x
```

The pattern is clear: **the larger and more complex the schema, the greater the AOT benefit**.

For a simple string validation, the overhead of Zod’s runtime traversal is minimal — you’re only walking one or two nodes. The speedup is modest.

But for a large nested object with 100 array items, each containing multiple validated fields, Zod has to traverse hundreds of schema nodes on every parse call. The AOT-compiled version does the same validation with flat, inlined code — no tree to walk. That’s where the 64x gap comes from.

The invalid input case is particularly interesting. The compiled validator hits the first failing check and returns immediately. Zod’s runtime has more overhead even for early exits because of the error collection and traversal machinery.

> ***Key takeaway****: If your hot-path schemas are simple primitives, Zod v4 is already fast enough. If you’re validating complex nested objects at high throughput, AOT compilation delivers an order-of-magnitude improvement.*

## Comparison and Trade-offs

## How zod-aot compares to alternatives

**vs Typia** (~76M ops/s): Typia is faster because it compiles directly from TypeScript types using a compiler plugin. But it requires you to define validation as TypeScript types — not Zod schemas. If your codebase already uses Zod, migrating to Typia means rewriting every schema.

**vs AJV standalone**: AJV compiles JSON Schema into validation functions — conceptually the same approach as zod-aot. But AJV operates in the JSON Schema ecosystem. If you’re using Zod, you’d need to convert schemas to JSON Schema first, losing Zod-specific features.

**vs Zod v4 native**: zod-aot is complementary, not competitive. It builds on Zod v4 and uses its internals. You keep writing Zod schemas — zod-aot just makes them faster in production.

**zod-aot’s niche**: zero migration cost for existing Zod users. You keep your schemas, your types, your ecosystem integrations with tRPC/React Hook Form/Next.js. You just add `compile()` and a build plugin.

## Honest trade-offs

Nothing is free. Here’s what you should know:

* **Build-time extraction**: zod-aot runs your schema code once at build time to extract the schema structure. If your schemas have side effects at definition time, this could cause issues.
* `transform`**/**`refine`**-heavy schemas** get minimal benefit. If most of your validation logic lives in custom functions, AOT compilation can't help much.
* **Bundle size**: generated validators are standalone JavaScript — no Zod dependency at runtime, but the generated code itself adds to your bundle. For most schemas this is smaller than Zod itself.
* **Zod v4 only**: zod-aot depends on Zod v4’s internal schema representation (`_zod.def`). It does not support Zod v3.

## Try It Out

`zod-aot` is open source under the MIT license.

* **GitHub**: <https://github.com/wakita181009/zod-aot>
* **npm**: [zod-aot](https://www.npmjs.com/package/zod-aot)

What’s next:

* Broader schema type coverage (recursive types, branded types)
* Incremental build caching for large codebases
* Source map support for debugging compiled validators

If you’re using Zod in a performance-sensitive context, give it a try. Star the repo if you find it useful, and file issues for anything that doesn’t work. PRs are always welcome.