---
title: "Writing  TypeScript custom AST Transformer (Part 1)"
url: https://medium.com/p/7585d6916819
---

# Writing  TypeScript custom AST Transformer (Part 1)

[Original](https://medium.com/p/7585d6916819)

Press enter or click to view image in full size

![]()

# Writing TypeScript custom AST Transformer (Part 1)

[![Long Ho](https://miro.medium.com/v2/resize:fill:64:64/0*H9xeXeYo5nsw6kCi.jpg)](https://medium.com/@longho?source=post_page---byline--7585d6916819---------------------------------------)

[Long Ho](https://medium.com/@longho?source=post_page---byline--7585d6916819---------------------------------------)

3 min read

·

Mar 24, 2019

--

Listen

Share

More

## Background

Babel’s ecosystem relies heavily on plugins which allows you to do a lot of things ranging from interop with other ecosystems (e.g CSS) to optimization (e.g hoisting/inlining). The TypeScript compiler, on the other hand, is designed to be a battery-included monolith that works great out of the box and thus, requires fewer plugins to build.

However, that partially changed back in TypeScript 2.3-ish when TS Compiler started supporting custom AST Transformer. This opens up a lot of possibilities to bring similar capabilities from babel to TS without having to chain these tools and also take full advantage of TS typechecker.

## Why did I care?

Primarily if you’re interested in learning how toolchain works under the hood and general AST transformation, this could be interesting to you.

The real-world interesting aspect to me has been figuring out the boundary between what to write in source & what compiler can take care of for you. This changes how I write code, specifically in manually optimizing certain code paths and enforcing convention. Understanding how this works and what can be done allows me to move some of those from manual code review to compile-time transformation.

Furthermore, this opens up opportunities to things like compiler macros and interop with other ecosystems while enforcing explicit dependencies in your source code.

This will be a multi-part series and part 1 specifically talks about the boilerplate.

## The boilerplate

Unfortunately right now `tsconfig.json` does not allow specifying custom AST transformers. There’re a couple of alternatives you can utilize, each with its own caveat:

1. <https://github.com/TypeStrong/ts-loader> for webpack ecosystem
2. <https://github.com/TypeStrong/ts-node> for REPL
3. <https://github.com/cevek/ttypescript> for `tsc` replacement
4. Write your own compiler wrapper

I’ll be talking about option 4 specifically in this post primarily because it’s more interesting and also has 0 outside dependencies other than `typescript` itself.

## Simple compiler wrapper

TypeScript wiki already has a decent set of docs surrounding [how to use the compiler API](https://github.com/Microsoft/TypeScript/wiki/Using-the-Compiler-API) that I highly recommend. For most of my TS Transformer projects, my boilerplate looks something like this:

This wrapper can be broken down into 3 main pieces:

### Parsing `tsconfig.json`

```
ts.getParsedCommandLineOfConfigFile(configFilePath, undefined, host);
```

At a high level, TS Compiler takes in 2 main params: the list of files to compile & the `CompilerOptions` to compile them with. You can choose to manually specify the options like:

However, there’re a couple of advantages to using `getParsedCommandLineOfConfigFile`

1. Centralize config around `tsconfig.json` which means you don’t have to manually `glob` files to pass into the compiler.
2. This handles CLI overwrites.
3. There’re subtle differences in the final `CompilerOptions`generated from this function compared to manually specifying one.

### Create `Program` and `emit` results

This is the bulk of the work where TS `Program` is constructed, starts compilation & emit both `.js` and `.d.ts` to the specified output directory. This is also where you’d specify your custom AST transformer, for example:

TS itself comes with [a lot of ESNext -> ES5 transformers](https://github.com/Microsoft/TypeScript/tree/master/src/compiler/transformers) by default. The pipeline allows you to order your custom transformer in a specific way:

1. `before` means your transformers get run before TS ones, which means your transformer will get raw TS syntax instead of transpiled syntax (e.g `import` instead of `require` or `define` )
2. `after` means your transformers get run after TS ones, which gets transpiled syntax.
3. `afterDeclarations` means your transformers get run during `d.ts` generation phase, allowing you to transform output type declarations.

Most transformers I wrote are `before` transformers because that’s where most of the use cases have been. `after` & `afterDeclarations` are necessary if you’re potentially modifying types. For example:

1. <https://github.com/longlho/ts-transform-json> inlines JSON keys into output file, which requires modifying `d.ts` as well, otherwise the type declaration would still preserve the original `json` file `import` which makes it less useful.
2. <https://github.com/dropbox/ts-transform-import-path-rewrite> modifies `import` & `export` paths, thus needing to have `d.ts` matching the new rewritten path or else type checking will fail.

This is it for Part 1. I’ll start walking through the anatomy of a custom AST transformer & walk through some transformers I wrote in subsequent parts :)

[## Learn TypeScript - Best TypeScript Tutorials (2019) | gitconnected

### The top 18 TypeScript tutorials - learn TypeScript for free. Courses are submitted and voted on by developers, enabling…

gitconnected.com](https://gitconnected.com/learn/typescript?source=post_page-----7585d6916819---------------------------------------)