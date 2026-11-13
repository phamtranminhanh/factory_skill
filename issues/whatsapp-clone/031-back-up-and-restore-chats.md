# [031] Back up and restore chats

| Field | Value |
|---|---|
| Area | Backup |
| Priority | P3 |
| Size | L |
| Suggested role | Backend |
| Depends on | 010 |

## Overview
Let users back up their chat history to the cloud and restore it on a new phone.

## User story
As a user, I want to restore chats on a new phone.

## Functional requirements
- Settings > Chats > Backup with manual 'Back up now' and schedule (daily/weekly/monthly)
- Backup to the user's own cloud (Google Drive / iCloud) as an encrypted archive
- Include or exclude media and videos
- Optional password or 64-digit key to encrypt the backup
- Restore prompt during onboarding after OTP verification
- Progress UI and Wi-Fi-only option
- Show last backup time and size

## User flow
1. Enable backup
2. App uploads in the background
3. On a new phone user verifies their number
4. App offers 'Restore from backup'

## Acceptance criteria
- [ ] Encrypted backup to cloud storage on a schedule
- [ ] Restore during onboarding on a new device

## Edge cases & error handling
- Insufficient cloud storage
- Interrupted restore: resume
- Backup encryption key lost: backup is unrecoverable (warn clearly)
- Incompatible backup version
- Low battery

## Non-functional requirements
- Backup runs on charging and Wi-Fi by default
- Restore of 1 GB completes in a reasonable time with progress

## Technical notes (Suggestion)
- Platform cloud APIs; encrypted SQLite dump + media archive.

## Testing notes
- Backup and restore across devices of the same platform, interrupted restore, wrong password.

## Out of scope
- Cross-platform restore (iOS to Android).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
