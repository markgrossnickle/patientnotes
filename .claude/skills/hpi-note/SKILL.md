---
name: hpi-note
description: >
  Generate a cardiac electrophysiology (EP) HPI (History of Present Illness) note
  following a specific template structure. Use this skill whenever the user wants to
  write an HPI, draft a patient note, create a clinic note, write up a patient encounter,
  or anything involving "HPI", "history of present illness", "patient note", "clinic note",
  or "EP note". Also trigger when the user provides patient details and wants them formatted
  into a note, or asks to "write up" a patient. If patient information is mentioned alongside
  any request for a note or documentation, use this skill.
---

# HPI Note Generator

This skill produces a Brief HPI (History of Present Illness) for cardiac electrophysiology
patients. The output follows a rigid structure that the provider uses consistently across
all patient encounters. Deviating from this structure makes the note less useful clinically,
so precision matters here.

## Before you start

Read both reference files:

1. `references/hpi-structure.txt` -- the full template with instructions and an example
2. `references/abbreviations.txt` -- mandatory abbreviations to use throughout the note

## Gathering patient information

Accept patient information in any format (free text, bullet points, a pasted prior note,
dictation, prior visit notes, procedure summaries, ZIO/monitor results, etc.) and reorganize
it into the template. If information is missing for a section, skip that section rather than
inventing details. If something is ambiguous, ask.

Information needed:

- Patient name, age, sex
- Medical history (the user may provide this as a list, and you need to sort it into the
  correct instruction slots -- see below)
- Cardiac EP diagnoses and any interventions with dates
- CHA2DS2-VASc score components (if applicable -- this applies to patients with atrial
  fibrillation or atrial flutter)
- Current anticoagulant (if applicable)
- EP drug history (failures, intolerances, current medications)
- Last EP visit: provider name, date, and what was discussed/decided
- Interim events since last visit (hospitalizations, ER visits, patient calls that changed
  management, diagnostic results like ZIO monitors or stress tests)
- Reason for today's visit
- Any pending requests from other EP providers (e.g., messages requesting specific follow-up
  actions -- incorporate these into the visit indication)

## Important rules for sorting medical history

- **Only personal medical history goes in the topic sentence slots.** Family history (e.g.,
  father with HCM) does not belong in the topic sentence. By the time patients are seen in
  EP clinic, they are already established and any diagnostics pertaining to family history
  are in the works. Family history is addressed in the A&P if relevant, not the HPI.
- **Diagnostic results belong in the timeline, not the topic sentence.** When ZIO, stress
  test, echo, or other diagnostic results are provided, weave them into the EP timeline
  narrative or the "since that visit" section, depending on when they occurred.
- **Contextualize diagnostics with treatment.** When a diagnostic result occurred after
  starting a new medication or post-procedure, note the temporal relationship so the reader
  can interpret the result in context (e.g., "ZIO (4/7/26, approximately 3.5 weeks after
  dronedarone initiation) showed...").
- **Bleeding history relevant to anticoagulation decisions** should be included in the body
  after the anticoagulant line, since it directly informs EP management (e.g., LAAO
  consideration).
- **When multiple prior notes give different CHA2DS2-VASc scores**, use the most complete
  calculation. Verify by checking the components against the patient's documented history.

## Writing the HPI

The HPI is a single paragraph. It has two parts: a topic sentence and a body.

### Topic sentence

The topic sentence follows this exact formula:

```
[Name] is a [age] y.o. [#1] [male/female] with PMHx significant for [#2], [#3], [#4], [#5]
```

Fill each slot as follows:

**Slot #1 -- Adjective-form comorbidities.** Convert conditions into adjective form,
comma-separated. "Hypertension" becomes "hypertensive". "Type 2 diabetes" becomes
"type 2 diabetic". "Obesity" becomes "obese". Only include conditions that have a natural
adjective form.

**Slot #2 -- Non-cardiac, non-pulmonary PMH relevant to EP.** Things like hypothyroidism,
alcohol use disorder, tobacco abuse, cancer, CKD, DVT, PE, hematologic problems. If the
patient has none, omit this slot.

**Slot #3 -- Pulmonary problems.** OSA, COPD, PH, asthma, CHRF. If the patient has none,
omit this slot.

**Slot #4 -- General cardiology problems (not EP).** CAD, HFpEF, HFrEF, HFimpEF, HFrecEF,
AS, VHD, ICM, NICM, infiltrative cardiomyopathy, sarcoidosis, amyloidosis, HOCM, HCM.
If the patient has none, omit this slot.

**Slot #5 -- Cardiac EP diagnoses.** This is the most detailed slot. List all EP diagnoses
comma-separated. Whenever a diagnosis was treated with a procedure, follow it with "s/p"
and the intervention details including the date. For example:
"PAF/typical flutter s/p catheter ablation (PFA PVI, CTI RFA) on 3/15/25"

The ordering of slots is strict: #1 through #5, in that order. If a slot is empty, skip it
and move to the next. Do not rearrange.

### EP timeline narrative

For patients with a complex EP history (e.g., multiple ablations, evolving PVC burden,
progression from paroxysmal to persistent AF), include a brief chronological narrative
after the topic sentence and before the CHA2DS2-VASc line. This covers the trajectory of
the EP problem(s) with key data points: monitor results with burden percentages, EF
trends, medication trials and dose changes, and how the disease evolved over time. Keep
it factual and concise -- this is a timeline, not an interpretation.

### Body

After the topic sentence, continue the paragraph with:

1. **CHA2DS2-VASc score** (if applicable): "CHA2DS2-VASc Score = X (list components)."
2. **Anticoagulant** (if applicable): "He/She is anticoagulated with [drug]."
3. **EP drug failures or intolerances** (if any).
4. **Last EP visit**: "He/She was last seen by [provider] on [date]."
5. **Summary of last visit**: "At that visit, [brief summary of the A&P]."
6. **Interim events** (if any): "Since that visit, [hospitalizations, ER visits, or patient
   calls that changed management]." Keep this to 1-3 sentences.
7. **Reason for today's visit**: "He/She presents today for [indication]."

If a body element does not apply (e.g., no CHA2DS2-VASc for a patient without AF/AFL),
skip it.

## Abbreviation rules

Always use the abbreviations from `references/abbreviations.txt`. When a term appears in
the note, use the abbreviated form, not the spelled-out version. For example, write "HTN"
not "hypertension" within the PMH list, write "s/p" not "status post", write "PAF" not
"paroxysmal atrial fibrillation".

The one exception: in Slot #1 (adjective-form comorbidities), use the adjective word form
(e.g., "hypertensive") since these are descriptors, not diagnoses.

## Handling procedures as the "last seen" encounter

When the most recent EP encounter was a procedure (not an office visit), reference the
prior office visit as "last seen" for the A&P discussion context, then describe the
procedure separately with its date and outcome. For example: "He was last seen by Dr. X
on [office visit date]. At that visit, [discussion/plan]. On [procedure date], he underwent
[procedure details]."

## Output format

Output the HPI as a single paragraph of plain text. No headers, no bullet points, no
markdown formatting. It should be ready to paste directly into a medical record.

After outputting the HPI, ask if the user wants any changes.

## Example

Here is a complete example of a correctly formatted HPI:

Ms. XXX is a 78 y.o. hypertensive female with PMHx significant for DVT, MR/TR, HFpEF, and mildly symptomatic (palps) persistent A-fib associated with severe LAE s/p bioMVR/TV repair/Cox/Maze/LAAL on 10/10/25 w/ post-operative course c/b SSS/slow atypical atrial flutter with high grade AV block s/p DCCV and Abbott CRT-P w/ RA and CS leads on 10/16/25. CHA2DS2-VASc Score = 5 (CHF, HTN, agex2, F). She is anticoagulated with warfarin. She was last seen by me on 12/12/25. At that visit, she was noted to have been in AF dating-back to at least device placement on 10/16/25. She'd been on amiodarone for 3 days prior to the 10/16/25 DCCV and had ERAF. At that visit, we'd explored the possibility of pursuing repeat DCCV on fully loaded amiodarone once INR stabilized. Amiodarone was resumed by NP Fevold for Afib with tentative plan to cardiovert if A-fib persisted after a month, but DCCV was ultimately deferred and amiodarone was continued at dose reduction (200 QD) per last OV note (3/12/26). She presents today in f/u.
