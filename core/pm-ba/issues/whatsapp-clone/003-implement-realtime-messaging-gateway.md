# [003] Implement realtime messaging gateway

| Field | Value |
|---|---|
| Area | Foundation |
| Priority | P0 |
| Size | L |
| Suggested role | Backend |
| Depends on | 001 |

## Overview
Provide the server-side realtime channel that carries messages, receipts, typing and presence events between devices. This is the technical heart of the product and must be reliable under reconnects and flaky networks.

## User stories
**Who:** Backend engineers; indirectly every user who chats

**Primary story (happy case)**
> As a user chatting with a friend, I want my message to reach their phone in under a second when they are online, so that the conversation feels live like a call.

**Additional stories**
- As a user who loses signal in an elevator, I want the app to reconnect by itself and deliver anything I missed in the right order, so that I never lose or duplicate a message.
- As an on-call engineer, I want to add or restart a server without dropping users' conversations, so that we can deploy during the day.

## Functional requirements
- Authenticated WebSocket endpoint; connection requires a valid session token
- Client auto-reconnects with exponential backoff (1s, 2s, 4s up to 30s) and resumes from the last received event ID
- Server routes a message to all connected devices of the recipient
- Messages for offline recipients are stored in a queue and delivered on reconnect, in order
- At-least-once delivery with client-side de-duplication by message ID
- Heartbeat ping every 30s; dead connections are closed after 60s
- Horizontal scaling: any server instance can deliver to any user (pub/sub between instances)

## User flow
1. App opens and establishes a socket
2. Server acknowledges and sends any queued events
3. Sender emits a message; server persists it, acks to the sender, and pushes it to the recipient

## Happy case
Two online users exchange messages and each arrives on the other device in under 1 second, in order, with no duplicates.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The user's connection drops mid-conversation | The app reconnects with backoff and delivers missed messages in order, without duplicates |
| The access token expires while connected | The socket closes with a clear code, the app refreshes the token and reconnects |
| A server node is killed | Clients reconnect to another node and no messages are lost |

## Acceptance criteria
- [ ] Authenticated WebSocket connection with auto-reconnect
- [ ] Server delivers a message to an online recipient in under 1s (p95)
- [ ] Messages for offline users are queued and delivered on reconnect

## Edge cases & error handling
- Recipient on 2 devices: both receive the message
- Connection drops mid-send: client retries with the same message ID and no duplicate appears
- Clock skew: ordering uses server timestamps and sequence numbers
- Token expiry during a connection: server closes with a clear code and client refreshes the token

## Non-functional requirements
- p95 delivery latency under 1s for online recipients
- Supports 10,000 concurrent connections per node (load-tested)
- TLS everywhere

## Technical notes (Suggestion)
- WebSocket with a message broker (Redis pub/sub or NATS) and a durable store (PostgreSQL) for queues.

## Testing notes
- Load test, kill a server node mid-conversation, toggle airplane mode, send 1,000 messages in order and verify no loss or duplicates.

## Out of scope
- Message UI, encryption (see issue on E2EE), push notifications.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
