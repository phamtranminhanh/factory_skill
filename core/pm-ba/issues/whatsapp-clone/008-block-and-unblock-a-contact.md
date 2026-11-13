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

## User stories
**Who:** A user receiving unwanted messages from an ex-partner, spammer or stranger

**Primary story (happy case)**
> As a user receiving unwanted messages from someone, I want to block that person in two taps from the chat, so that they can no longer message or call me.

**Additional stories**
- As a user who blocked someone by mistake, I want to see a Blocked list in Settings and unblock from there, so that I can fix it.
- As a blocked person, I should not be notified, so that the blocker is not put at risk of confrontation.

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

## Happy case
The user blocks a contact in two taps, the contact can no longer message or call, and the user can unblock later from Settings.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The block request fails (network) | The user sees an error and the contact is not shown as blocked |
| The blocked person tries to message or call | Messages are dropped silently and calls are rejected, without notifying them |
| The user blocks someone in the middle of a call | The call ends immediately |

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
