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

## User story
As a user, I want to manage messages so that I can reply and fix mistakes.

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
