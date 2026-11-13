# [022] Make and receive voice calls

| Field | Value |
|---|---|
| Area | Calls |
| Priority | P1 |
| Size | L |
| Suggested role | Mobile |
| Depends on | 003, 010 |

## Overview
Peer-to-peer voice calling between two users over the internet, with call signalling through the app backend.

## User story
As a user, I want to call a contact over the internet.

## Functional requirements
- Call button in chat header starts a call; ringing UI on the callee with Accept/Decline
- Signalling via the realtime gateway; media via WebRTC with STUN/TURN fallback
- In-call controls: mute, speaker, end call, call duration
- Incoming calls ring even when the app is closed (high-priority push / CallKit / ConnectionService)
- Busy state: second call shows 'User is busy' and is logged as missed
- Auto-end after 60s of no answer
- Call quality adapts (Opus codec, bitrate drops on poor network)
- Call events (missed, ended) appear in the chat

## User flow
1. User taps the call icon
2. Callee's phone rings
3. Callee accepts and the audio connects
4. Either side ends the call

## Acceptance criteria
- [ ] Outgoing and incoming call screens with ring, accept, decline
- [ ] Mute and speaker toggles
- [ ] Call ends cleanly on network loss with a message

## Edge cases & error handling
- Network drop: attempt reconnect for 15s, then end with message
- Switching Wi-Fi to cellular mid-call
- Blocked caller is rejected
- Permission to use microphone denied
- Bluetooth headset routing

## Non-functional requirements
- Call setup under 3s
- End-to-end audio latency under 400ms
- Calls are DTLS-SRTP encrypted

## Technical notes (Suggestion)
- WebRTC, coturn TURN servers, CallKit (iOS) and ConnectionService (Android).

## Testing notes
- Calls on same and different networks, background/killed app, busy, decline, bad network simulation.

## Out of scope
- Group calls, call recording.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
