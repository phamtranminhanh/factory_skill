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

## User story
As a user, I want to log out or revoke devices so that my account stays secure.

## Functional requirements
- Log out of the current device: clears tokens and local cache after a confirmation dialog
- Sessions list: device name, platform, last active time, approximate location
- Revoke any session; the revoked device is signed out on its next request or immediately via the socket
- Notify the user when a new device signs in

## User flow
1. Settings > Account > Devices
2. User sees the list and taps 'Log out' on one
3. Confirm dialog, session is revoked

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
