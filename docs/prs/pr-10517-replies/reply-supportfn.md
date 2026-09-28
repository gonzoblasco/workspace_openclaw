This function is gone now. The custom property replaces the hook entirely, so there is no support check left on the component side - the declarations are inert in browsers without anchor positioning, and the check only remains in the browser tests as the skip condition.

If a check does come back to the src side later it should stay lazy: a module-load constant also evaluates during SSR, where `CSS` does not exist, so it would freeze a false the client then reuses.
