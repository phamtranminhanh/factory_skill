# [020] Send voice messages

| Field | Value |
|---|---|
| Area | Media Sharing |
| Priority | P1 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Record and send short voice notes, with an inline player.

## User stories
**Who:** A user who is driving, walking or has a lot to say

**Primary story (happy case)**
> As a user, I want to hold the mic button and speak a voice message (up to 15 minutes), so that I can reply when typing is inconvenient.

**Additional stories**
- As a user, I want to slide to cancel or lock the recording so I can keep talking hands-free, so that I do not send half a message by mistake.
- As a recipient, I want to play a voice note at 1.5x or 2x speed with a waveform, so that I can listen quickly.
- As a user, I want my recording saved as a draft if a call interrupts it, so that I do not lose what I said.

## Functional requirements
- Press and hold the mic button to record; slide left to cancel; slide up to lock hands-free
- Max 15 minutes; timer shown while recording
- Preview before send in locked mode
- Waveform player with play/pause, scrubbing and speed 1x/1.5x/2x
- Played indicator (blue mic) for the sender once heard
- Plays through speaker or earpiece based on proximity sensor
- Audio encoded as Opus/AAC at ~24 kbps

## User flow
1. Hold mic
2. Speak
3. Release to send
4. Recipient taps play

## Happy case
The user records a voice note, releases to send, and the recipient plays it with a waveform.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Microphone permission is denied | An explanation and a settings shortcut appear |
| A phone call interrupts the recording | The recording is saved as a draft |
| The recording is shorter than 1 second | It is discarded silently |
| The user slides to cancel | Nothing is sent |

## Acceptance criteria
- [ ] Hold to record, slide to cancel, release to send
- [ ] Playback with waveform, speed control (1x/1.5x/2x)

## Edge cases & error handling
- Microphone permission denied
- Incoming call interrupts recording: save as draft
- Recording shorter than 1s is discarded
- Playback continues when switching screens

## Non-functional requirements
- Recording starts in under 200ms
- Voice note of 1 minute under 300 KB

## Technical notes (Suggestion)
- Native audio recorder; waveform computed on device.

## Testing notes
- Cancel, lock, interruption by call, playback speed and background.

## Out of scope
- Voice-to-text transcription.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
