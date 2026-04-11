---
name: paper-humanize
description: Placeholder for Phase B paper-humanize skill. Removes AI writing patterns from English text with academic-aware overrides. Currently not implemented.
disable-model-invocation: true
user-invocable: false
---

# paper-humanize (Phase B placeholder)

This skill is a Phase B placeholder. The full implementation is documented in
`docs/superpowers/specs/2026-04-11-academic-paper-plugin-design.md` section 4
and will be added in a separate plan.

For now this skill is `user-invocable: false` so it does not appear in the
slash menu. It exists only to reserve the `paper-humanize` name in the plugin
namespace and to make Phase A's routing eval able to reference it.

When Phase B is implemented, this file is replaced with the real skill body
that delegates to `agents/humanizer_engine.md`.
