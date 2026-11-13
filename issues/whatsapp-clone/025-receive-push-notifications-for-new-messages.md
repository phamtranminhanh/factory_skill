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

## User story
As a user, I want alerts when I get messages while the app is closed.

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
