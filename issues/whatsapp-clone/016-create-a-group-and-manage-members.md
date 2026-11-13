# [016] Create a group and manage members

| Field | Value |
|---|---|
| Area | Group Chat |
| Priority | P0 |
| Size | L |
| Suggested role | Backend |
| Depends on | 010 |

## Overview
Let users create group conversations and manage who is in them, with admin roles.

## User story
As a user, I want to create groups so that I can talk to many people.

## Functional requirements
- Create a group: name (max 25 chars), optional photo and description, select 1–255 members
- Creator is the first admin; admins can add/remove members, promote/demote admins, edit group info
- Any member can leave; if the last admin leaves, the oldest member becomes admin
- System messages in the chat for 'X added Y', 'Z left', 'name changed'
- Group info screen lists members with roles
- Invite link to join the group (optional P2)
- Setting: only admins can edit info / send messages

## User flow
1. New group > select contacts
2. Set name and photo
3. Group is created and appears in the chat list

## Acceptance criteria
- [ ] Create group with name, photo and up to 256 members
- [ ] Admins can add and remove members and promote other admins
- [ ] Members can leave the group

## Edge cases & error handling
- Maximum members reached: show 'Group is full'
- Adding a user who blocked the admin: not allowed
- Removed member keeps old history but cannot see new messages
- Duplicate group names are allowed

## Non-functional requirements
- Group creation completes in under 2s
- Membership changes propagate to all members in under 2s

## Technical notes (Suggestion)
- `groups`, `group_members(role)` tables; membership checked by the gateway on every message.

## Testing notes
- Create with 2 and 256 members, role changes, leave as last admin, removed member behaviour.

## Out of scope
- Group messaging UI (separate issue), communities.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
