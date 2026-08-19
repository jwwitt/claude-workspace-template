# ADR-0006: The enterprise systems and the agent staff

**Status:** Accepted · 2026-08-18
**Builds on:** [ADR-0005](0005-services-hold-the-record.md) — which governs the migrations; this governs the org

## Context

On 2026-08-18 Jonah decided to run his whole operation — the freelance music
business plus the personal domains — as one enterprise on the homelab, held in
three self-hosted services and worked by a staff of Claude agents. The full
plan, its 24 decisions and the three standing rulings it reverses are recorded
in [`.scratch/life-enterprise/`](../../.scratch/life-enterprise/map.md) (private);
this ADR carries the parts that constrain work beyond that effort, because a
cloner of the template receives the decisions but not the arguments.

## Decision

> **Structured, transactional records live in services; the vault keeps
> knowledge and reasoning. The services are worked by agents with named
> accounts, and nothing crosses the boundary out of the systems without
> Jonah's approval.**

Three services, each the record for what it holds (per ADR-0005):

- **Dolibarr** — the ERP: finances, CRM, invoicing, HR, helpdesk, and the
  **asset register for every item** (business gear, IT hardware, anything with
  a serial, warranty or real value). Modules are enabled only when their first
  real record exists — a full build-out of empty modules is the scaffolding
  failure with a login page.
- **OpenProject** — the project system, under full-rigor PMBOK: every project
  gets a charter, WBS, baseline, risk register, and formal change control with
  Jonah as the sole change authority. Earned value is computed from logged
  time priced at a fixed internal labor rate.
- **Vikunja** — the single roll-up point for actionable tasks. Apple Reminders
  survives only as the phone-native capture inbox that drains into it.

The **agent staff** rules, which outlive any one roster:

1. **A charter, not a daemon.** Each agent is a versioned charter file plus
   scheduled runs. No always-on processes.
2. **A named account everywhere it acts.** Each agent is a real user with its
   own API credentials in every system it touches, so every action is
   attributable in the record itself. The agents are also employees in HR —
   the org chart is legible inside the ERP.

   > **One recorded exception: the task manager.** Vikunja's projects are owned
   > by a user rather than by the instance, so a second account sees nothing
   > until every project is shared with it — the rule would buy attribution in
   > a system with one human and charge ongoing sharing maintenance for it.
   > The assistant therefore acts as the owner there. **Stated as a deviation
   > rather than absorbed**, because the next system with a per-user ownership
   > model will pose the same question, and the answer is not "named accounts
   > are optional" but "attribution is worth what the audit is worth."
3. **The boundary gate.** Inside the systems, agents create and update
   records freely. Sending email, spending money, modifying calendars,
   posting externally, or writing into the PKM notes graph requires Jonah,
   always. Autonomy is widened per-role only through recorded performance
   reviews.
4. **Failure files a ticket.** A scheduled run that fails must surface as a
   record in the helpdesk queue — state is read from the systems, never from
   a job's own report of itself.
5. **Chat is a bus, not a store.** Any conversational surface (Slack) carries
   notifications and discussion; a decision exists only once it lands in a
   system of record.

## Consequences

- **Three databases are now irreplaceable content.** Nightly dumps precede
  authority (done in `backup.sh` before this ADR was written), live DB
  directories are excluded from file backup so nothing mistakes them for one.
- **The vault's business and task files retire** per ADR-0005's four
  requirements — migrated verbatim, writers rewired in the same change,
  deleted rather than left as stale twins. Console views over them go dark.
- **Two recorded rulings are reversed knowingly** — the case against
  OpenProject (it collides with the PMAC build) and the closed subagent-roster
  entry. The reversals and their reasoning are in the effort's map; PMAC
  continues as a build project and takes over only if it one day serves
  better.
- **The cost most likely to bite:** full PMBOK rigor and time-logging demand
  discipline that has no external enforcer. The tell will be a week where no
  spent-time is logged; the change-control answer is to renegotiate the
  decision on the record, not to let the system quietly go stale.
