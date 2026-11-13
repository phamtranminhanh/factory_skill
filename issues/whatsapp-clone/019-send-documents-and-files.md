# [019] Send documents and files

| Field | Value |
|---|---|
| Area | Media Sharing |
| Priority | P1 |
| Size | M |
| Suggested role | Mobile |
| Depends on | 010 |

## Overview
Allow sharing documents (PDF, Office files, archives) in chats.

## User story
As a user, I want to send files like PDFs.

## Functional requirements
- Attach menu > Document opens the system file picker
- Max file size 100 MB
- Bubble shows file icon, name, size and type; tap to download and open with a system viewer
- Upload/download progress with cancel
- Block executable file types (.exe, .apk, .bat)
- Downloaded files cached and removable from storage settings

## User flow
1. Tap + > Document
2. Pick a file
3. Send
4. Recipient taps to download and open

## Acceptance criteria
- [ ] File picker with a 100 MB limit
- [ ] File name, size and type icon shown in the bubble

## Edge cases & error handling
- File exceeds 100 MB: show limit
- Filename with special characters or very long names
- No app installed to open the type: offer 'Save to Files'
- Download interrupted: resume

## Non-functional requirements
- Virus scanning on the server (open question)
- Signed, expiring download URLs

## Technical notes (Suggestion)
- Reuse media upload service from the media issue.

## Testing notes
- Several file types and sizes, blocked types, interrupted download.

## Out of scope
- Cloud-drive pickers, document preview thumbnails.

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
