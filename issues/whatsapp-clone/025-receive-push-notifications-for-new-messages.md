# [025] Receive push notifications for new messages

| Field | Value |
|---|---|
| Area | Notifications |
| Priority | P0 |
| Size | M |
| Suggested role | Backend |
| Depends on | 010 |

## Overview
Notify users of new messages when the app is closed or in the background, using platform push services.

## User stories
**Who:** A user who has the app closed or the phone locked

**Primary story (happy case)**
> As a user whose phone is locked, I want a notification with the sender's name and message preview when a message arrives, so that I can decide whether to reply now.

**Additional stories**
- As a user, I want to tap the notification to open that exact chat, so that I do not have to find it.
- As a user, I want to reply or mark as read straight from the notification, so that I can respond quickly.
- As a user who denied notification permission, I want an in-app banner explaining how to enable it, so that I do not miss messages.

## Functional requirements
- Register the device push token on login and refresh on change
- Server sends a push when a message arrives for an offline device
- Notification shows sender name and message preview (respecting the 'show preview' setting); grouped per chat
- Tapping a notification opens the exact chat
- Reply and Mark as read quick actions
- Badge count updated
- Muted chats do not alert
- Silent push syncs messages in the background

## User flow
1. Recipient's app is closed
2. Message is sent
3. Push arrives within seconds
4. Tap opens the chat

## Happy case
A message arrives while the app is closed, a notification appears in seconds, and tapping it opens that chat.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Notification permission is denied | An in-app banner explains how to enable it |
| The push token is invalid or expired | It is removed and a new one is registered on next launch |
| The message was already read on another device | The notification is dismissed |
| The chat is muted | No alert is shown |

## Acceptance criteria
- [ ] Push arrives within 5s of a message
- [ ] Tapping opens the right chat
- [ ] Muted chats do not notify

## Edge cases & error handling
- Invalid or expired token: remove it
- Notification permission denied: show an in-app banner explaining how to enable
- Multiple messages collapse into one summary notification
- User already read the message on another device: dismiss the notification
- With E2EE, preview text is decrypted on device by a notification service extension

## Non-functional requirements
- Push delivered within 5s for 95% of sends
- No message content in plain text through the push provider when E2EE is enabled

## Technical notes (Suggestion)
- FCM for Android, APNs for iOS; notification service extension for decryption.

## Testing notes
- App killed, background, foreground; tapping; muted; permission denied; multi-device dismissal.

## Out of scope
- Marketing push, per-contact custom tones.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
