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

## User stories
**Who:** A user who wants to acknowledge a message without writing a reply

**Primary story (happy case)**
> As a user, I want to long-press a message and pick an emoji reaction, so that I can acknowledge it ('👍 got it') without adding another message to the chat.

**Additional stories**
- As a user, I want to see who reacted to a message in a group, so that I know who has seen and agreed.
- As a user, I want to change or remove my reaction, so that I can correct a mis-tap.

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

## Happy case
The user long-presses a message, picks an emoji, and both users see the reaction instantly under the message.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The target message was deleted | Reacting is disabled |
| The user is offline | The reaction queues and syncs on reconnect |
| Two users react at the same moment | Both reactions are stored and shown |

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
