---
title: "Building LightOS with React Native"
url: https://medium.com/p/4b6e4ad1cd7f
---

# Building LightOS with React Native

[Original](https://medium.com/p/4b6e4ad1cd7f)

Press enter or click to view image in full size

![]()

# Building LightOS with React Native

[![Hugh Francis](https://miro.medium.com/v2/resize:fill:64:64/0*pwmGS0V412190UU_.jpeg)](/@hhff?source=post_page---byline--4b6e4ad1cd7f---------------------------------------)

[Hugh Francis](/@hhff?source=post_page---byline--4b6e4ad1cd7f---------------------------------------)

13 min read

·

Jan 8, 2020

--

8

Listen

Share

More

The Light Phone 2 is a minimalist cellphone that was named one of [Time Magazine’s best inventions of 2019](https://time.com/collection/best-inventions-2019/5733061/the-light-phone-ii/). In early 2018, we joined Light to build the operating system and supporting software stack, namely the **“LightOS”**.

[## The Light Phone

### Light is a radically different technology company. We design beautiful tools that respect and empower our users and our…

www.thelightphone.com](https://www.thelightphone.com/?source=post_page-----4b6e4ad1cd7f---------------------------------------)

As far as we know, **LightOS is the first operating system built with React Native** — this post will serve as a teardown of how the device works, why we chose React Native, and some of the challenges we faced in development.

## Chipset and Base OS

When developing hardware, one of the biggest software constraints is the chipset. This is because usually, included with the chipset, will be a vanilla build of a base operating system (usually a flavor of Linux, or by extension, Android). If you want to change it at this point, it’s usually a big task, as you’ll likely have to rewrite all of the custom drivers for your alternative OS.

![]()

The LightOS runs a Qualcomm Snapdragon — the MSM8909 to be exact. It’s an entry level smartphone chipset (great for wearables).

Given The Light Phone 2 is “designed to be used as little as possible”, the MSM8909 makes a nice tradeoff between flexibility and price.

As such, the LightOS is based on the Android Operating System Project (referred to herein as AOSP). It’s a fork of Android 8.1, originally provided to us by Qualcomm, and customized for the chipset.

[## Android Open Source Project

### Android is an open source operating system for mobile devices and a corresponding open source project led by Google…

source.android.com](https://source.android.com/?source=post_page-----4b6e4ad1cd7f---------------------------------------)

**All of that is to say:** when we refer to the LightOS, we are referring to “our custom fork of Android 8.1 that embeds a platform-signed React Native app as the default launcher” (amongst other drivers and low-level customizations).

## The Eink Screen

The Light Phone 2 has a bunch of peripheral components, but by far the most interesting is it’s Eink Screen (measures 2.84" diagonally, 16 shades of grey, with a resolution of 600x480).

In case you’re not familiar (I wasn’t!), an Eink screen is made up of millions of microcapsules, each holding black and white particles that can be moved in the Z axis by applying a positive or negative charge.

![]()

This quality makes the device fantastic for eye strain — it doesn’t blast blue (LCD) light into your eyeballs late at night, and feels like a natural surface for reading.

There’s a few difficulties that come along when working with a physical screen material like Eink, however:

### 1. Eink is prone to “ghosting”

Ghosting is the effect where those internal Eink particles “get stuck” between updates. Small, quick, localized updates can be great for the user experience, but because we’re driving those particles quicker, the lack of power means that they’re occasionally stuck in their old position, showing artifacts of the old frame, when a newer frame is active.

In addition, those particles can “drift”. Given they’re floating in a capsule, suspended in place only by an electrical charge, the particles will occasionally drift out of place. This means as the screen calculates a color-change differential, the math is based on the assumed position, rather than the actual position of the particle; often resulting in an incorrect update.

### 2. Eink can be slow to update (depending)

Press enter or click to view image in full size

![]()

In order to reduce that ghosting, it’s necessary to do “full screen, flashing updates”.

This is why Eink devices are known for their signature inverted color flash — that inverted flash is necessary because it resets the known position of each ink capsule, essentially forcing the image to update it’s integrity.

Unfortunately however, these fullscreen flashes can take between 600–1200ms to complete (depending on the ambient temperature).

**This makes for a maximum refresh rate of 1–2 fullscreen updates per second.**

## OK, but why React Native?

You might think that React Native is a strange choice for a native platform embedded into a firmware development project: we did too!

**Before we begin:** *yes* — we use type checked javascript via [Flow](https://flow.org/) (although these days our studio uses Typescript across the board).

[## Flow: A Static Type Checker for JavaScript

### Using data flow analysis, Flow infers types and tracks data as it moves through your code. You don't need to fully…

flow.org](https://flow.org/?source=post_page-----4b6e4ad1cd7f---------------------------------------)

### 1. Sane render cycles for an Eink Screen

After meeting with the Eink team in Taiwan, and understanding the full range of screen quirks we’d need to accommodate for, we realized we needed to find a UI programming model that would allow us to entirely separate the concerns of updating the view tree from batching, folding and dispatching updates to the Eink screen itself.

As such, we were looking for something that was:

* [**Declarative over Imperative**](https://stackoverflow.com/questions/129628/what-is-declarative-programming)**:** We wanted to layout our UI once and clearly, rather than managing painting & mutation manually
* **Reactive and Immutable:** We wanted a system that would manage it’s own render lifecycle based on changes to underlying system state
* **Abstractable:** We did not want UI developers managing framework-level screen APIs, this needed to be a “pluggable” low-level layer
* **Composable:** We’re building a UI Framework for an OS, after all!

Surprisingly, there’s not a lot in the way of Reactive UI frameworks for Java / Kotlin\*, and because we’ve built a handful of React Native apps before, the choice was obvious.

Given the Eink screen is the bottleneck at 2–3fps, **achieving 60fps was not a goal**. Additionally, the LightOS is designed to be “frame-by-frame”, with few dynamic segments and virtually no animation, so updates are often folded and batched (more on that below).

\*[Litho](https://fblitho.com/) might have worked, but plain old XML layouts have to be managed imperatively, which we wanted to avoid. [Jetpack Compose](https://developer.android.com/jetpack/compose) was released after we started, but it looks pretty great!

### 2. A React-driven App SDK (coming 2020)

The average Light Phone user is a savvy consumer. They’re usually tech forward hackers, forever trying to find a way for their device to set them free.

* Just [take a look at this user](https://imgur.com/a/TLRcaaH) who hacked a makeshift CLI onto their device, using SMS!

By using React Native, we’ll soon be able to open our SDK to the widest developer community, allowing hackers and javascript developers to ship their own custom tools for the LightOS.

![]()

## The React x Eink Architecture

Of course, we wanted to lean in to React’s “Unidirectional Data Flow” pattern. Additionally, we didn’t want to block rendering in React — this would slow the UI to a crawl.

Instead, we settled on an “eventually consistent” model for rendering. This pattern went through a few iterations, until we finally landed on our VTObserver strategy, which shipped to end users in LightOS `v56-release`.

Press enter or click to view image in full size

![]()

The beauty of using React Native meant that the UI developers could go about their day building features and shipping new screens, without needing to be concerned about how each render might propagate to the Eink screen.

In order to mark a component as “having dynamic content”, they simply needed to wrap their work as a render prop for the `Eink.js` component. Here’s the TimeDisplay widget from the center of the top info bar in the Settings Panel:

On the Java side, we see React Native renders come in as “hidden” render tags in the view tree — these tags describe the update mode (the above is `Modes.DU`), and few other heuristics needed to update the screen.

As soon as a new render tag is discovered, the kernel driver goes to work synchronizing the Eink screen against the Linux frame buffer (`/devices/virtual/graphics/fb0`).

In the ~600–1200ms gap while the screen is updating, we keep collecting renders from React Native in a worker thread (so to not block the UI), batching and folding them into one single update. The moment the pending screen update propagates entirely, the kernel driver sends a uEvent into userspace. That’s our signal to stop folding, start to apply that next queued update immediately.

Press enter or click to view image in full size

![]()

## Developing against a real device

For the first couple of months, we were able to develop against the Android emulator. We setup an Android 8.1 virtual device with the same screen size as our Eink screen, and got to work fleshing out the basic UI infrastructure for our platform app.

Timing-wise this was great, as we hadn’t received a development board from our manufacturing partner just yet.

However — we soon needed to use platform-level APIs (more on accessing those below), and thus, needed to be developing against the “real” firmware.

This is because the target firmware embeds platform keys (secret signing keys that indicate to AOSP that a software component is “first party”, amongst other things). Unless an APK is signed with the target firmware’s platform keys, it will not be able to access private Android platform APIs.

Press enter or click to view image in full size

![]()

So — once we had received our first development device, and obtained the platform keys from our manufacturing partner, we setup a local `.keystore` to sign our APK in development.

**Bingo!** We could now build an APK onto our development device, giving legal access to ***all of hidden Android’s platform APIs***.

Albeit — Android Studio still couldn’t compile against them (keep reading), but we could at least get to most of them using reflection.

## Compiling against Android platform APIs in development

Most Android apps aren’t embedded into the firmware of a manufactured device — instead, they’re code-signed by a 3rd party developer, and as per Android’s permissions model, those apps won’t be able to access low-level, privileged APIs.

When you’re developing a standard 3rd party Android app, Android Studio assumes that application will be 3rd party, meaning it won’t compile if you try to access a hidden API (like a bunch of methods on `android.telephony.TelephonyManager`).

However, we’re building an OS here! We need to be able to access (and compile against) ***every method*** in the Android codebase. Later, when we code-sign our build with AOSP platform keys, we’ll get those permissions, but if we can’t develop against them, it’s a non-starter.

In order to allow Android Studio to access these APIs, we needed to build AOSP from source, and extract the framework stubs as a `.jar` file.

> Android APIs change from version to version, and the firmware build may have further customizations to AOSP, so the exact firmware target for the platform app must be used to compile your framework stubs.

Compiling AOSP is well documented, so I’ll leave that out here, but after a successful build, we had an output file like: `target/common/obj/JAVA_LIBRARIES/framework_intermediates/classes.jar`

Press enter or click to view image in full size

![]()

We took that file (renaming it `framework_all.jar`), and added it to our Android codebase, under the `android/app/libs` folder.

**Please note:** if you add or remove methods in your AOSP build, you’ll need to rebuild this file.

Next, in our`android/app/build.gradle` file, we ensure that folder is compiled first-in-line:

```
dependencies {  
    //... Ensure your framework_all.jar is compiled first:  
    compileOnly fileTree(dir: "libs", include: ["*.jar"])    //... your other dependencies here  
    implementation project(':react-native-svg')  
}
```

Finally, we `Clean Project`, and we were now able to import, use and compile against ***all*** of the hidden APIs in the entire Android SDK!

(Thanks to [Corochann](https://github.com/corochann) for the detailed post on doing this):

[## Importing Android SDK with hidden APIs

### How to import ActivityManagerNative?My first motivation was to use AndroidManagerNative class, even you can find this…

corochann.com](https://corochann.com/importing-android-sdk-with-hidden-apis-493.html?source=post_page-----4b6e4ad1cd7f---------------------------------------)

## Working against an unstable screen (and kernel)

In the early phases of development, our manufacturing partner was writing the “Hardware Abstraction Layer” (or HAL). This is fancy name for the set of C++ drivers that bridge electrical signal from our chipset to control signal for our peripherals (like the vibrating motor, or loudspeaker).

One of these custom drivers is the Eink kernel driver — the architecture we settled on was a Linux kernel driver that reads directly from the framebuffer (as noted earlier).

**Side Note:** In hindsight, a better architecture would have leveraged [Android’s in-memory surfaceflinger](https://source.android.com/devices/graphics/surfaceflinger-windowmanager) (reading directly from the framebuffer proved finicky, and required some extra workarounds). However at this time, we mostly had access to driver engineers (our framework engineers were working on mission critical pieces like FOTA), so this was the best route forward, all things considered.

Press enter or click to view image in full size

![]()

As you can probably guess, in these early days, the Eink screen barely worked. The kernel driver was riddled with bugs, and would crash the entire device with a kernel panic quite often.

So — to keep development speed at a good clip, we used [Vysor](http://vysor.io/): a fantastic open source screen mirroring software that reads directly from Android’s compositor, and allows the user to interact with their device directly from the computer.

This meant that our unstable screen did not block development during those early days! Vysor is free to use, and Vysor Pro is $40 for a lifetime license.

[## Vysor

### Are you an Android developer? Vysor gives you the integration and ease of an emulator on a physical device.

vysor.io](http://vysor.io/?source=post_page-----4b6e4ad1cd7f---------------------------------------)

## Signing & Embedding React Native in AOSP

The final piece to embedding a React Native build into an Android image is to actually include it in the firmware build process, so that devices leaving the factory would boot directly into it.

This is well documented for a regular Android app, but there’s a few gotchas when using React Native.

### 1. Extract React Native’s `armeabi-v7a` and `x86` libs

An APK file is nothing more than a fancy `.zip`, and amongst the files in that archive are a bunch of pre-built `.so` files, required by React Native at runtime. Specifically, these are:

```
libfb.so  libfolly_json.so  libglog_init.so  libglog.so  libgnustl_shared.so  libicu_common.so libimagepipeline.so  libjsc.so libprivatedata.so  libreactnativejni.so  libyoga.so
```

**Note:** While it’s not necessary (we only have a single target architecture), we grabbed the versions in both `lib/armeabi-v7` (32 bit) and `lib/x86` (64 bit) so that our build can work on as many architectures as possible, should it be necessary in the future.

Usually, when a React Native APK is installed from an app store, the Android process will discover and extract these libs, but in the case of an embedded platform app, that process is skipped.

As such, we needed to move and place these files as part of the firmware build step manually.

### 2. Create a Package Directory for the APK

For the sake of easy and consistent packaging (via [CircleCI](https://circleci.com/)), we chose to use prebuilt a React Native APK, rather than have it built from source in the firmware. As such, we setup a new directory in the AOSP workspace:

```
packages/apps/LightOS/  
├── LightOS.apk  
├── Android.mk  
├── lib/  
|   ├── libfb.so  
|   ├── libfolly_json.so  
|   ├── libglog_init.so  
|   ├── libglog.so  
|   ├── libgnustl_shared.so  
|   ├── libicu_common.so  
|   ├── libimagepipeline.so  
|   ├── libjsc.so  
|   ├── libprivatedata.so  
|   ├── libreactnativejni.so  
|   ├── libyoga.so  
└── lib64/  
    ├── libfb.so  
    ├── libfolly_json.so  
    ├── libglog_init.so  
    ├── libglog.so  
    ├── libgnustl_shared.so  
    ├── libicu_common.so  
    ├── libimagepipeline.so  
    ├── libjsc.so  
    ├── libprivatedata.so  
    ├── libreactnativejni.so  
    └── libyoga.so
```

Press enter or click to view image in full size

![]()

### 3. Setup the Android.mk File

The Android.mk file instructs the AOSP build how to include the package. Given the 22 dependencies, this file was extra long, but I’ve shortened it here as it’s a lot of copy/paste:

```
LOCAL_PATH := $(call my-dir)# Move 32 bit deps  
include $(CLEAR_VARS)  
LOCAL_MODULE := libfb  
LOCAL_SRC_FILES := lib/libfb.so  
LOCAL_MODULE_TAGS := optional  
LOCAL_MULTILIB := 32  
LOCAL_MODULE_SUFFIX := .so  
LOCAL_MODULE_CLASS := SHARED_LIBRARIES  
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/vendor/lib  
include $(BUILD_PREBUILT)#... and so on for each extracted file in ./LightOS/lib/*.so# Move 64 bit deps  
include $(CLEAR_VARS)  
LOCAL_MODULE := libfb  
LOCAL_SRC_FILES := lib64/libfb.so  
LOCAL_MODULE_TAGS := optional  
LOCAL_MULTILIB := 64  
LOCAL_MODULE_SUFFIX := .so  
LOCAL_MODULE_CLASS := SHARED_LIBRARIES  
LOCAL_MODULE_PATH := $(PRODUCT_OUT)/vendor/lib64  
include $(BUILD_PREBUILT)#... and so on for each extracted file in ./LightOS/lib64/*.so# Actually make the LightOS  
include $(CLEAR_VARS)  
LOCAL_MODULE_TAGS := optional  
LOCAL_MODULE := LightOS  
LOCAL_SRC_FILES := $(LOCAL_MODULE).apk  
LOCAL_MODULE_CLASS := APPS  
LOCAL_MODULE_SUFFIX := $(COMMON_ANDROID_PACKAGE_SUFFIX)  
LOCAL_CERTIFICATE := platform  
LOCAL_PRIVILEGED_MODULE := true  
include $(BUILD_PREBUILT)
```

**Important:** Note the `LOCAL_CERTIFICATE := platform` in the final block. This line ensures our React Native APK is code-signed with the firmware’s platform keys, so that we can access those Android Platform APIs.

### 4. Add the PRODUCT\_PACKAGE

Finally, we add the LightOS as a part of the firmware `make` step.

```
PRODUCT_PACKAGES += LightOS
```

This instruction can be added in a variety of different places, but in our case, in the following two files:

```
- device/qcom/common/common.mk  
- device/qcom/common/common64.mk
```

(We found this by grep’ing for the string `PRODUCT_PACKAGES`).

## And that’s just the beginning

This post barely scratches the surface of the enormous infrastructure supporting the LightOS. In addition to the firmware image, we built a custom eCommerce experience, fully featured user dashboard, a cloud sync’d contact address book, and even the supply and activation of Light SIM cards.

Press enter or click to view image in full size

![]()

Across the LightOS ecosystem, we’re using 9 (or more?) programming languages, and a variety of infrastructures like Kubernetes, Serverless Node, Elixir Phoenix, WebDAV, React.js, Ember.js, Docker, CircleCI and many others. It’s a huge, sprawling system, that has been incredibly interesting to build and maintain.

Press enter or click to view image in full size

![]()

[You can buy a Light Phone over here](https://www.thelightphone.com/), and if you’re interested in joining Sanctuary Computer’s NYC development team, please email me via **hugh@sanctuary.computer** — we’re always looking for sharp people with an eye towards functional programming, and typesafe, performant code.

— Hugh