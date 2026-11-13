# [011] Show chat list with last message and unread count

| Field | Value |
|---|---|
| Area | 1:1 Messaging |
| Priority | P0 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
The home screen of the app: a list of all conversations sorted by latest activity, with previews and unread counts.

## User story
As a user, I want an inbox so that I can jump into conversations.

## Functional requirements
- Row shows avatar, name, last message preview (1 line), time (today HH:mm, yesterday, date), unread badge
- Sorted by most recent activity; pinned chats stay on top (up to 3)
- Unread badge counts messages not yet seen; app icon badge shows the total
- Swipe actions: archive, mute, delete chat
- Opening a chat clears its unread count and syncs across devices
- Empty state with a 'Start chatting' call to action
- Preview shows icons for media (e.g. 'Photo', 'Voice message')

## User flow
1. App opens on Chats tab
2. User sees conversations
3. Taps one to open it; unread badge disappears

## Acceptance criteria
- [ ] Chats sorted by latest activity
- [ ] Each row shows avatar, name, last message preview, time, unread badge
- [ ] Opening a chat clears its unread count

## Edge cases & error handling
- Hundreds of chats: virtualised list
- New message arrives while on the list: row moves to top with animation
- Deleted last message: preview updates
- Muted chats show a muted icon and a grey badge

## Non-functional requirements
- List renders in under 500ms on cold start from cache

## Technical notes (Suggestion)
- Query from local DB sorted by `last_message_at`; badge counts via an unread counter per chat.

## Testing notes
- Receive messages while on the list, pin/mute/archive, unread count sync across two devices.

## Out of scope
- Search (separate issue), chat folders.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
