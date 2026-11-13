# [026] Mute chats and customise notification settings

| Field | Value |
|---|---|
| Area | Notifications |
| Priority | P2 |
| Size | S |
| Suggested role | Mobile |
| Depends on | 025 |

## Overview
Give users control over how and when they are notified.

## User story
As a user, I want control over alerts.

## Functional requirements
- Mute a chat for 8 hours, 1 week or always from the chat menu or swipe action
- Global settings: message sounds, vibration, show preview, in-app sounds
- Per-chat custom tone (optional)
- Muted state syncs across devices
- Mentions can bypass mute (toggle)
- Do-not-disturb schedule (optional)

## User flow
1. Open chat menu > Mute
2. Choose duration
3. Chat shows a muted icon and no alerts are delivered

## Acceptance criteria
- [ ] Mute a chat for 8 hours, 1 week or always
- [ ] Toggle sound, vibration and preview

## Edge cases & error handling
- Mute expires: automatically unmute
- Calls from muted chats still ring unless blocked
- OS-level notification settings override

## Non-functional requirements
- Setting applied server-side so pushes are not sent at all when muted

## Technical notes (Suggestion)
- `chat_settings(user_id, chat_id, muted_until)`.

## Testing notes
- Each duration, expiry, sync across devices, mention bypass.

## Out of scope
- Notification categories per message type.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
