# [018] Send photos and videos

| Field | Value |
|---|---|
| Area | Media Sharing |
| Priority | P0 |
| Size | L |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Let users share photos and videos in chats, with preview, compression and progress feedback.

## User stories
**Who:** A user sharing holiday photos or a short video clip

**Primary story (happy case)**
> As a user, I want to pick up to 30 photos or videos from my gallery or camera, add a caption and send them, so that my friends can see what I saw.

**Additional stories**
- As a user on a slow connection, I want to see upload progress and cancel or resume it, so that a large video does not waste my data.
- As a recipient, I want to tap a blurred thumbnail to download and open the media full screen and save it to my gallery, so that I control my data use.
- As a user on mobile data, I want media to auto-download only on Wi-Fi, so that I do not burn through my data plan.

## Functional requirements
- Attach menu > Camera / Gallery, multi-select up to 30 items
- Preview screen with optional caption per item, crop/rotate for photos
- Photos compressed to max 1600px longest side; videos trimmed up to 3 minutes and transcoded to H.264 720p
- Upload with progress ring and cancel; resumable uploads for large files
- Recipient sees a blurred thumbnail and downloads the full file on tap (auto-download on Wi-Fi setting)
- Full-screen viewer with swipe between items, pinch to zoom, save to gallery
- Files stored in object storage with signed URLs and access limited to chat members

## User flow
1. Tap + > Gallery
2. Select photos
3. Add a caption and send
4. Recipient taps the thumbnail to view

## Happy case
The user selects media, adds a caption, sends, sees upload progress finish, and the recipient views it full screen.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| Camera or gallery permission is denied | An explanation with a link to settings |
| The file is too large or an unsupported format | Rejected before upload with a clear message |
| The upload is interrupted | Retry resumes from where it stopped |
| Device storage is low | The user is warned and the download is not started |

## Acceptance criteria
- [ ] Pick from gallery or camera, with preview and caption
- [ ] Media is compressed and uploaded with a progress indicator
- [ ] Recipient sees thumbnail and downloads full media on tap

## Edge cases & error handling
- Upload fails mid-way: retry resumes
- Permission denied for camera/photos
- File over size limit (16 MB photo / 64 MB video): clear error
- Unsupported format
- Low storage on device
- Cancel during upload removes the message

## Non-functional requirements
- Thumbnails visible in under 1s after send
- Media is not accessible by guessable URLs
- Respect data-saver mode

## Technical notes (Suggestion)
- Presigned multipart upload to S3-compatible storage; thumbnails generated client-side (blurhash).

## Testing notes
- Slow network, large videos, multi-select, permission flows, view and save on the receiving device.

## Out of scope
- Stickers/GIFs, view-once media, E2EE of media (covered in encryption issue).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
