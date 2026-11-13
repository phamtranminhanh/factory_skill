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

## User story
As a user, I want to see past calls.

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
