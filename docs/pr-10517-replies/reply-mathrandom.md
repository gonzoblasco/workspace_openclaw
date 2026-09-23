You are right, and the random id was treating a symptom.

The reason to move off `React.useId` was real: it does not exist before React 18, and the React 16/17 jobs crashed on it (`test-16` and `test-17` failed on 79e3cc9de). But `react-aria/useId` is the version-safe equivalent - it resolves to `React.useId` on 18+ and to a counter on 16/17 - and it is already what Button, Dialog, Disclosure and Tree use in this package.

So I switched to `useId` from `react-aria/useId`, keeping the sanitizer since React's id contains characters that are not valid in a `<dashed-ident>` in some versions.

`Math.random` also broke SSR: the value differs between server and client, so the inline `anchor-name` would have been a hydration mismatch.

The id itself has to stay per instance - see the separate comment on the custom property for the measurement.
