# [005] Set up profile (name, photo, about)

| Field | Value |
|---|---|
| Area | Accounts & Onboarding |
| Priority | P0 |
| Size | S |
| Suggested role | Mobile |
| Depends on | 004 |

## Overview
After registration, the user sets how others see them: a display name, optional profile photo and an 'about' line.

## User stories
**Who:** A newly registered user who wants friends to recognise them

**Primary story (happy case)**
> As a new user, I want to enter my name and optionally add a profile photo from my camera or gallery, so that friends who have my number see who I am before they reply.

**Additional stories**
- As a user, I want to write a short 'About' line (up to 139 characters), so that I can tell contacts if I am busy or at work.
- As a user who changes their look, I want to update my photo and name any time from Settings, so that contacts always see my current profile.

## Functional requirements
- Display name: required, 1–25 characters
- About: optional, up to 139 characters, default 'Hey there! I am using this app'
- Photo: take with camera or pick from gallery, crop to square, store resized versions (256px and 640px)
- Edit profile later from Settings
- Profile changes sync to contacts within seconds
- Permission prompts for camera and photo library explain why access is needed

## User flow
1. After OTP the user lands on 'Set up profile'
2. Enters name and optionally adds a photo
3. Taps Done and enters the chats screen

## Happy case
The user enters a valid name, adds a photo and optional about line, taps Done, and contacts see the updated profile.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Name is empty or only spaces | Done stays disabled with an inline message |
| Photo is over 10 MB or an unsupported type | Upload is rejected with a clear reason; the old photo remains |
| Camera or gallery permission is denied | A message explains and the user can skip the photo |
| Upload fails due to network | User can retry; profile is saved without photo meanwhile |

## Acceptance criteria
- [ ] Display name is required, photo and about are optional
- [ ] Photo can be taken or chosen from gallery and is cropped to a square
- [ ] Profile changes are visible to contacts

## Edge cases & error handling
- Camera/gallery permission denied: show a message and allow skipping
- Unsupported or huge image: reject over 10 MB with a clear message
- Emoji and non-Latin names must display correctly
- Name with only spaces is invalid

## Non-functional requirements
- Image upload under 3s on 4G
- Photos served via CDN with signed URLs
- Profanity filtering optional (open question)

## Technical notes (Suggestion)
- Object storage (S3-compatible) with image resizing on upload.

## Testing notes
- Name length boundaries, photo from camera and gallery, permission denied path, profile visible on a second device.

## Out of scope
- Privacy controls over who can see the photo (see privacy settings issue).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
