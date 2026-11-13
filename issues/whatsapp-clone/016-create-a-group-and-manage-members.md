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

## User stories
**Who:** A user organising a family, team or friend group

**Primary story (happy case)**
> As a user planning a trip, I want to create a group, name it, add a photo and select up to 255 contacts, so that all the participants can talk in one place.

**Additional stories**
- As a group admin, I want to add or remove members and make others admins, so that I can manage the group and hand it over when I leave.
- As a group member, I want to leave a group I no longer need, so that I stop receiving its messages.
- As an admin, I want to restrict who can edit group info or send messages, so that announcements are not buried.

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

## Happy case
The creator makes a group with a name and members, and the group appears for all members with admin tools available to admins.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The group reaches the member maximum (256) | 'Group is full' is shown and no one is added |
| The user adds someone who blocked them | The add is refused with a neutral message |
| The last admin leaves | The longest-serving member is promoted automatically |
| Group creation fails (network) | Nothing is half-created and the user can retry |

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
