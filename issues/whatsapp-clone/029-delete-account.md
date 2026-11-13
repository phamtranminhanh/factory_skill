# [029] Delete account

| Field | Value |
|---|---|
| Area | Settings & Privacy |
| Priority | P2 |
| Size | S |
| Suggested role | Backend |
| Depends on | 004 |

## Overview
Allow a user to permanently delete their account and personal data, as required by app stores and data-protection laws.

## User story
As a user, I want to delete my account and data.

## Functional requirements
- Settings > Account > Delete account with a clear warning of consequences
- Re-verify by OTP to the registered number
- Account is deactivated immediately; personal data (profile, messages on server, media, backups) erased within 30 days
- Removed from groups with a system message and from contacts' lists
- Phone number becomes available for re-registration after deletion
- Confirmation email/SMS after completion

## User flow
1. Settings > Account > Delete
2. Read the warning
3. Enter OTP
4. Account deleted and the app returns to the welcome screen

## Acceptance criteria
- [ ] Confirmation with phone number re-verify
- [ ] All personal data is removed within 30 days

## Edge cases & error handling
- User is the only admin of groups: transfer admin automatically
- Pending outgoing messages are dropped
- Accidental deletion: optional 7-day grace period (open question)
- Legal retention requirements

## Non-functional requirements
- GDPR/CCPA compliant erasure with audit log
- Deletion job is idempotent

## Technical notes (Suggestion)
- Background job that purges DB rows and object-storage files.

## Testing notes
- Full deletion verified in DB and storage; re-registering the same number; group admin transfer.

## Out of scope
- Data export (separate request).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
