# [021] Share location

| Field | Value |
|---|---|
| Area | Media Sharing |
| Priority | P2 |
| Size | S |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Let a user share their current location in a chat.

## User story
As a user, I want to share my location.

## Functional requirements
- Attach menu > Location asks for location permission
- Shows a map with the current position and a 'Send your current location' button
- Message bubble displays a static map preview with address text
- Tap opens the location in the maps app
- Live location sharing is out of scope for this issue

## User flow
1. Tap + > Location
2. Confirm position
3. Send
4. Recipient taps the map to navigate

## Acceptance criteria
- [ ] Send current location as a map preview
- [ ] Tapping opens the maps app

## Edge cases & error handling
- Permission denied or GPS off: explain and link to settings
- Low accuracy: show a warning
- No network for map tiles: show coordinates text

## Non-functional requirements
- Location is sent once and not tracked afterwards
- Privacy: precise location only after explicit tap

## Technical notes (Suggestion)
- Static map image from a maps provider; coordinates stored in message payload.

## Testing notes
- Permission paths, airplane mode, opening in maps.

## Out of scope
- Live location, nearby places search.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
