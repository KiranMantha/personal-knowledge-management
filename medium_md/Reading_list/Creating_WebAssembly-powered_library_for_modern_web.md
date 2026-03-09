---
title: "Creating WebAssembly-powered library for modern web"
url: https://medium.com/p/846da334f8fc
---

# Creating WebAssembly-powered library for modern web

[Original](https://medium.com/p/846da334f8fc)

# Creating WebAssembly-powered library for modern web

[![Kagami](https://miro.medium.com/v2/resize:fill:64:64/0*FzWmi9NmStXCuyAB.)](/@KagamiH?source=post_page---byline--846da334f8fc---------------------------------------)

[Kagami](/@KagamiH?source=post_page---byline--846da334f8fc---------------------------------------)

11 min read

·

Mar 3, 2018

--

3

Listen

Share

More

*This article tells about my first practical experience with WebAssembly and few useful technics which I’ve obtained while creating* [*vmsg library*](https://github.com/Kagami/vmsg)*.*

I’ve got some free time recently so I decided to try the new WebAssembly standard and implement simple but useful library with it.

As stated in [WebAssembly docs](http://webassembly.org/docs/high-level-goals/) one of the main goals was to create format that can be parsed fast and has compact code representation. So I was really curious to leverage that main advantage. I’ve had experience with asm.js in past, making ports of pretty complicated C software such as FFmpeg and video/audio encoders. The build sizes were terrible — about 15 megabytes of minified JavaScript for ffmpeg CLI with few basic filters and encoders. Given that parsing of code is computationally expensive operation, especially on mobiles, it didn’t look so practical, more like targeted for proof of concepts little demos: [webm.js](https://kagami.github.io/webm.js/), [deviceframe.es](https://paulkinlan.github.io/deviceframe.es/).

On the other hand, WebAssembly binary can be parsed and compiled [as fast as it comes over the network](https://twitter.com/wycats/status/942908325775077376) making it a perfect build target for libraries written in C which you need to use inside a web page.

The idea of library came pretty quickly: I’m spending quite a lot of time on web forums, discussing various things via text messages and images. Recently with the raise of HTML5 video and WebM/VPx formats, it’s became quite common to attach small videos to the posts, increasing the possibilities of self-expression even more. What about voice? What if you can literally tell your message and send it as part of the post? Sounds great, let’s try it!

### Deciding on high-level architecture

So first we need to grab audio samples from microphone, then encode it, then return file to the library user. Looks pretty simple.

In 2018 [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API) is widely supported, no real headaches here. [getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) with conjuction of [ScriptProcessorNode](https://developer.mozilla.org/en-US/docs/Web/API/ScriptProcessorNode) are capable of the first step, WebAssembly module would be responsible for the second. Because `onaudioprocess` callback of `ScriptProcessor` node is being executed in the main thread and also to keep interface of web page responsive, WebAssembly module will be instantiated in the Web Worker, communicating with the main thread via messages.

> Side note: `ScriptProcessNode` has been deprecated and is soon to be replaced by [Audio Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API#Audio_processing_in_JavaScript) but it’s only implemented in Chrome 64+ behind a flag for the moment and for compatibility we have to use old API in near future anyway. Moreover, since we process samples in a worker, don’t output them to speakers and can use large buffer, Worklet isn’t required in our particular case. `ScriptProcessNode` should work just fine, all it needs to do is send samples to Web Worker which is very fast and lightweight operation.

We also going to create simple interface which would ask for permission to use mic and display recording form with start/stop/close buttons. Below you can see schematical overview of components of the library:

Press enter or click to view image in full size

![]()

### Choosing the format

Now we need to decide which audio format we will use to encode received samples to. Prerequisites: it should work in all browsers that support WebAssembly, it should give sane compression, it should be widespread across all platforms.

My initial desire was to grab Opus because it’s the best that you can use for speech compression. Unfortunately it’s not supported by `<audio>` element in Safari and Edge. Of course there’re various workarounds for this. For example in Edge you can manually fetch Opus file and play it via [MediaSource API](https://developer.mozilla.org/en-US/docs/Web/API/MediaSource). It’s also seems to be possible to [install Web Media Extension](https://wpdev.uservoice.com/forums/257854/suggestions/6513488) package for the full support. In Safari you can use Opus decoders ported to JavaScript such as [ogv.js](https://github.com/brion/ogv.js).

Even though it’s possible it’s too impractical for real use in my opinion. It’s ok to say: “If you want to support for voice messages add this library to your project”. But now you dictate which player to use to listen for resulting audios or require some non-trivial code to handle playback. I don’t like it so I had to abandon Opus. Maybe in few years from now the choice would be much easier.

> Side note: Chrome and Firefox support [MediaStream Recording API](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Recording_API) and can encode `MediaStream` data with Opus codec right out of the box. Not in Safari and Edge though and I really want to make my library work in all 4 of them so no luck here again.

Next one, there is WAV/PCM format available in all browsers. Creating WAV file from raw samples is a dead-simple process, there is [library](https://github.com/mattdiamond/Recorderjs) already for that. It has one *little* drawback though: there is no compression *at all*. So whether you sing some beatiful song in your mic or keep silent, 30 seconds of record (48KHz/mono) will always weight exactly 2.7 megabytes. This is way too wasteful.

What about MP3? It’s supported everywhere, has decent compression and great [LAME encoder](http://lame.sourceforge.net). Historially FOSS projects stepped aside from using it because of software patents but all of them [have expired in last year](https://en.wikipedia.org/wiki/LAME#Patents_and_legal_issues). So seems like we have a winner.

There are also AAC and Vorbis but neither of them fit. Former [forbids distribution of codec implementation in binary form](https://en.wikipedia.org/wiki/Advanced_Audio_Coding#Licensing_and_patents) which our WebAssembly module will effectively be. (Also it’s questionable whether free implementations as good as proprietary.) Latter doesn’t suitable for the speech compression.

### Compiling

So we need to grab LAME encoder, compile to WebAssembly module and make possible to use it from JavaScript.

There are tons of asm.js ports of LAME and maybe even WASM ports but I decided to make a new one from scratch in order to focus on build size optimizations.

At first I [mirrored SVN repo](https://github.com/Kagami/lame-svn) with git-svn because the [previous semi-official mirror](https://github.com/rbrito/deprecated-lame-mirror) was deprecated for some reason and don’t contain the latest 3.100 release, which might have some helpful bugfixes.

For compiling we use de-facto standard [Emscripten toolchain](http://webassembly.org/getting-started/developers-guide/), nothing new here. It’s been actively developed for many years and designed to port C/C++ libraries to the web, exactly what we need. I won’t go into details, you can read more about Emscripten at [official site](https://kripken.github.io/emscripten-site/).

Emscripten’s asm.js compiler is powered by LLVM backend called fastcomp. For WebAssembly you have two options: compile to asm.js first and translate to WASM with [Binaryen](https://github.com/WebAssembly/binaryen). Or use LLVM’s in-tree WebAssembly backend which is capable of producing WebAssembly binaries by itself (almost, you still need to use Binaryen for the final step). I chose the second because it seems to be the preferred one in near future. Also Emscripten’s got support for [standard LLVM linker](https://github.com/kripken/emscripten/pull/6056) recently which is again going to be preferred soon.

> Side note: I’m not going to describe the process of compiling LLVM with WASM backend. It’s generally recommended to use the latest SVN version. You can check out [this gist](https://gist.github.com/yurydelendik/4eeff8248aeb14ce763e) for the starting point. It’s also possible to compile WASM backend with emsdk by providing `--enable-wasm` flag but it uses pretty old LLVM (the base for fastcomp patches) so the resulting module might be bigger/slower than with SVN LLVM. It also doesn’t build LLD.

Let’s create stub of our library. I will use Linux shell commands, YMMV.

```
$ cd ~  
$ git init vmsg && cd vmsg  
$ npm init -y
```

Now we need sources of LAME encoder, git submodules are really handy for that:

```
$ git submodule add https://github.com/Kagami/lame-svn.git  
$ cd lame-svn && git checkout RELEASE__3_100 && cd ..
```

So far so good. Let’s compile `libmp3lame.so` (shared LAME library) so that we can later call its functions from WebAssembly module. I use GNU Makefile even though modern builders like webpack and parcel are getting support for WASM, because it’s not mature yet and I want to experiment with compiler flags and other optimizations. And builders will only stand in the way here.

Create `Makefile` with the following text (make sure to use tabs for indentation):

```
export EMCC_WASM_BACKEND = 1  
export EMCC_EXPERIMENTAL_USE_LLD = 1  
  
lame-svn/lame/dist/lib/libmp3lame.so:  
	cd lame-svn/lame && \  
	git reset --hard && \  
	patch -p2 < ../../lame-svn.patch && \  
	emconfigure ./configure \  
		CFLAGS="-DNDEBUG -Oz" \  
		--prefix="$$(pwd)/dist" \  
		--host=x86-none-linux \  
		--disable-static \  
		\  
		--disable-gtktest \  
		--disable-analyzer-hooks \  
		--disable-decoder \  
		--disable-frontend \  
		&& \  
	emmake make -j8 && \  
	emmake make install
```

I told Emscripten to use WASM backend and LLD, enabled advanced shrinking size optimizations, disabled asserts and disabled some extra stuff in LAME we don’t need. The [patch](https://github.com/Kagami/vmsg/blob/v0.2.0/lame-svn.patch) fixes strtol check in configure script and disables default LAME’s reporters to shrink the build size (otherwise Emscripten will include implementation of `printf` function and other stuff).

```
$ source /path/to/emsdk/emsdk_env.sh  
$ make
```

This activates Emscripten environment and creates LAME library at `lame-svn/lame/dist/lib/` directory.

Now we need to use LAME library functions in WebAssembly module and export MP3 creation routines so they can be called from JavaScript. I won’t go much into details here, you can check out the resulting [vmsg.c](https://github.com/Kagami/vmsg/blob/v0.2.0/vmsg.c). It has 4 methods: *init*, *encode*, *flush* and *free* which are self-descriptive and call one or few corresponding LAME functions inside. To communicate back and forth with JavaScript simple `vmsg` structure is being used which stores the current state of encoding. It’s also possible to encode multiple files in parallel because we don’t have global variables.

Let’s finally compile our WebAssembly module. Add this to `Makefile`:

```
vmsg.wasm: lame-svn/lame/dist/lib/libmp3lame.so vmsg.c  
	emcc $^ \  
		-DNDEBUG -Oz --llvm-lto 3 \  
		-Ilame-svn/lame/dist/include \  
		-s WASM=1 \  
		-s "EXPORTED_FUNCTIONS=['_vmsg_init','_vmsg_encode','_vmsg_flush','_vmsg_free']" \  
		-o _vmsg.js  
	cp _vmsg.wasm $@
```

Nothing really puzzled here, we ask Emscripten to compile our C wrapper, combine it with LAME shared library and export functions we would need on JavaScript side.

Type `make vmsg.wasm` and that’s it. We’ve ported fully-functional MP3 encoder to web which weights only about 70kb gzipped:

```
$ wc -c < vmsg.wasm  
152799  
$ gzip -6 -c vmsg.wasm | wc -c  
74152
```

Note that 70kb of gzipped WebAssembly is not even similar to 70kb of gzipped JavaScript in terms of parsing complexity. It’s like a small image: WASM module will be compiled and ready to use roughly just after it has been downloaded. It might be possible to shrink size of the module even more but for now I’m satisfied with the numbers.

### Runtime

[JavaScript API](https://developer.mozilla.org/en-US/docs/WebAssembly/Loading_and_running) for loading and calling WebAssembly module is pretty simple. The tricky part here is to provide functions that module needs to correctly operate on a web platform. WebAssembly spec doesn’t define any standard library like in C which is in charge of memory allocations, math operations, input/output API and so on. And LAME won’t work without some of them. Emscripten uses patched lightweight [musl](https://en.wikipedia.org/wiki/Musl) C standard library on WASM side (so the libraries being ported don’t need to be rewritten) and generates wrapper module in JS which would work in tandem with musl and make calls to e.g. in-browser `Date` object so the date/time functions of musl can work properly. Unfortunately it comes with a cost: even minified by Closure library it would weight about 10kb, so I was curious if I can do a better job than Emscripten in my particular case.

Let’s first look what module actually needs with `wasm-dis` from Binaryen toolchain:

```
$ wasm-dis vmsg.wasm | grep '(import'  
 (import "env" "memory" (memory $0 3))  
 (import "env" "pow" (func $import$1 (param f64 f64) (result f64)))  
 (import "env" "exit" (func $import$2 (param i32)))  
 (import "env" "powf" (func $import$3 (param f32 f32) (result f32)))  
 (import "env" "exp" (func $import$4 (param f64) (result f64)))  
 (import "env" "sqrtf" (func $import$5 (param f32) (result f32)))  
 (import "env" "cos" (func $import$6 (param f64) (result f64)))  
 (import "env" "log" (func $import$7 (param f64) (result f64)))  
 (import "env" "sin" (func $import$8 (param f64) (result f64)))  
 (import "env" "sbrk" (func $import$9 (param i32) (result i32)))
```

Only 10 functions and most of them can be mapped directly to `Math` object! There is also `exit` which is called when module decided to, well, exit, `memory` which is virtual memory and created with `new WebAssembly.Memory` and `sbrk` called by musl when it needs to allocate more memory. [Here](https://github.com/Kagami/vmsg/blob/efcbb9ffdd718fe0aebd13b19d0018b71027bfcc/vmsg.js#L24-L55) you can see my implementation of all that functions which takes only 30 lines and works perfectly fine.

### Polyfill

It’s a great thing that WebAssembly is supported by all 4 major browsers (Chrome/Firefox/Safari/Edge) but not all users on the web have access to latest versions of browsers. So it’s reasonable to make your application support as many versions as you can if it doesn’t hurt readability/performance/maintenance/etc much. For example I intentionally use XHR on browsers without [WebAssembly.instantiateStreaming](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly/instantiateStreaming) because it makes code only 5 lines longer and allows to support browsers without Fetch API e.g. Edge 12–14.

Right now the recommended way of “polyfilling” WebAssembly is to make separate asm.js build of the same code. It works pretty well with Emscripten’s runtime because it abstracts out differences between these two techs and provides single `Module` interface to interact with compiled code. Because we use our own runtime and because it feels more natural to use WebAssembly API if available and emulate it if not, I decided to put foot at “true polyfill” path.

Quick search for “WebAssembly polyfill” returned several projects, most promising of them was [by Ryan Kelly](https://github.com/rfk/wasm-polyfill). It works by emulating WebAssembly browser APIs such as `WebAssembly.Memory` and `WebAssembly.Table`, parsing binary module and generating asm.js-alike code on the fly. Exactly what I wanted! Unfortunately it was no longer maintained so I had to fork it, slightly refactor, fix obvious issues and tests and publish to NPM. The most horrible bug was in code generation of `i64.store` instruction but eventually I kinda fixed it. [Here](https://github.com/Kagami/wasm-polyfill.js) is my fork, I think it might be useful for other projects too.

I’ve also found [polyfill in Binaryen repo](https://github.com/WebAssembly/binaryen/blob/master/bin/wasm.js) but it was too huge (2.5mb vs 95kb in case of wasm-polyfill) and not complete: it doesn’t emulate the WebAssembly browser API. Finally the [official polyfill prototype](https://github.com/lukewagner/polyfill-prototype-1) looks abandoned so wasm-polyfill is probably the best option that we have now. It’s not ideal though: generated code is not as effecient as it could be, there’re lot of extra bound checkings created to be fully semantically correct. See last section for the possible improvements in that area.

Usage of polyfill is straight-forward: include minified `wasm-polyfill.js` build with `<script>` tag or call `importScripts` in case of Worker. A piece of cake.

### Putting everything together

We already have WebAssembly module, can load it from JavaScript and call its functions, what else? We need to spawn it in Worker, define communication protocol and feed it some real data from mic.

Also we need to build some UI so users won’t have to reimplement it all the time. At first I leant towards to React because it’s so extremely popular and powerful library for creating composable UI components. It comes with a cost though: not everyone in the world uses React e.g. Angular and Vue.js are widespread too, and by sticking to React-only you leave lot of potential users of your library outside. Given that I planned to make interface pretty simple, React won’t help much here, so better to utilize standard DOM API. Moreover it’s always possible to include such library into site powered by any framework but not the other way around.

I won’t annotate all code I’ve got, most of it is self-descriptive. Check out resulting [vmsg.js](https://github.com/Kagami/vmsg/blob/v0.2.0/vmsg.js). Interaction with Web Audio and Web Workers is already documented quite good on the web. The only interesting part is that I don’t use separate file for worker source but create a [Blob URL](https://github.com/Kagami/vmsg/blob/v0.2.0/vmsg.js#L340-L344) instead. This makes library a bit more pleasant to use: you don’t have to care about extra file.

The full demo is available [here](https://kagami.github.io/vmsg/).

### Future ideas

What now? Library works pretty well, I already use it at my forum for voice messages support. But there are few more interesting areas worth trying:

1. Emscripten is going to get support for [emmalloc](https://github.com/kripken/emscripten/pull/6249) soon which should decrease build size without any efforts, just by enabling it via option. It comes with a cost of making malloc operations less effecient but for LAME it shouldn’t be a problem.
2. It might be interesting to implement some audio filters such as noise supression and pitch shifting as part of WebAssembly module. Because it runs in separate Worker thread, we can use advanced algorithms without the fear of introducing latency and freezing the main thread.
3. It’s worth to compare performance of wasm-polyfill with and without memory bound checkings. Because LAME shouldn’t generally trap it’s rather safe to just disable all checks for better performance. Even in case of bug in C code it won’t affect JavaScript side because of sandboxing.
4. Pretty complex but doable task is to make code translated by wasm-polyfill asm.js-compatible. Right now there’re a lot of spec violations so it can’t be AOT compiled. It runs as normal JavaScript therefore not as fast and performant (though JIT should optimize such code pretty hard anyway).