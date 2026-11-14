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

## User stories
**Who:** A user whose friends are not on the app yet

**Primary story (happy case)**
> As a user, I want to send my friends an invite link through any app on my phone (SMS, email, social), so that more of my contacts can join and I can chat with them.

**Additional stories**
- As a friend who receives the link on an iPhone or Android phone, I want it to open the right store page, so that I can install the app in one tap.

## Functional requirements
- 'Invite friends' entry in Settings and in the contacts list
- Opens the native share sheet with a prefilled message and a link to the store listing
- Invite link has a referral parameter for tracking (optional)
- Show count of invites sent (optional)

## User flow
1. Settings > Invite friends
2. Share sheet opens
3. User picks an app and sends

## Happy case
The user taps Invite, picks an app, sends the link, and the friend opens the right store page and installs.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| No app can handle sharing | The link is copied to the clipboard with a toast |
| The link is opened on a desktop browser | A landing page shows both store links |
| The share is cancelled | Nothing is sent and the user returns to the previous screen |

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
