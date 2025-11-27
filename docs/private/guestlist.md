# Guestlist

This page explains how the guestlist data shown in the site works and what each item means. It is written for site administrators and event organisers who manage invites and view guest responses.

## Overview
- Guest groups represent invited parties (households, couples, families).
- Guests are the individual people within a group.
- An RSVP Submission records a group's response when someone completes the RSVP flow.
- Answers to custom RSVP questions are saved alongside each submission so you can review and report on them.

Use this guide to understand what you’re seeing in the admin UI and how guest responses are stored.

---

## Guest Group (Party)
What it represents
- A single invitation unit — for example "The Smith Family" or "John & Jane".
- Holds contact info (address, email, phone), an RSVP code, and general notes about the party.

What you will see / use
- Name — the display name for the invite.
- RSVP code — unique code you can give to guests for quick access to their invite.
- Counts — quick totals for the group (number of members, how many are attending, how many declined, overnight needs, VIPs).

When to edit
- Update contact details if a group’s address or email changes.
- Use notes to record phone calls or special arrangements.
- If guests need to be re-assigned, edit the members listed under the group.

Practical tip: Give each group their RSVP code in the invite email so they can open their group’s RSVP form quickly.

---

## Guest (Individual)
What it represents
- A person who is part of a Guest Group.

Typical fields you’ll use
- First / Last name — used on name lists and printed materials.
- Invited — whether this person was formally invited.
- Responded / Attending — whether they completed the RSVP and their attendance decision.
- Overnight / VIP flags — capture accommodation needs or VIP status.
- Notes — any special details about the guest.

How it behaves
- Marking a guest as attending updates the group’s attendance counters.
- You can mark plus‑ones, special dietary needs or other details on the guest record.

Practical tip: Keep names accurate for placecards and catering counts.

---

## RSVP Submission (What happens when a guest responds)
What it represents
- A single recorded response for a Guest Group. It captures the time of submission and any top‑level notes.

What is stored
- Timestamp — when the RSVP was submitted.
- Top‑level choices — the group’s accept/decline decision and any global notes.
- Associated answers — each custom question answer (boolean or text) is saved with the submission.

How to use it
- Open the latest submission to see what the group answered and when.
- Use the submission to reconcile counts (attending/declined) and accommodation requests.

Practical tip: If a guest contacts you to change their response, check the latest submission to confirm and edit guest records if needed.

---

## Custom RSVP Questions and Answers
There are two question types used in the RSVP flow:

1. Boolean questions (Yes/No)
   - Examples: "Will you attend the rehearsal dinner?", "Do you need a shuttle?"
   - Stored as discrete Yes/No answers tied to the submission.

2. Input questions (Free text / specific)
   - Examples: "Dietary requirements", "Guest email"
   - Stored as short text answers.

What you’ll see
- The question label and any helper text along with each saved answer in the submission view.
- Which questions were marked as required — required questions must be answered before submitting.

Why answers are stored this way
- Every submission contains the answers given at that time so you can track what was provided even if the question text later changes.

Practical tip: Use boolean questions for quick choices and input questions for details like dietary notes or contact emails.

---

## Best practices
- Keep question text short and clear — guests skim forms.
- Only make essential questions required to reduce friction.
- Use the Order value (where available) to present the most important questions first.
- Use guest notes for manual follow‑ups that don’t belong in structured answers.

---


