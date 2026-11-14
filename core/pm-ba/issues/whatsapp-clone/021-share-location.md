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

## User stories
**Who:** A user meeting a friend or sending directions

**Primary story (happy case)**
> As a user, I want to send my current location as a map pin in a chat, so that my friend can find me at the cafe without describing the address.

**Additional stories**
- As a recipient, I want to tap the pin to open it in my maps app for navigation, so that I can get there directly.
- As a user who denied location permission, I want a clear message with a link to settings, so that I can enable it if I choose.

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

## Happy case
The user sends their current location and the recipient taps the map to navigate.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Location permission is denied or GPS is off | A message explains and links to settings |
| Accuracy is poor | A warning is shown before sending |
| No network for map tiles | The pin shows coordinates as text |

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
