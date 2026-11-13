# [002] Build design system and app shell

| Field | Value |
|---|---|
| Area | Foundation |
| Priority | P0 |
| Size | M |
| Suggested role | Design |
| Depends on | 001 |

## Overview
Build the reusable UI building blocks and the main navigation so every screen looks and behaves consistently. Designers deliver tokens and components; mobile devs implement them once.

## User story
As a user, I want a consistent look and navigation so that the app feels familiar.

## Functional requirements
- Design tokens: colors, typography scale, spacing, radius, elevation, for light and dark themes
- Components: button (primary/secondary/destructive), text input, avatar (with initials fallback), list item, badge, bottom sheet, toast, dialog, empty state, loading skeleton
- App shell with bottom tabs: Chats, Calls, Settings; header with title and actions
- Theme follows system setting and can be overridden in Settings
- Components documented in a component gallery screen or Storybook

## User flow
1. User opens the app and sees the tab bar
2. User switches tabs and the selected tab keeps its scroll position
3. User switches the device to dark mode and the app updates instantly

## Acceptance criteria
- [ ] Tabs for Chats, Calls, Settings exist
- [ ] Light and dark themes supported
- [ ] Shared components (button, input, avatar, list item) documented

## Edge cases & error handling
- Large system font sizes must not break layouts (support up to 200%)
- Right-to-left languages must mirror layouts
- Small screens (iPhone SE, 360dp Android) must not clip content

## Non-functional requirements
- Contrast ratio at least 4.5:1 for text
- Touch targets at least 44x44pt
- Screen-reader labels on all interactive components

## Technical notes (Suggestion)
- Figma library as source of truth; theme provider in code; icons as an SVG set.

## Testing notes
- Visual check of each component in light/dark and at 100%/200% font scale on iOS and Android.

## Out of scope
- Individual feature screens (covered by their own issues).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
