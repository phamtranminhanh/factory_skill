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

## User stories
**Who:** A user in noisy groups or in meetings

**Primary story (happy case)**
> As a user in a very active group, I want to mute it for 8 hours, 1 week or always, so that it does not buzz my phone while I work or sleep.

**Additional stories**
- As a user, I want @mentions to still alert me in a muted group, so that I do not miss direct questions.
- As a user, I want to turn off message previews and change sounds globally, so that others cannot read my messages on my lock screen.

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

## Happy case
The user mutes a chat for a chosen duration, receives no alerts from it, and it unmutes automatically on expiry.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| A mute duration expires | The chat is unmuted automatically |
| The OS-level notification setting is off | The in-app settings show that notifications are disabled by the system |
| A muted chat gets an @mention (bypass on) | The user is still alerted |

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
