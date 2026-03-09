---
title: "Porting Games to the Web with WebAssembly"
url: https://medium.com/p/70d598e1a3ec
---

# Porting Games to the Web with WebAssembly

[Original](https://medium.com/p/70d598e1a3ec)

# **Porting Games to the Web with WebAssembly**

## How to port an *Asteroids* game from C to WebAssembly 🎮

[![Robert Aboukhalil](https://miro.medium.com/v2/resize:fill:64:64/1*uQPULQh-yuw4DmTSpRxfbw.jpeg)](/?source=post_page---byline--70d598e1a3ec---------------------------------------)

[Robert Aboukhalil](/?source=post_page---byline--70d598e1a3ec---------------------------------------)

5 min read

·

Apr 9, 2019

--

2

Listen

Share

More

[WebAssembly](https://webassembly.org) is a new language for the web. Much like low-level assembly languages, however, very few people write WebAssembly by hand; instead, you can compile code written in other languages (e.g. C, C++ and Rust) to WebAssembly and run that code in the browser.

Why would you *ever* want to do that, you ask? **One reason is portability**: WebAssembly makes it easier to port existing [games](http://www.continuation-labs.com/projects/d3wasm/), [desktop applications](http://blogs.autodesk.com/autocad/autocad-web-app-google-io-2018/), and [command-line tools](http://www.jqkungfu.com/) to the web. **Another reason is the potential for speeding up web apps** by [replacing slow JavaScript calculations with compiled WebAssembly](https://www.smashingmagazine.com/2019/04/webassembly-speed-web-app/).

In this article, we’ll focus on **how to port an** [**open-source clone of the classic Asteroids game**](https://github.com/flightcrank/asteroids) **from C to WebAssembly.**

> For a preview of the final result, [**check out this live demo**](http://www.levelupwasm.com/apps/asteroids/index.html).

![]()

## **Let’s get started!**

To compile this game, we’ll use [Emscripten](https://emscripten.org), a tool that helps you compile C and C++ programs to WebAssembly. As we’ll see, developing in WebAssembly is not easy, but Emscripten provides many tools and features that make it much easier.

To install Emscripten, you can pull [this Docker image](https://hub.docker.com/r/robertaboukhalil/emsdk/tags) I put together that contains all the tools you’ll need for this article (you can also [install Emscripten from scratch](https://emscripten.org/docs/getting_started/downloads.html), but that may take a while):

```
# Fetch docker image containing Emscripten  
$ docker pull robertaboukhalil/emsdk:1.38.26# Create a container from that image and   
# mount ~/wasm to /src inside the container  
$ mkdir ~/wasm  
$ cd ~/wasm  
$ docker run -dt -name wasm \  
    --volume "$(pwd)":/src  
    robertaboukhalil/emsdk:1.38.26# Enter the container  
$ docker exec -it wasm bash
```

Inside the container, let’s clone the repo. We’ll check out a specific commit ID, in case the code changes after this article is published:

```
$ git clone "https://github.com/flightcrank/asteroids.git"  
$ cd asteroids  
$ git checkout 529cad3
```

**Interestingly, if you try to compile this code as is to WebAssembly, your browser tab will crash because of the infinite loops in the code!**

## **A series of unfortunate loops**

**Games often contain infinite loops that wait around for user input**, mouse movement or an animation to finish. For example, you’ll see the following infinite loop if you dive into the Asteroids code (`asteroids/main.c`) — here’s the equivalent pseudocode:

```
int main() {  
  <initialization>  // render loop  
  while(quit == 0) {  
    <main loop contents>  
  }  <cleanup and exit game>  
}
```

**While using infinite loops works in a desktop game, this won’t fly in the browser**, where infinite loops will crash your tab ([details here](https://emscripten.org/docs/porting/emscripten-runtime-environment.html#browser-main-loop)).

What this means is that we’ll have to restructure the `while()` loop above into something the browser can handle, i.e. running the contents of that loop periodically instead of continuously. In general, we can use Emscripten’s `emscripten_set_main_loop()` function in our C++ code to define a function to call periodically:

```
emscripten_set_main_loop(  
  mainloop,  // function to call  
  0,         // frame rate (0 = browser figures it out)  
  1          // simulate infinite loop  
);
```

So let’s replace this infinite loop; here’s pseudocode to illustrate what we need to change in the code:

```
// Put this at the top to import emscripten_set_main_loop()  
#include "emscripten.h"...// Move the infinite loop to a separate function  
void mainloop() {  
  <main loop contents>  // Stop simulating the infinite loop  
  if(<user pressed Escape key>) {  
    emscripten_cancel_main_loop();  
    <cleanup and exit game>  
  }  
}// In main(), simulate infinite loop  
int main() {  
  <initialization>  
  emscripten_set_main_loop(mainloop, 0, 1);  
}
```

As you can see, there’s a fair bit of moving code around to adapt it to the browser. The final `main.c` is [available here](https://github.com/robertaboukhalil/wasm-asteroids/blob/master/asteroids/main.c) (see [diff here](https://github.com/flightcrank/asteroids/compare/master...robertaboukhalil:master?diff=split#diff-17d64fa73f9cca12acec5190a5b62db8))**.**

Now that our game has been un-infinite-loop-ified — a valid scrabble word, I’m sure — we’re ready to compile our game!

## Compiling the game

Let’s see how we would usually compile this game to binary, and then which modifications we need to compile it to WebAssembly. According to the `README` file, we can compile the Asteroids game as follows:

```
# To compile to binary (don't type this yet):  
$ gcc \  
    -o app asteroids/*.c \  
    -Wall -g -lm \  
    `sdl2-config --cflags --libs`
```

Instead, to compile it to WebAssembly, we’ll use Emscripten’s `gcc` wrapper: `emcc`.

Like many games written in C/C++, Asteroids uses the SDL library, which is short for [Simple DirectMedia Layer](https://wiki.libsdl.org/Introduction). In a nutshell, it’s a library with useful utility functions to handle user input via mouse/keyboard/joystick, play audio files, and more. Because SDL is so popular, it has already been [ported to WebAssembly](https://github.com/emscripten-ports/SDL2), and Emscripten provides special flags to support it out of the box; here’s what the `emcc` invocation looks like (differences in bold):

```
# To compile to WebAssembly:  
$ emcc \  
    -o app.html asteroids/*.c \  
    -Wall -g -lm \  
    -s USE_SDL=2
```

Let’s unwrap this:

1. We modified the output to be `app.html` so that Emscripten generates HTML and JavaScript files that will conveniently initialize our WebAssembly module (`app.wasm`) and load the game in an HTML canvas.
2. Instead of calling `sdl2-config`, we use the Emscripten flag `USE_SDL` to use the SDL2 library.

If you launch `app.html`, you should now be able to play Asteroids in your browser:

Press enter or click to view image in full size

![]()

Congratulations, you just ported a game to WebAssembly!

> **Fun exercise**: to make this game more interesting, set `BULLETS=100` in the file `asteroids/player.h` *😄*

**The full code is** [**available on GitHub**](https://github.com/robertaboukhalil/wasm-asteroids)**.**

**A live demo is** [**available here**](http://www.levelupwasm.com/apps/asteroids/index.html)**.**

## **Ready for more?**

If you’d like to dig deeper into how to port more interesting/complex games to the web such as Pacman (screenshot below), or if you want to learn how to get started using WebAssembly in your own web applications, **check out my book** [***Level up with WebAssembly***](http://levelupwasm.com)**.**

[![]()](http://www.levelupwasm.com/)