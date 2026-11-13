# [006] Manage sessions and log out

| Field | Value |
|---|---|
| Area | Accounts & Onboarding |
| Priority | P2 |
| Size | S |
| Suggested role | Backend |
| Depends on | 004 |

## Overview
Let users sign out of this device and review or revoke other devices that are logged into their account.

## User stories
**Who:** A security-conscious user with more than one device

**Primary story (happy case)**
> As a user who has lost an old phone, I want to see every device logged into my account and revoke the lost one remotely, so that nobody else can read my chats.

**Additional stories**
- As a user, I want to log out of the current phone with a confirmation, so that I can hand it to someone else safely.
- As a user, I want a notification when a new device signs in to my account, so that I can spot unauthorised access.

## Functional requirements
- Log out of the current device: clears tokens and local cache after a confirmation dialog
- Sessions list: device name, platform, last active time, approximate location
- Revoke any session; the revoked device is signed out on its next request or immediately via the socket
- Notify the user when a new device signs in

## User flow
1. Settings > Account > Devices
2. User sees the list and taps 'Log out' on one
3. Confirm dialog, session is revoked

## Happy case
The user opens Devices, sees every active session, revokes the lost phone, and that phone is signed out within 5 seconds.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The user revokes the current session | It behaves like a log out with confirmation |
| A revoked device is offline | It is signed out on its next connection |
| The sessions list cannot load | An error with a retry button; no sessions are lost |

## Acceptance criteria
- [ ] User can log out from the current device
- [ ] User can see and revoke active sessions

## Edge cases & error handling
- Revoking the current session behaves as a log out
- Offline device: revocation applies on next connection
- Logging out must not delete the cloud backup

## Non-functional requirements
- Revocation takes effect within 5 seconds for connected devices

## Technical notes (Suggestion)
- Store sessions with refresh-token IDs in the database; blacklist revoked token IDs.

## Testing notes
- Sign in on two devices, revoke one, verify it is kicked out and the other keeps working.

## Out of scope
- Linked-device (desktop/web) pairing.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
