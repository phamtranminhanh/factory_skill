# [027] Search chats and messages

| Field | Value |
|---|---|
| Area | Search |
| Priority | P2 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Let users search for messages and conversations quickly.

## User story
As a user, I want to find past messages.

## Functional requirements
- Search bar on the Chats tab; searches contact names, group names and message text
- Results grouped: Chats, Contacts, Messages with highlighted matches
- Tapping a message result opens the chat scrolled to that message
- In-chat search from the chat menu with next/previous match
- Search runs on the local database for instant results; case and accent insensitive
- Recent searches (clearable)

## User flow
1. Tap the search bar
2. Type a word
3. See results and tap one

## Acceptance criteria
- [ ] Search by contact name and message text
- [ ] Results open the chat at the matching message

## Edge cases & error handling
- No results: empty state
- Very large history: debounce input and paginate results
- Deleted messages must not appear
- With E2EE, search must run locally on decrypted text

## Non-functional requirements
- Results in under 300ms for 100k messages

## Technical notes (Suggestion)
- SQLite FTS5 index.

## Testing notes
- Accents, emoji, deleted messages, large datasets.

## Out of scope
- Server-side search, media search by content.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
