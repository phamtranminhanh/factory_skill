# [004] Register with phone number and OTP

| Field | Value |
|---|---|
| Area | Accounts & Onboarding |
| Priority | P0 |
| Size | M |
| Suggested role | Backend |
| Depends on | 001 |

## Overview
Let a new user create an account using only their phone number, verified by an SMS one-time password (OTP). The phone number is the user's identity.

## User stories
**Who:** A first-time user who owns a smartphone and no account yet

**Primary story (happy case)**
> As a new user who has just installed the app, I want to sign up using only my mobile number and a 6-digit SMS code, so that I can start chatting in under a minute without remembering a password.

**Additional stories**
- As a returning user on a new phone, I want to enter my number and code to get back into my existing account, so that I keep my contacts and identity.
- As a user whose SMS is slow, I want to request a new code after a 60-second countdown, so that I am not stuck on the verification screen.
- As the product owner, I want OTP requests rate-limited per number and per IP, so that attackers cannot run up our SMS bill.

## Functional requirements
- Screen to choose country code and enter phone number, validated against E.164 format
- Send a 6-digit OTP by SMS; OTP expires after 5 minutes
- Max 3 OTP requests per number per hour and 5 wrong attempts before a 15-minute lockout
- Resend button enabled after 60s countdown
- On success, create the user if new, or sign in if existing, and issue an access token and refresh token
- Store only the hashed OTP; log attempts for abuse detection
- Show terms of service and privacy policy link before verification

## User flow
1. User opens the app for the first time
2. Enters country and number, taps Next
3. Receives SMS and enters the code
4. Account is created and the user continues to profile setup

## Happy case
The user enters a valid number, receives the SMS within 30 seconds, enters the correct code and lands on profile setup, signed in.

(Steps: see User flow above.)

## Unhappy cases
| Situation | Expected behaviour |
|---|---|
| User enters a wrong code | 'Incorrect code' appears with attempts left; after 5 failures the user is locked out for 15 minutes |
| The code expires after 5 minutes | The user is told it expired and can request a new one |
| An invalid or too-short number is entered | Inline error appears and no SMS is sent |
| The SMS never arrives | Resend is enabled after 60s; limited to 3 per hour with a clear message |

## Acceptance criteria
- [ ] User enters number and receives a 6-digit SMS code
- [ ] Correct code creates the account and a session
- [ ] Wrong or expired code (5 min) is rejected; resend limited to 3 per hour

## Edge cases & error handling
- Wrong code: show 'Incorrect code' and remaining attempts
- Expired code: offer resend
- SMS not received: resend, or call-me voice fallback (P2)
- Number already registered on another phone: sign in and revoke the old session after notice
- No network: show retry state

## Non-functional requirements
- OTP SMS delivered in under 30s for 95% of sends
- Rate limiting per IP and per number to prevent SMS pumping fraud
- GDPR: consent recorded with timestamp

## Technical notes (Suggestion)
- SMS provider such as Twilio Verify; JWT access tokens (15 min) with rotating refresh tokens.

## Testing notes
- Valid and invalid numbers in several countries, expired/wrong/reused codes, rate-limit lockout, resend timing.

## Out of scope
- Email login, social login, profile setup (separate issue).

## Definition of done
- [ ] Code reviewed and merged, tests passing, acceptance criteria verified on iOS and Android, docs/API spec updated.
