# [009] Invite friends via share link

| Field | Value |
|---|---|
| Area | Contacts |
| Priority | P3 |
| Size | S |
| Suggested role | Mobile |
| Depends on | 007 |

## Overview
Let a user invite friends who are not on the app via the system share sheet.

## User story
As a user, I want to invite friends so that they can join.

## Functional requirements
- 'Invite friends' entry in Settings and in the contacts list
- Opens the native share sheet with a prefilled message and a link to the store listing
- Invite link has a referral parameter for tracking (optional)
- Show count of invites sent (optional)

## User flow
1. Settings > Invite friends
2. Share sheet opens
3. User picks an app and sends

## Acceptance criteria
- [ ] Share sheet opens with an invite message and download link

## Edge cases & error handling
- No share targets available: fall back to copy link
- Link must route iOS users to the App Store and Android users to Google Play

## Non-functional requirements
- Message text is localizable

## Technical notes (Suggestion)
- Branded short link service or Firebase Dynamic Links alternative.

## Testing notes
- Share via a messaging app, open on iOS and Android, verify redirect.

## Out of scope
- Rewards or referral programs.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
