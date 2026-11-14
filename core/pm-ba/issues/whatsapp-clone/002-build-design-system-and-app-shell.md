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

## User stories
**Who:** Designers, mobile devs and every end user

**Primary story (happy case)**
> As a mobile developer building a new screen, I want a documented set of themed components (buttons, inputs, avatars, list items), so that I can assemble screens quickly and they look consistent with the rest of the app.

**Additional stories**
- As a user who uses dark mode at night, I want the app to follow my phone's theme automatically, so that it is comfortable on my eyes.
- As a user with low vision who sets a large system font, I want text to scale without being cut off, so that I can read every screen.

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

## Happy case
The user switches tabs, toggles dark mode or a larger font, and every screen renders consistently with no clipped or unreadable text.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| System font is set to 200% | No text is clipped; layouts scroll or wrap |
| Device uses a right-to-left language | Layout mirrors correctly |
| A tiny screen (360dp / iPhone SE) is used | All actions remain reachable without overlap |

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
