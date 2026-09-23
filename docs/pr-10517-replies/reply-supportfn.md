With the CSS variable approach below, the hook goes away entirely, so this function goes with it - the check only stays in the browser tests, as the skip condition.

If we keep a check on the src side it should stay lazy. A module-load constant also evaluates during SSR, where `CSS` does not exist, so it can freeze a false the client then reuses.
