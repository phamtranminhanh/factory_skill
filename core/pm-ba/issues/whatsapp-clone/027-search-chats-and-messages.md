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

## User stories
**Who:** A user hunting for an address, file or past decision

**Primary story (happy case)**
> As a user, I want to type a word and see matching chats, contacts and messages instantly, so that I can find the address someone sent me last month.

**Additional stories**
- As a user, I want to tap a message result and land exactly on that message in the chat, so that I see the context.
- As a user inside one conversation, I want to search that chat only and jump between matches, so that I can find what we said.

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

## Happy case
The user types a word, sees matching results instantly, taps one and lands on that message.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| There are no results | An empty state with the query shown |
| Messages were deleted | They never appear in results |
| Search runs on a huge history | Input is debounced and results paginate without freezing |

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
