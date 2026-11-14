# [012] Show delivery and read receipts

| Field | Value |
|---|---|
| Area | 1:1 Messaging |
| Priority | P1 |
| Size | M |
| Suggested role | Backend |
| Depends on | 010 |

## Overview
Show senders the status of each message: sent, delivered and read, via tick icons.

## User stories
**Who:** A sender waiting for a reply to something time-sensitive

**Primary story (happy case)**
> As a sender, I want ticks that show whether my message was sent, delivered to their phone, or read, so that I know if my friend has seen my message about meeting at 6 pm.

**Additional stories**
- As a privacy-minded user, I want to turn off read receipts, so that people cannot see exactly when I read their messages.
- As a user, I want a Message info screen with exact delivered/read times, so that I can confirm when something was received.

## Functional requirements
- One grey tick = server received; two grey ticks = delivered to recipient's device; two blue ticks = read
- Delivery receipt is sent by the recipient's app on receipt; read receipt when the message is visible in an open chat
- Receipts propagate through the realtime gateway and persist
- If either user disables read receipts, blue ticks are not shown (but delivered ticks still are)
- Long-press a message to see 'Message info' with delivered/read timestamps

## User flow
1. Sender sends; one tick
2. Recipient's phone receives; two ticks
3. Recipient opens the chat; ticks turn blue

## Happy case
The sender sees one tick when sent, two when delivered, and blue ticks when the recipient reads the message.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| The recipient is offline | The sender stays at one tick until delivery |
| Read receipts are turned off by either user | Blue ticks never appear; delivered ticks still do |
| Receipt events arrive out of order | The status never moves backwards |

## Acceptance criteria
- [ ] One tick = sent, two = delivered, blue two = read
- [ ] Read receipts can be turned off in privacy settings (see Privacy issue)

## Edge cases & error handling
- Recipient offline: stays at one tick
- Messages read in a batch: send a single read receipt for the latest message ID
- Group chats: handled in the group messaging issue

## Non-functional requirements
- Receipt updates reach the sender in under 1s when online

## Technical notes (Suggestion)
- Receipt events `delivered`/`read` carrying message ID ranges.

## Testing notes
- Online and offline recipient, read receipts on/off, multiple devices.

## Out of scope
- Group read-by list.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
