# [013] Show typing indicator and online/last seen

| Field | Value |
|---|---|
| Area | 1:1 Messaging |
| Priority | P1 |
| Size | S |
| Suggested role | Backend |
| Depends on | 010 |

## Overview
Show live presence signals in the chat header: when the other person is typing, and whether they are online or when they were last seen.

## User stories
**Who:** A user in an active, back-and-forth conversation

**Primary story (happy case)**
> As a user waiting for an answer, I want to see 'typing…' and whether my contact is online or when they were last seen, so that I know whether to wait or call instead.

**Additional stories**
- As a user who values privacy, I want to hide my last seen from everyone, so that people cannot track my activity.
- As a user, I want the typing indicator to disappear after a few seconds of inactivity, so that it does not mislead me.

## Functional requirements
- 'typing…' appears within 1s of the other user typing and disappears after 3s of inactivity
- Header shows 'online' or 'last seen today at HH:mm'
- Presence respects privacy settings (hidden if the user chose 'Nobody')
- Typing events throttled to at most 1 per 2 seconds
- Presence updates on app foreground/background

## User flow
1. User opens a chat
2. Sees 'online' under the name
3. Other user types; header shows 'typing…'

## Happy case
The user sees 'typing…' while the contact types and 'online' or a correct last-seen time in the header.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The contact's last seen is hidden | Nothing is shown and the viewer's own last seen is also hidden (reciprocal) |
| The contact's connection drops | Presence expires after 60s and shows last seen, not 'online' |
| Typing stops | The indicator disappears after 3 seconds |

## Acceptance criteria
- [ ] 'typing…' shows within 1s and disappears after 3s idle
- [ ] Online or last seen time is shown in the chat header

## Edge cases & error handling
- Hidden last seen: show nothing, and the viewer also cannot see the other's last seen (reciprocal rule)
- Multiple devices: online if any device is active
- Network drop: presence expires after 60s without heartbeat

## Non-functional requirements
- Low bandwidth: ephemeral events are not persisted

## Technical notes (Suggestion)
- Ephemeral events over the gateway; Redis keys with TTL for presence.

## Testing notes
- Type on one device and watch another; background the app; privacy 'Nobody' setting.

## Out of scope
- Group typing indicator details.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
