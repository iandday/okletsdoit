# Wedding Settings

The Settings page provides a centralized view of all configurable settings across the entire application.  Default data has been configured at first launch, now it's time to make it your own!

## Display Details
- **Wedding Date**: Date of the wedding. Shown on public pages and used for countdown displays.
- **Allow RSVP**: When enabled the public RSVP flow is visible to guests.


## RSVP Settings

These fields control the display for the begining and end of the RSVP process

- **RSVP Accept Button Text**: Text shown on the primary button guests click to accept (e.g. "Yes, attending").
- **RSVP Decline Button Text**: Text shown on the button guests click to decline (e.g. "Sorry, can't make it").
- **RSVP Accept Success Message**: Short confirmation message shown after a guest accepts.
- **RSVP Decline Success Message**: Short confirmation message shown after a guest declines.


## RSVP Accept Page Settings

These fields control the content of the multi‑step RSVP acceptance flow.

- **RSVP Attending Checkbox Label**: Label next to the attending checkbox (e.g. "Will you attend?").
- **RSVP Overnight Checkbox Label**: Label for overnight attendance or accommodation checkbox (e.g. "Will you stay with us?").
- **RSVP Accept Page Intro Paragraph**: Intro text shown at the start of the accept flow.
- **RSVP Accept Page Accommodation Intro Paragraph**: Paragraph shown if the guests are being offered accommodations.


## RSVP Yes/No Questions

Custom questions which appear as checkboxes in the RSVP acceptance flow. Each question contains the following data points:

- **Question**: The question text guests see (required).
- **Description**: Optional helper text shown beneath the question.
- **Required**: If enabled, guests must answer this question before submitting.
- **Order**: Integer used to sort questions; lower values appear first.
- **Published**: Toggle to show/hide the question in the RSVP acceptance flow.

Example:

- **Question**: `Will you attend the rehearsal dinner?`
- **Description**: `Optional: join us for the rehearsal dinner at 6pm`
- **Required**: `No`
- **Order**: `10`
- **Published**: `Yes`

## RSVP Input Questions

Free‑text questions collected during the RSVP acceptance flow. Each question contains the following data points:

- **Question**: The question text guests see (required).
- **Description**: Optional helper text shown beneath the question.
- **Required**: If enabled, guests must answer this question before submitting.
- **Order**: Integer used to sort questions; lower values appear first.
- **Published**: Toggle to show/hide the question in the RSVP acceptance flow.

Example:
- **Question**: `Do you have any dietary requirements?`
- **Required**: `No`
- **Order**: `20`
- **Published**: `Yes`

---


Tips for better responses

- **Use short, clear question text and button labels**: so guests understand actions quickly.
- **Mark only essential fields as Required**: to reduce submission friction.
- **For long intro paragraphs, preview formatting**: on the public RSVP page before finalizing.
