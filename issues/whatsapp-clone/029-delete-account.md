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

## User stories
**Who:** A user who wants to leave the service and erase their data

**Primary story (happy case)**
> As a user who no longer wants the service, I want to delete my account after confirming with a code, so that my profile, messages and media are erased.

**Additional stories**
- As a user, I want a clear warning of what will be lost, so that I do not delete by mistake.
- As a group admin deleting my account, I want admin rights to pass to another member, so that my groups keep working.

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

## Happy case
The user confirms with an OTP, the account is deactivated at once and all personal data is erased within 30 days.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Wrong or expired OTP during deletion | Deletion does not proceed |
| The user is the only admin of a group | Admin passes to another member automatically |
| The user taps Delete by accident | A confirmation with a clear warning is required |
| The erasure job fails | It retries and is alerted until complete |

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
