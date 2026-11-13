# [024] Show call history

| Field | Value |
|---|---|
| Area | Calls |
| Priority | P2 |
| Size | S |
| Suggested role | Mobile |
| Depends on | 022 |

## Overview
Show a log of past calls so users can quickly call back.

## User stories
**Who:** A user who missed or wants to return a call

**Primary story (happy case)**
> As a user, I want a Calls list showing incoming, outgoing and missed calls with time and duration, so that I can see who tried to reach me.

**Additional stories**
- As a user, I want to tap a missed call to call back, so that I can respond in one step.
- As a user, I want to delete entries or clear the whole history, so that I can keep my call log private.

## Functional requirements
- Calls tab lists calls: contact, direction icon (incoming/outgoing/missed), time and duration
- Missed calls highlighted in red
- Tap a row to call back; info button opens call details
- Swipe to delete an entry; clear all
- Entries sync across the user's devices

## User flow
1. Open the Calls tab
2. See recent calls
3. Tap to call back

## Happy case
The Calls tab lists every recent call correctly and tapping an entry calls the person back.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The call history fails to load | An error with retry; no entries are lost |
| A call was from an unknown number | The number is shown instead of a name |
| The user has no calls yet | An empty state invites them to make one |

## Acceptance criteria
- [ ] List of incoming, outgoing and missed calls with duration
- [ ] Tap to call back

## Edge cases & error handling
- Unknown number (not a contact) shows phone number
- Contact deleted: show number
- Empty state

## Non-functional requirements
- List loads in under 500ms

## Technical notes (Suggestion)
- `calls` table with status and duration written by the signalling service.

## Testing notes
- Missed, declined, completed calls; deletion; call back.

## Out of scope
- Call recording, scheduled calls.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
