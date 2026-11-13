# WhatsApp-like Messaging App: Feature Backlog

## Assumptions
- Mobile app (iOS + Android) with a backend; no web client.
- MVP = P0 features; P1 follows; P2/P3 are enhancements.
- Out of scope: payments, business API, status/stories, channels, desktop app.

## Foundation
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 001 | [Set up project, repo and CI/CD](001-set-up-project-repo-and-ci-cd.md) | P0 | M | DevOps | none |
| 002 | [Build design system and app shell](002-build-design-system-and-app-shell.md) | P0 | M | Design | 001 |
| 003 | [Implement realtime messaging gateway](003-implement-realtime-messaging-gateway.md) | P0 | L | Backend | 001 |

## Accounts & Onboarding
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 004 | [Register with phone number and OTP](004-register-with-phone-number-and-otp.md) | P0 | M | Backend | 001 |
| 005 | [Set up profile (name, photo, about)](005-set-up-profile-name-photo-about.md) | P0 | S | Mobile | 004 |
| 006 | [Manage sessions and log out](006-manage-sessions-and-log-out.md) | P2 | S | Backend | 004 |

## Contacts
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 007 | [Sync phone contacts and find registered users](007-sync-phone-contacts-and-find-registered-users.md) | P0 | M | Mobile | 004 |
| 008 | [Block and unblock a contact](008-block-and-unblock-a-contact.md) | P1 | S | Backend | 007 |
| 009 | [Invite friends via share link](009-invite-friends-via-share-link.md) | P3 | S | Mobile | 007 |

## 1:1 Messaging
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 010 | [Send and receive text messages](010-send-and-receive-text-messages.md) | P0 | M | Mobile | 003, 005 |
| 011 | [Show chat list with last message and unread count](011-show-chat-list-with-last-message-and-unread-count.md) | P0 | M | Mobile | 010 |
| 012 | [Show delivery and read receipts](012-show-delivery-and-read-receipts.md) | P1 | M | Backend | 010 |
| 013 | [Show typing indicator and online/last seen](013-show-typing-indicator-and-online-last-seen.md) | P1 | S | Backend | 010 |
| 014 | [Reply to, delete and forward messages](014-reply-to-delete-and-forward-messages.md) | P1 | M | Mobile | 010 |
| 015 | [Send emoji reactions to messages](015-send-emoji-reactions-to-messages.md) | P2 | S | Mobile | 010 |

## Group Chat
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 016 | [Create a group and manage members](016-create-a-group-and-manage-members.md) | P0 | L | Backend | 010 |
| 017 | [Send messages in group chats](017-send-messages-in-group-chats.md) | P0 | M | Mobile | 016 |

## Media Sharing
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 018 | [Send photos and videos](018-send-photos-and-videos.md) | P0 | L | Mobile | 010 |
| 019 | [Send documents and files](019-send-documents-and-files.md) | P1 | M | Mobile | 010 |
| 020 | [Send voice messages](020-send-voice-messages.md) | P1 | M | Mobile | 010 |
| 021 | [Share location](021-share-location.md) | P2 | S | Mobile | 010 |

## Calls
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 022 | [Make and receive voice calls](022-make-and-receive-voice-calls.md) | P1 | L | Mobile | 003, 010 |
| 023 | [Make and receive video calls](023-make-and-receive-video-calls.md) | P2 | L | Mobile | 022 |
| 024 | [Show call history](024-show-call-history.md) | P2 | S | Mobile | 022 |

## Notifications
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 025 | [Receive push notifications for new messages](025-receive-push-notifications-for-new-messages.md) | P0 | M | Backend | 010 |
| 026 | [Mute chats and customise notification settings](026-mute-chats-and-customise-notification-settings.md) | P2 | S | Mobile | 025 |

## Search
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 027 | [Search chats and messages](027-search-chats-and-messages.md) | P2 | M | Mobile | 010 |

## Settings & Privacy
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 028 | [Configure privacy settings](028-configure-privacy-settings.md) | P1 | M | Backend | 005 |
| 029 | [Delete account](029-delete-account.md) | P2 | S | Backend | 004 |

## Security
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 030 | [Implement end-to-end encryption](030-implement-end-to-end-encryption.md) | P1 | L | Backend | 010 |

## Backup
| ID | Feature | Priority | Size | Role | Depends on |
|---|---|---|---|---|---|
| 031 | [Back up and restore chats](031-back-up-and-restore-chats.md) | P3 | L | Backend | 010 |

## Build order
1. **Foundation:** 001–003
2. **Core MVP (P0):** 004, 005, 007, 010, 011, 016, 017, 018, 025
3. **Enhancements (P1):** receipts, typing/presence, message actions, files, voice notes, voice calls, block, privacy, E2EE
4. **Nice-to-have (P2/P3):** reactions, location, video calls, call history, mute, search, delete account, invite, backup

## Counts
Total issues: 31. P0: 12, P1: 9, P2: 8, P3: 2.
Per area: Foundation: 3, Accounts & Onboarding: 3, Contacts: 3, 1:1 Messaging: 6, Group Chat: 2, Media Sharing: 4, Calls: 3, Notifications: 2, Search: 1, Settings & Privacy: 2, Security: 1, Backup: 1.
