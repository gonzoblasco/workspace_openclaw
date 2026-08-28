# Draft - Reply to react-spectrum PR #10517 (review 5046701957)

**Context:** PR #10517 "fix: expose input styling on RAC Checkbox and Radio". Maintainer snowystinger left an inline comment on Checkbox.tsx (line 123) asking for a smaller API and manual screen reader validation via story. This is the draft reply.

**Goal:** respond directly to the substance with evidence, no greeting, no thanks, no filler. English, no em dash.

---

## Draft reply (English)

You're right that exposing raw control over `VisuallyHidden` gives people a lot of rope, and the `visibility: hidden` trap is a real one - it is the natural thing to reach for and it does break screen reader exposure.

Two things I'd like to do:

1. **Add a story and validate it with a real screen reader.** I'll add a story for Checkbox and Radio that stretches the hidden input over the component using the documented technique (`visuallyHiddenStyle={{inset: 0, width: 'auto', height: 'auto'}}` + `inputStyle={{position: 'absolute', inset: 0}}`), and confirm with VoiceOver that the focus ring tracks the component and the input stays exposed.

2. **Propose a smaller API.** Instead of exposing all four props (`inputClassName/inputStyle` + `visuallyHiddenClassName/visuallyHiddenStyle`), I'd rather explore a single prop that encodes the safe pattern and keeps `VisuallyHidden` encapsulated. Something like a `focusRing` or `inputPosition` boolean that applies the correct positioning internally (label as containing block, wrapper stretched, input filling it) without handing out arbitrary style/className access. That achieves the fix for the reported issue with a much smaller surface, and it cannot be used to accidentally un-accessible the component.

My instinct is option 2 is the right shape for a library like this - the reported issue is specifically about the screen reader focus ring not tracking the component, and a boolean that encodes "make the hidden input cover the component" solves exactly that without exposing implementation details.

Want me to put together a proposal for the smaller prop (with the story + VoiceOver check) so we can compare it side by side against the current approach?

---

## Notes

- No greeting, no thanks. Directly to the substance, per Gonzo's rule (only thank humans, and even then only when it adds something; here it's pure noise).
- Option 2 (single boolean prop) directly addresses snowystinger's "we do not want to expose all of these props if possible".
- The story + VoiceOver validation is the concrete ask; committing to it shows good faith and unblocks the conversation.
- Check with `scripts/check_em_dash.py` before publishing.
