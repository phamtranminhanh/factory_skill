# [028] Configure privacy settings

| Field | Value |
|---|---|
| Area | Settings & Privacy |
| Priority | P1 |
| Size | M |
| Suggested role | Backend |
| Depends on | 005 |

## Overview
Let users decide who can see their personal information and activity.

## User story
As a user, I want to control who sees my info.

## Functional requirements
- Settings > Privacy with options for Last seen & online, Profile photo, About: Everyone / My contacts / Nobody
- Read receipts toggle (when off, user also does not see others' blue ticks)
- Who can add me to groups: Everyone / My contacts
- Blocked contacts shortcut
- Settings are enforced server-side, not only in the UI
- Changes take effect immediately and are synced across devices

## User flow
1. Settings > Privacy
2. Change 'Last seen' to 'Nobody'
3. Other users no longer see last seen

## Acceptance criteria
- [ ] Choose who sees last seen, photo and about: everyone, contacts or nobody
- [ ] Toggle read receipts

## Edge cases & error handling
- Reciprocity rule for last seen and read receipts
- Existing group memberships not affected by the new group-invite setting
- Defaults are privacy-friendly where required by law

## Non-functional requirements
- Enforced in all API responses; audited by tests

## Technical notes (Suggestion)
- `privacy_settings` table consulted by profile and presence endpoints.

## Testing notes
- Each option vs. contact and non-contact viewer accounts.

## Out of scope
- Disappearing messages, app lock (future issues).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
