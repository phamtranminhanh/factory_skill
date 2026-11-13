# [010] Send and receive text messages

| Field | Value |
|---|---|
| Area | 1:1 Messaging |
| Priority | P0 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 003, 005 |

## Overview
Core one-to-one chat: a user opens a conversation with a contact, reads history and sends and receives text messages in real time.

## User stories
**Who:** Any registered user chatting one-to-one

**Primary story (happy case)**
> As a user, I want to open a chat with a contact, type a message and see it appear immediately with a clear status (sending, sent, failed), so that I know whether it went through.

**Additional stories**
- As a user on a train with a patchy connection, I want my messages to queue while offline and send automatically when I am back online, so that I do not have to retype them.
- As a user returning to an old conversation, I want to scroll back through earlier messages that load quickly, so that I can find what we agreed last week.
- As a user, I want links in messages to be tappable, so that I can open them without copying.

## Functional requirements
- Chat screen with message bubbles (own right, other left), date separators and timestamps
- Text input with send button; Enter inserts a new line, max 4,096 characters
- Optimistic UI: message appears instantly with states pending (clock), sent, failed (retry)
- Messages persisted in a local database so history loads offline
- Cursor-based pagination loads older messages on scroll (50 per page)
- Auto-scroll to newest message; 'jump to latest' button when scrolled up
- Links are detected and tappable; emoji supported
- Each message has a unique client-generated ID for de-duplication

## User flow
1. User taps a contact
2. Types a message and taps send
3. Message shows pending then sent
4. Recipient's device receives it and shows it in real time

## Happy case
The user types and sends a message, sees it go from pending to sent, and the recipient receives it instantly.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The user is offline when sending | The message stays queued with a clock icon and sends automatically on reconnect |
| The send fails permanently | The bubble shows a red icon; tap offers Retry or Delete |
| The app is killed mid-send | Pending messages resume on next launch without duplicates |
| A message exceeds 4,096 characters | The send button is disabled and a counter explains the limit |

## Acceptance criteria
- [ ] Chat screen shows history, newest at bottom, with timestamps
- [ ] Sent message appears immediately and shows pending, sent or failed state
- [ ] Failed messages can be retried

## Edge cases & error handling
- Offline send: message queues locally and sends when online
- Send failure: show a red icon, tap to retry or delete
- Very long messages and messages with only emoji (render larger)
- Rapid sending of many messages preserves order
- App killed while sending: pending messages resume on relaunch

## Non-functional requirements
- Chat opens in under 300ms from local cache
- Scrolling stays at 60fps with 5,000 messages

## Technical notes (Suggestion)
- Local SQLite/Realm store, server timestamps for ordering, uses the realtime gateway.

## Testing notes
- Airplane mode send, kill app mid-send, two devices chatting, 5,000-message scroll performance.

## Out of scope
- Media, reactions, replies, receipts (separate issues).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
