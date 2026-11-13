# [030] Implement end-to-end encryption

| Field | Value |
|---|---|
| Area | Security |
| Priority | P1 |
| Size | L |
| Suggested role | Backend |
| Depends on | 010 |

## Overview
Encrypt messages end to end so only the sender and recipients can read them, not even the server.

## User story
As a user, I want my messages private so that only recipients can read them.

## Functional requirements
- Each device generates identity and pre-keys on registration; public keys uploaded to the server
- 1:1 chats use the Signal protocol (X3DH + Double Ratchet); groups use sender keys
- Message bodies and media are encrypted client-side before upload; server stores ciphertext only
- Safety number / QR code to verify a contact's identity
- Warning in chat when a contact's keys change
- Chat banner 'Messages are end-to-end encrypted'
- Key backup is covered in the backup issue

## User flow
1. User sends a message
2. App encrypts it per recipient device
3. Server relays ciphertext
4. Recipient app decrypts and displays it

## Acceptance criteria
- [ ] Messages are encrypted on-device and server stores only ciphertext
- [ ] Safety number can be verified between two users
- [ ] Key change shows a warning in the chat

## Edge cases & error handling
- New device: sessions are re-established
- Recipient offline for long periods: one-time pre-keys run out, fall back to the last-resort key
- Lost keys after reinstall: messages cannot be decrypted, show a notice
- Server-side features such as search and link previews must work on the client

## Non-functional requirements
- Encryption overhead under 50ms per message
- Use a vetted library; independent security review before launch

## Technical notes (Suggestion)
- libsignal; keys stored in the secure enclave / Android Keystore.

## Testing notes
- Man-in-the-middle test, key change warning, multi-device, group member add/remove rekeying.

## Out of scope
- Metadata protection, disappearing messages.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
