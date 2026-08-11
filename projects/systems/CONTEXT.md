# Systems — Context

**Personal infrastructure**: the devices you own, what connects to what, and what breaks if a connection stops. Plus a small judgement layer about software, and a pointer to wherever accounts actually live.

> **Storage — read before writing anything here.** This domain has no storage of its own; its files live in the workspace's git repository and go wherever that repository goes. **This workspace's rule: private remote, never made public.** A private host is access-controlled, not encrypted — adequate for device roles and backup state, and *not* adequate for the never-write list below. See [health/CONTEXT.md](../health/CONTEXT.md) for the full reasoning; it was written for a different domain and applies here unchanged.

**This is a map, not an asset register.** An asset register serves insurance and resale and wants purchase dates, prices, serials and warranties. None of those belong here. A thing earns a place because something else depends on it, not because you own it.

**Status: specified.** The record format below was earned by real use rather than invented upfront — it exists to answer one question first, *what depends on this before I take it apart*, and it should stay no larger than that question requires.

## Never written here

Separate from, and stronger than, any publish classification. **Marking a file private stops it being published; it does not stop it being permanent.** Git history does not forget, and this repository lives on a laptop.

- **Credentials of any kind** — passwords, MFA seeds, recovery codes, security-question answers, API keys, account numbers. These belong in a password manager, whatever a repository's visibility.
- **Identity topology** — which accounts hang off which email or SSO provider, and what breaks if one is lost. Genuinely worth recording, and it belongs in an *encrypted* store, not merely a private one. Keep a pointer here and nothing else.
- **Network ingress detail** — external hostnames, public IP addresses, port forwards, VPN endpoints, dynamic-DNS names, wireless network names.
- **Precise physical addresses.** `Location:` means "desk" or "hall cupboard".

The third one is the trap specific to this domain, and it is worth stating why. A map made of connections naturally wants to record *how* each connection is reached — and for anything self-hosted, that means a port forward and a hostname. That is not inventory; it is an attack surface with directions attached.

> **Record that a connection exists and what breaks if it stops. Never record how to reach it.**

## Boundary

| Domain | Keeps | Test |
| --- | --- | --- |
| `business/` | Commerce — what equipment cost, whether it is deductible, whether it is insured | Same object, different fact. This domain never holds money |
| `finances/` | What a subscription costs and when it renews | This domain holds only that a tool is used and what for |
| `learning/` | Curricula and practice | Owning a thing is not studying it |
| `pkm/` | Durable ideas about tools and systems | Still true after you sell the hardware → PKM |

**When two domains claim the same object, they are usually claiming different facts about it.** Split by aspect and link; do not argue about an owner.

## Glossary

Terms resolved in real use. Add to it the same way — never invent vocabulary upfront.

| Term | Means |
| --- | --- |
| **Node** | A device with a section in the map. Earns one by the test below |
| **Edge** | A dependency between nodes, recorded with the consequence of it stopping |
| **Sole copy** | This node holds the only copy of something. The single most valuable flag here |
| **Recorded** | Hand-maintained, because nothing else holds it |
| **Referenced** | A pointer to the system that holds it authoritatively. Never a copy |
| **Derived** | A command, plus a dated snapshot of what it returned |

## What earns a place

> **A device earns a section if replacing it with an identical unit would require reconfiguration or moving data.**

Asked out loud: *if I swapped this for the same model out of a box, would anything need setting up again or copying across?* If yes it holds state and belongs here. If no it is equipment.

That admits computers, phones, servers, network gear, drives, and peripherals that carry drivers or configuration. It excludes anything that only passes signal — cables, stands, microphones, monitors. It needs no special case for any category, which is the point of phrasing it this way.

**Connections are recorded selectively, nodes are not.** A connection earns a line only if you can name a concrete consequence of it stopping — "nothing, really" is a valid answer that leaves it out. Nodes stay broad, because the node list is the search space in which forgotten connections get found.

## The record

One file, `systems-map.md`, with a section per device. Field lines are `Key: value` so they can be searched; connections are a list, because a consequence is a sentence and does not fit in a table cell.

```markdown
## <device>

Role: what it is for, in one line
OS: version · Location: where it physically is
Backup: what backs it up, and where that copy lands
Sole copy: yes | no
Status: active
Verified: YYYY-MM-DD

Depends on:
- <other node> — what breaks if this stops
```

**Each connection is written once, on the side that does the depending.** *What depends on this* is a search, not a field — two records of one fact can disagree, and the searched answer updates itself as a side effect of recording a dependency.

**`Verified:` is deliberate**, and a departure from this workspace's usual "git knows when it changed" rule. Git knows when a file was *edited*; it cannot tell you when a fact was *checked and found still true*, and those differ exactly when it matters. A section untouched for a year is either perfectly accurate or completely wrong.

Enumerations that a command can produce are **not** written here. `snapshots/<machine>.md` holds the command and a dated copy of its output — the command never goes stale and is the refresh mechanism, while the date makes an old snapshot visibly old rather than quietly wrong.

## State

One field, on devices only:

```yaml
status: active | retired
```

**Retired devices stay in the map.** Absence cannot mean retirement, because a retired drive in a drawer may still hold the only copy of something — which is the most valuable thing this domain records. Retirement is reversible, so it is a field rather than a folder move; expressing it by location would also break the links pointing at it.

No `done`. A device never finishes.

**Nothing else here has state.** A connection either exists or it does not, judgement about software has no lifecycle, and a snapshot's date is evidence rather than status.

## Conventions

- Part of the Obsidian vault rooted at `projects/`. Links are `[[wikilinks]]`; filenames are kebab-case.
- **The graph view is navigation, not the map.** A wikilink says two notes relate; it cannot say what breaks if a connection stops. Dependencies live in the text, deliberately.
- This domain does **not** inherit the PKM frontmatter schema — see [pkm/CONTEXT.md](../pkm/CONTEXT.md).
- Durable content belongs here, not in `memory/`. Memory holds only how Claude should behave and collaborate.
- Notes here may freely wikilink into `pkm/notes/` — one graph.
- If `systems-map.md` outgrows one file, split the device sections out and keep the rest. That is a size problem with an obvious fix; do not pre-solve it.
