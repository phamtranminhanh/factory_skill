# [008] Block and unblock a contact

| Field | Value |
|---|---|
| Area | Contacts |
| Priority | P1 |
| Size | S |
| Suggested role | Backend |
| Depends on | 007 |

## Overview
Allow a user to block unwanted contacts so they can no longer message or call them.

## User story
As a user, I want to block someone so that they cannot contact me.

## Functional requirements
- Block from the chat header menu or contact info screen with a confirmation
- Blocked user cannot send messages, call, or see last seen/online/profile photo/about changes
- Blocked user is not notified
- Blocked contacts list in Settings > Privacy with an Unblock action
- Messages sent by a blocked user are silently dropped, not queued
- Blocking works for numbers that are not in contacts

## User flow
1. Open chat > menu > Block
2. Confirm
3. Chat shows 'You blocked this contact'
4. Later unblock from Settings > Privacy > Blocked

## Acceptance criteria
- [ ] Blocked user cannot send me messages or call me
- [ ] Blocked contacts can be viewed and unblocked in Settings

## Edge cases & error handling
- Block while the other user is mid-call: end the call
- Group chats with a blocked user: user still sees group messages but the blocked user cannot DM
- Unblocking does not restore messages sent during the block

## Non-functional requirements
- Block takes effect on the server within 2 seconds

## Technical notes (Suggestion)
- Server-side `blocks(user_id, blocked_id)` table checked in the message gateway.

## Testing notes
- Block, send from the blocked account, unblock, verify messaging resumes only for new messages.

## Out of scope
- Report and block spam flow.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
