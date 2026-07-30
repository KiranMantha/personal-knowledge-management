---
type: Learning
title: Pass cli args to nodejs program and read them
topic: Backend_Databases_etc
tags:
  - nodejs
  - cli
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:34.729Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:34.729Z'
---
```javascript
// index.js
const getArgs = () =>
  process.argv.reduce((args, arg) => {
    // long arg
    if (arg.slice(0, 2) === "--") {
      const longArg = arg.split("=");
      const longArgFlag = longArg[0].slice(2);
      const longArgValue = longArg.length > 1 ? longArg[1] : true;
      args[longArgFlag] = longArgValue;
    }
    // flags
    else if (arg[0] === "-") {
      const flags = arg.slice(1).split("");
      flags.forEach((flag) => {
        args[flag] = true;
      });
    }
    return args;
  }, {});

const args = getArgs();
console.log(args);
```
Examples:
-------
1. calling inline:

`node index.js -D --name=Hello` => `{ D: true, name: 'Hello' }`

2. calling via package.json
```json
// package.json
{
  "scripts": {
    "start": "node index.js"
  }
}
```
`npm start -- -D --name=Hello` => `{ D: true, name: 'Hello' }`
