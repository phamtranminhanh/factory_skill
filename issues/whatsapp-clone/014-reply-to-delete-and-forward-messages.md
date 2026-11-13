# [014] Reply to, delete and forward messages

| Field | Value |
|---|---|
| Area | 1:1 Messaging |
| Priority | P1 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Give users basic control over messages in a chat: reply with a quote, delete mistakes and forward to others.

## User stories
**Who:** A user who makes typos or replies to older messages

**Primary story (happy case)**
> As a user in a busy chat, I want to reply to a specific message with a quote, so that the other person knows exactly what I'm answering.

**Additional stories**
- As a user who sent a message to the wrong chat, I want to delete it for everyone within an hour, so that the wrong person does not keep it.
- As a user, I want to forward a useful message (such as an address) to up to 5 chats at once, so that I do not have to retype it.
- As a user, I want to copy the text of a message, so that I can paste it elsewhere.

## Functional requirements
- Swipe right or long-press > Reply shows a quoted preview above the input; tapping the quote scrolls to the original
- Delete for me removes it locally only
- Delete for everyone allowed within 1 hour of sending; shows 'This message was deleted' to both
- Forward to up to 5 chats at once; forwarded messages carry a 'Forwarded' label
- Copy text action
- Long-press menu is accessible and keyboard friendly

## User flow
1. Long-press a message
2. Choose Reply, Delete or Forward
3. Action completes with visible feedback

## Happy case
The user replies with a quote, deletes a message for everyone within an hour, and forwards a message to selected chats; each shows the right result to both sides.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The user tries to delete for everyone after 1 hour | Only 'Delete for me' is offered |
| The recipient is offline during delete for everyone | The deletion applies when they reconnect |
| The user replies to a message that was deleted | The quote shows 'Message unavailable' |
| A forward goes to more than 5 chats | The action is blocked with a message about the limit |

## Acceptance criteria
- [ ] Swipe to reply quotes the original message
- [ ] Delete for me and delete for everyone (within 1 hour)
- [ ] Forward a message to one or more chats

## Edge cases & error handling
- Replying to a deleted message shows 'Message unavailable'
- Delete for everyone on an offline recipient: applies when they reconnect
- Forwarding media re-uses the uploaded file, not re-upload
- After 1 hour only 'Delete for me' is offered

## Non-functional requirements
- Actions respond in under 200ms locally

## Technical notes (Suggestion)
- Messages carry `reply_to_id`, `forwarded` flag and a `deleted_at` tombstone.

## Testing notes
- All three actions on text and media, across two devices, with offline recipient.

## Out of scope
- Edit message, starring/pinning messages.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
