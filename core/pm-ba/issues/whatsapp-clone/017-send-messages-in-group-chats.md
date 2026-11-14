# [017] Send messages in group chats

| Field | Value |
|---|---|
| Area | Group Chat |
| Priority | P0 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 016 |

## Overview
Sending and receiving messages inside a group chat, with member attribution, mentions and per-member read info.

## User stories
**Who:** A member of an active group chat

**Primary story (happy case)**
> As a group member, I want every message to show who sent it, with their name and avatar, so that I can follow a conversation with many people.

**Additional stories**
- As a member, I want to @mention someone and have them notified even if the group is muted, so that important questions get seen.
- As a sender, I want to open Message info and see which members have read my message, so that I know who still needs a reminder.
- As a removed member, I want to be clearly told I can no longer send, so that I understand why my message failed.

## Functional requirements
- Each incoming bubble shows sender name (colour per member) and avatar
- Messages fan out to all members; delivered once per device
- @mention: typing @ opens a member picker; mentioned users get a distinct notification and highlight, even if the group is muted
- Message info shows delivered/read by member list
- Reply, forward and reactions work like 1:1 chat
- System messages for membership changes appear inline
- Restriction: when set to admins only, non-admins see a disabled input

## User flow
1. Open a group
2. Type a message and send
3. All members receive it; a mentioned member gets a special alert

## Happy case
A member sends a group message; every member sees it with the sender's name and avatar, and a mentioned member is notified.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| A member is removed while typing | Send fails with 'You are no longer a member' |
| A user mentions someone who left | The mention is shown as plain text and no alert is sent |
| The group is set to admins only and a non-admin tries to write | The input is disabled with an explanation |

## Acceptance criteria
- [ ] Messages show the sender name and avatar
- [ ] Receipts show who has read a message (info screen)
- [ ] Mentions with @ notify the mentioned member

## Edge cases & error handling
- Member removed while typing: send fails with 'You are no longer a member'
- Large groups: batching of receipts to avoid event storms
- Mentioning a user who left
- Sender blocked by a member: that member does not receive the message

## Non-functional requirements
- Fan-out to 256 members under 2s (p95)

## Technical notes (Suggestion)
- Fan-out on the server per recipient queue; receipts aggregated.

## Testing notes
- 3+ devices in one group, mentions in muted group, removed member, admin-only mode.

## Out of scope
- Group calls, polls.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
