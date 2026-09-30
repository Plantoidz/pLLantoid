# pLLantoid

<!-- tpc-meter:v1 -->
## Usage metering

This repo reports its paid AI usage to the Two Planets studio ledger, and tags any Stripe checkout with the project's registry slug. **Before adding or changing a model call or a checkout here, run `/meter`.** Its procedure lives in two-planets-creative at `.claude/global-skills/meter/SKILL.md`; changes there reach this repo without editing this block.

- The wiring is small on purpose: after each paid call, `meter(response, { service, endpoint })`. Don't parse usage or compute cost here; the cloud does, and its fixes reach past rows.
- Counts only, never prompts or responses. The ingest key comes from the environment; never print, copy or commit it.
- Status: not wired yet. The session that wires it: follow `/meter`, then update this line.
<!-- /tpc-meter -->
