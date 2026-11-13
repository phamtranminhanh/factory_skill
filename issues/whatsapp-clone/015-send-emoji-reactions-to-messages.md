# [015] Send emoji reactions to messages

| Field | Value |
|---|---|
| Area | 1:1 Messaging |
| Priority | P2 |
| Size | S |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Allow quick emoji reactions on a message without sending a new message.

## User story
As a user, I want to react to messages quickly.

## Functional requirements
- Long-press opens a reaction bar with 6 default emojis and a '+' to open the full picker
- Each user can have one reaction per message; tapping the same emoji removes it
- Reactions appear under the bubble with counts
- Tapping the reaction summary shows who reacted
- Reaction triggers a lightweight notification (muted by default setting)

## User flow
1. Long-press a message
2. Pick an emoji
3. Both users see it under the message instantly

## Acceptance criteria
- [ ] Long press opens a reaction picker
- [ ] Reactions show under the message and sync to both users

## Edge cases & error handling
- Reacting to a deleted message is blocked
- Two users react at the same moment: both stored
- Offline reaction queues and syncs

## Non-functional requirements
- Reaction visible to the other party in under 1s

## Technical notes (Suggestion)
- Separate `reactions(message_id, user_id, emoji)` table; events over the gateway.

## Testing notes
- Add, change, remove reactions from two devices.

## Out of scope
- Custom stickers.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
