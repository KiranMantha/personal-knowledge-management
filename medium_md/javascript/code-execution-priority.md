JavaScript doesn’t just run code in order — it maintains multiple queues with different priorities:

- **Call Stack:** Currently executing code (highest priority)
- **Microtask Queue:** Promises, queueMicrotask, MutationObserver
- **Macrotask Queue:** setTimeout, setInterval, I/O, UI events
- **Render Queue:** requestAnimationFrame, style/layout/paint

```javascript
console.log('1: Sync');
setTimeout(() => console.log('2: Macro'), 0);
Promise.resolve()
  .then(() => console.log('3: Micro 1'))
  .then(() => console.log('4: Micro 2'));
requestAnimationFrame(() => console.log('5: RAF'));
console.log('6: Sync');

// Output: 1, 6, 3, 4, 5, 2
// Sync → All Micros → RAF → Macro
```