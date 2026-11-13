# [023] Make and receive video calls

| Field | Value |
|---|---|
| Area | Calls |
| Priority | P2 |
| Size | L |
| Suggested role | Mobile |
| Depends on | 022 |

## Overview
Extend voice calls with live video.

## User stories
**Who:** Two users who want to see each other

**Primary story (happy case)**
> As a user on a voice call, I want to turn on my camera or start a video call directly, so that I can show my friend or family something live.

**Additional stories**
- As a user on a slow network, I want the call to lower video quality, or drop to audio only, instead of freezing, so that the conversation continues.
- As a user, I want to flip between front and back cameras, so that I can show my surroundings.

## Functional requirements
- Video call button in chat header; can also upgrade a voice call to video
- Local preview picture-in-picture, remote full screen
- Controls: camera on/off, flip camera, mute, end
- Adaptive resolution (up to 720p) based on bandwidth; falls back to audio-only on very poor network
- Landscape support
- Camera permission handling

## User flow
1. Tap the video icon
2. Callee accepts
3. Both see video; toggle camera as needed

## Happy case
Both users see each other's video, can toggle camera and flip it, and the call ends cleanly.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Camera permission is denied | The call continues as audio only |
| Bandwidth is very low | Resolution drops, then video pauses, audio continues |
| The device has no front camera | The flip button is hidden |

## Acceptance criteria
- [ ] Camera on/off and front/back switch
- [ ] Adapts quality to bandwidth

## Edge cases & error handling
- Camera permission denied: join audio only
- Device lacks a front camera
- Thermal throttling: reduce resolution
- App goes to background: keep audio, pause video

## Non-functional requirements
- Video latency under 500ms on good networks
- Battery impact monitored

## Technical notes (Suggestion)
- WebRTC video tracks with simulcast optional.

## Testing notes
- Flip camera, rotate, poor network, background/foreground.

## Out of scope
- Screen sharing, filters, group video.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
