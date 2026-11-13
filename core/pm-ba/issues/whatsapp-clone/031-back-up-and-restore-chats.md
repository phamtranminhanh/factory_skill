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

## User stories
**Who:** A user changing or losing a phone

**Primary story (happy case)**
> As a user who bought a new phone, I want to restore my chat history from a backup after verifying my number, so that I do not lose years of conversations.

**Additional stories**
- As a user, I want automatic daily, weekly or monthly backups on Wi-Fi while charging, so that I never have to remember.
- As a user, I want to protect the backup with a password or key and be warned that losing it means the backup cannot be recovered, so that my history stays private.

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

## Happy case
The user backs up, signs in on a new phone, restores, and sees the full history.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Cloud storage is full | The backup fails with a clear message and no partial backup replaces the old one |
| The restore is interrupted | It can be resumed |
| The backup password is forgotten | The user is clearly warned in advance that it cannot be recovered |
| The backup is from an incompatible version | Restore is refused with an explanation |

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
