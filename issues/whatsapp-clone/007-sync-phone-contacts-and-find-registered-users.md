# [007] Sync phone contacts and find registered users

| Field | Value |
|---|---|
| Area | Contacts |
| Priority | P0 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 004 |

## Overview
Find which of the user's phone contacts already use the app so they can start chatting immediately, without exposing the raw address book to the server.

## User stories
**Who:** A user with 100+ people in their phone address book

**Primary story (happy case)**
> As a new user, I want the app to tell me which of my phone contacts already use it, so that I can start chatting with them without typing numbers.

**Additional stories**
- As a privacy-minded user, I want my address book matched using hashed numbers only, so that my contacts' phone numbers are not stored by the company.
- As a user who denied contacts permission, I want to still start a chat by typing a phone number, so that I am not locked out of the app.
- As a user who just saved a new friend's number, I want the list to refresh by pull-to-refresh, so that I can chat with them immediately.

## Functional requirements
- Request contacts permission with a clear explanation
- Normalize numbers to E.164, hash them (salted SHA-256) and send hashes to the server for matching
- Show registered contacts in a 'Contacts on app' list with name from the phone and avatar from their profile
- Unmatched contacts show an 'Invite' action
- Re-sync on app start, on pull-to-refresh and when the address book changes
- Tapping a contact opens the chat with that user

## User flow
1. User taps New chat
2. Grants contacts permission
3. Sees matched contacts and taps one to chat

## Happy case
The user grants contacts access and immediately sees which contacts are on the app; tapping one opens a chat.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Contacts permission is denied | An explanation and a settings shortcut appear; the user can still type a number to chat |
| The address book is very large (10,000+) | Sync runs in batches without freezing the app |
| A contact has no registered account | They show an Invite action, not a chat |

## Acceptance criteria
- [ ] With permission, contacts are matched by hashed phone number
- [ ] Registered contacts show in a list; others show an invite option
- [ ] Denied permission shows a clear fallback

## Edge cases & error handling
- Permission denied: show an explanation and a button to open system settings; allow starting a chat by typing a number
- Duplicate contacts or multiple numbers per contact
- Large address books (10,000+): sync in batches
- Contact changes their number or deletes the account

## Non-functional requirements
- Initial sync of 1,000 contacts in under 5s
- Server never stores raw phone numbers of non-users
- Privacy policy updated to describe contact usage

## Technical notes (Suggestion)
- Use native contacts APIs; matching endpoint accepts batches of up to 500 hashes.

## Testing notes
- No permission, partial permission (iOS limited access), big address book, contact added while app is open.

## Out of scope
- Inviting non-users (see invite issue).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
