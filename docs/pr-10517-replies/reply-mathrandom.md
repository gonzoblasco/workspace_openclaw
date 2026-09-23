You are right, and the random id was the wrong fix.

The reason to move off `React.useId` was real: it does not exist before React 18, and the React 16/17 CI jobs crashed on it (test-16 and test-17 failed on 79e3cc9de, and the next commit replaced it). But `react-aria/useId` is the version-safe equivalent - it resolves to React.useId on 18+ and to a counter on 16/17 - and it is what Button, Dialog, Disclosure and Tree already use in this package.

So I will switch to `useId` from `react-aria/useId` and keep the sanitizer, since React's id contains colons which are not valid in a `<dashed-ident>`.

`Math.random` also breaks SSR: the value differs between server and client, so the rendered `anchor-name` style attribute would mismatch on hydration.
