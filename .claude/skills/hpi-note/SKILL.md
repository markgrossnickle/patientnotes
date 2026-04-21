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
it into the template.

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

## Critical: Infer from context, never leave placeholders

The user is a busy EP provider. They will paste clinical notes, not fill out a form. Your
job is to extract and synthesize everything you can from the provided material. Follow
these rules strictly:

- **Never use bracket placeholders** like [Name], [age], [drug], [indication], or
  [needs calculation] in the output. Either fill in the value from context or omit the
  element entirely.
- **Infer age when not stated explicitly.** CHA2DS2-VASc components reveal age range:
  1 point for age means 65-74, 2 points means >=75. Prior notes often state age directly.
  Use the most recent age mentioned in any provided note.
- **Calculate CHA2DS2-VASc yourself** from documented conditions. The components are:
  C (CHF, 1pt), H (HTN, 1pt), A2 (age >=75, 2pts), D (DM, 1pt), S2 (stroke/TIA/
  thromboembolism, 2pts), V (vascular disease e.g. CAD/MI/PAD, 1pt), A (age 65-74, 1pt),
  Sc (sex category female, 1pt). Add them up. If a prior note states a score, verify it
  against documented conditions and use the most complete calculation.
- **Identify the anticoagulant from medication lists or context.** Notes often mention
  "Eliquis" (apixaban), "Xarelto" (rivaroxaban), "warfarin", etc. in medication lists,
  orders, or plan sections. If the specific drug isn't named but anticoagulation is
  mentioned (e.g., "on DOAC", "on OAC"), write "a DOAC" rather than leaving a placeholder.
- **Synthesize the visit indication from clinical context.** If the user says "write a
  pre-procedure HPI for DCCV", the indication is DCCV. If notes discuss plans for ablation
  after cardioversion, the indication is "DCCV as bridge to ablation." If the context is
  a follow-up, use "f/u". Never leave the visit indication blank.
- **Extract symptoms from the notes.** If the note mentions the patient has fatigue, DOE,
  palpitations, exercise intolerance, etc., include the relevant symptoms parenthetically
  after the EP diagnosis in Slot #5 (e.g., "symptomatic (DOE, fatigue) longstanding
  persistent AF").
- **Use "me" for the provider name** when the note is clearly written by the user (first
  person language like "I discussed", "we agreed", "my impression").
- **When information is truly absent** (not inferable from any provided material), omit
  that element from the HPI. Do not ask the user to fill in missing fields unless the
  gap is critical to patient safety (e.g., completely unknown anticoagulation status
  before a procedure). A note flagging minor gaps at the end is fine, but the HPI
  itself must be complete and ready to paste.

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

## Handling "last seen" encounters

"Last seen" always refers to the most recent EP encounter, whether that was an office
visit, a hospital consult, or a procedure. Use whichever is most recent.

- If the user's own note is the most recent encounter, use "me" as the provider and
  the date of that note.
- If the most recent EP encounter was a procedure (not an office visit), reference the
  prior office visit as "last seen" for the A&P discussion context, then describe the
  procedure separately with its date and outcome. For example: "He was last seen by Dr. X
  on [office visit date]. At that visit, [discussion/plan]. On [procedure date], he underwent
  [procedure details]."
- Never skip past the user's own recent visit to reference an older visit from a
  different provider. If the user provides their own OV note from 4/7/26 and an older
  note from 9/21/23, the "last seen" is 4/7/26.

## Pre-procedure Brief HPI variant

When the user asks for a "pre-procedure H&P" or "pre-sedation HPI" (for DCCV, ablation,
loop recorder implant, device implant, etc.), produce a shorter, more focused version:

- The topic sentence follows the same slot structure (this stays complete -- do not
  abbreviate the topic sentence or omit PMH).
- The EP timeline can be abbreviated -- focus on what's directly relevant to the procedure
  being performed rather than the full chronological history.
- The body is trimmed: include CHA2DS2-VASc, anticoagulant, last visit (brief), and the
  procedure indication.
- **Exclude from pre-procedure notes:** device interrogation details (battery, lead
  parameters, pacing percentages), ECG findings (QRS, QTc, intervals), detailed visit
  summaries, and lengthy interim event narratives -- unless they directly affect the
  procedure (e.g., subtherapeutic INRs requiring TEE before DCCV, or amiodarone loading
  status for a post-load DCCV).
- The visit indication should state the specific procedure: "She presents today for DCCV"
  or "He presents today for TEE/DCCV" or "She presents today for loop recorder implant."
- If the DCCV is planned as a bridge to a future ablation, state that: "presents today
  for DCCV as bridge to ablation."
- If there's a specific clinical rationale for the procedure timing (e.g., completed
  3 weeks of anticoagulation, amiodarone loading complete), include it briefly.

## Output format

Output the HPI as a single paragraph of plain text. No headers, no bullet points, no
markdown formatting. It should be ready to paste directly into a medical record.

After outputting the HPI, ask if the user wants any changes.

## Learning from feedback

When the user corrects or adjusts an HPI you produced, treat that feedback as a rule
for all future notes in the conversation. Common types of feedback include:

- Moving a diagnosis to a different slot
- Changing how a condition is described or abbreviated
- Requesting more or less detail in a section
- Adjusting the structure (e.g., "cluster the AF/AFL info together toward the end")
- Adding or removing specific clinical details

Apply these corrections consistently to all subsequent HPIs without being asked again.
If the user says "keep X clustered together" or "don't include Y," that applies to every
future note in the session, not just the one being edited.

## Examples

Below are several examples covering different clinical scenarios. These demonstrate the
expected output quality, level of inference, and formatting.

### Example 1: Complex follow-up with multiple ablations and interim events

Mr. Imamovic is a 73 y.o. hypertensive, pre-diabetic male with PMHx significant for anxiety/panic, thyroid nodule, hyperaldosteronism, HLD, COPD, CHRF (3L nocturnal O2), OSA with concern for central component, PFO, mild CAD, HFrecEF/NICM (EF% 55-60%, grade III diastolic dysfunction per echo 2/2026), severe AS/AI with possible bicuspid valve s/p TAVR 8/2/23, and PVCs s/p ablation 8/2018 (LV perivalvular inferoseptum), PAF/AFL s/p initial ablation 5/2011 (CTI, PVI), s/p 2nd ablation 3/2012 (redo PVI [RIVP], LA roof, mitral annular flutter, focal AT), s/p 3rd ablation 5/2018 (re-do prior PV line, anterior roof, LA roof, posterior RIPV region, PWI, LoM), s/p dofetilide re-initiation 8/2024 (250 mcg q12h). Of note, dofetilide was stopped in 7/2018 and changed to mexiletine out of concern for dofetilide causing ventricular ectopy, although PVCs persisted on follow-up ZIO (26%) leading to ablation 8/2018. He had an admission for ?VT in 5/2024; however, ZIO at that time confirmed 2:1 atrial flutter with LBBB for which he was re-prescribed amiodarone. Although ablation was discussed, he was ultimately admitted for resumption of dofetilide in 8/2024, final dose 250 mcg q12h. CHA2DS2-VASc Score = 3 (age >65, HTN, CHF). He is anticoagulated with apixaban 5mg BID. He has failed multiple AADs with breakthrough (sotalol, dofetilide, amiodarone). He was last seen by Mallory Swirka, NP on 10/13/25. At that visit, he had no recurrent AF/AFL and no changes were made; plan was to continue dofetilide, carvedilol, and apixaban with f/u in 6 months. Since that visit, he presented to the ER on 1/4/26 for a seizure episode (tongue biting, urinary incontinence, CTA head/neck with MCA aneurysms but no active bleed, MRI negative for mass, discharged with neurology f/u, no antiepileptics started); was admitted 2/6-7/26 for acute dyspnea and diaphoresis with troponin leak (peak hs trop 120, EKG nonischemic, CTA chest negative for PE, echo with preserved systolic function and grade III diastolic dysfunction, felt to be demand ischemia in the setting of anemia, carvedilol increased to 25mg BID, eplerenone decreased to 25mg BID); returned to the ER on 2/15/26 for hypoxia to the 50s (improved with nebulizers, troponin negative x2, BNP mildly elevated, vascular congestion on CXR with trace LE edema, given low-dose Lasix, discharged with outpatient cardiology and pulmonology f/u); and was admitted to Swedish Hospital 4/1-2/26 for acute on chronic hypoxic and hypercapnic respiratory failure with recurrent apnea episodes concerning for central component related to cardiac disease and OSA (VBG improved on BiPAP, prescribed nightly CPAP, remained rate-controlled on telemetry on dofetilide/carvedilol/apixaban, no acute cardiac events). He presents today in f/u.

### Example 2: Simple pre-procedure DCCV (post-ablation blanking period)

Ms. ___ is a 70 y.o. hypertensive female with PMHx significant for hypothyroidism, breast cancer, CLL, asthma, moderate MR, HFpEF, and typical flutter s/p CTI ablation in 2018, symptomatic (DOE) peAF s/p catheter ablation (PVI, PWI via PFA, CTI redo via RFA) on 2/6/26. CHA2DS2-VASc Score = 4 (age, F, CHF, HTN). She is anticoagulated with apixaban (no missed doses in the last 3 weeks). She was last seen by me on 4/9/26. At that visit, she was noted to have recurrent AF documented on ECG (also on 3/24/26 ECG with Allison Fike), within the post-ablation blanking period. Symptoms (DOE) had improved post-ablation but recurred in recent weeks. AF is rate-controlled on metoprolol succinate 100mg daily. DCCV risks and benefits were discussed and she was agreeable to proceed. She presents today for DCCV.

### Example 3: Pre-procedure DCCV as bridge to ablation (longstanding persistent AF)

Mr. ___ is a 58 y.o. hypertensive male with PMHx significant for OSA on CPAP, HFrEF/dilated cardiomyopathy (EF% improved from 16% to 50-51%, NYHA class 2), LA enlargement, and symptomatic (fatigue, reduced exercise capacity) long-standing persistent AF (>20 years, onset following lightning strike in 2002 with subsequent tachycardia and EF% 16% in 2003) s/p catheter ablation (PFA PVI, PFA PWI, anterior "Y" mitral line for counterclockwise mitral annular flutter, focal ablation of AT from inferior vestibule of LA, focal ablation/SVC isolation for AT from septal SVC-RA junction) on 4/14/26, s/p DCCV 4/15/26 (200J unsuccessful, 360J with manual compression converted to NSR, reverted to AF with RVR). CHA2DS2-VASc Score = 2 (CHF, HTN). He is anticoagulated with apixaban. He was last seen on 4/15/26 at discharge following ablation and DCCV. At that time, he had reverted to AF with RVR post-DCCV; amiodarone was initiated (400mg BID x 7 days then 200mg BID) with plan to return for repeat DCCV after amiodarone loading. Rate control: carvedilol, digoxin 0.125mg daily. He presents today for repeat DCCV on amiodarone.

### Example 4: Simple post-ablation follow-up (minimal PMH)

Mr. ___ is a 59 y.o. hypertensive male with PMHx significant for moderate TR, and symptomatic PAF s/p catheter ablation (PFA PVI) on 2/24/26. CHA2DS2-VASc Score = 1 (HTN). He is anticoagulated with apixaban (started 3 weeks pre-procedure, planned for at least 3 months post-procedure). He is AAD naive. He was last seen by Dr. Matt Zipse on 9/22/25 for initial EP evaluation. At that visit, he presented with PAF increasing in both frequency and duration over the past year in the context of ~4 years of previously sporadic episodes, with symptoms of palpitations, exercise intolerance, and lightheadedness. AF episodes were tracked via Apple Watch beginning 12/2024; ZIO captured an 18 hr episode and episodes were possibly lasting up to 24 hrs. He elected to proceed with PFA catheter ablation. On 2/24/26, he underwent successful PFA PVI with entrance and exit block. Metoprolol was stopped post-procedure given sinus bradycardia. He presents today for f/u s/p PFA PVI.

### Example 5: Pre-procedure TEE/DCCV (complex congenital, bridge to ablation)

Ms. ___ is a 34 y.o. female with PMHx significant for Shone's syndrome with congenital aortic coarctation s/p repair via left subclavian flap (causing growth restriction of LUE) and subaortic membrane resection with myectomy 1991, s/p Kono aortoventriculoplasty 1993 c/b CHB due to enlargement of LVOT, s/p mechanical AVR and MVR 1998, HFrEF (LVEF 45% per echo 11/2022), Medtronic CRT-P in situ (s/p epicardial PPM at time of Kono procedure, transitioned to endocardial device 2006, c/b lead malfunction 10/2022 with RA lead no sensing/capture and noise on RV lead, s/p full system extraction and implant of CRT-P 10/10/2022), frequent PVCs (LRL increased to 70 bpm in 8/2023 with improvement), atypical AFL s/p ablation 9/2022, and persistent AF/AFL since 12/2025. CHA2DS2-VASc Score = 2 (CHF, F). She is anticoagulated with warfarin (goal INR 2.5-3.5 for mechanical valves), with subtherapeutic INRs noted. She was last seen by me on 4/7/26. Catheter ablation is planned for long-term rhythm control. She presents today for TEE/DCCV as bridge to ablation.
