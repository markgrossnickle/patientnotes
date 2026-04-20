# PatientNotes

HPI (History of Present Illness) note generation skill for cardiac electrophysiology patients.

## Structure

```
PatientNotes/
├── README.md
├── Abbreviations.txt          # Editable abbreviation list
└── .claude/
    └── skills/
        └── hpi-note/
            ├── SKILL.md       # Skill instructions
            └── references/
                ├── abbreviations.txt   # Abbreviations used by the skill
                └── hpi-structure.txt   # HPI template structure
```

## Usage

The skill generates a Brief HPI following a rigid template:

1. **Topic sentence** with 5 ordered slots: adjective-form comorbidities, non-cardiac/non-pulmonary PMH, pulmonary problems, general cardiology problems, and cardiac EP diagnoses with interventions/dates.
2. **EP timeline narrative** for complex histories (multiple ablations, evolving PVC burden, AF progression).
3. **Body** with CHA2DS2-VASc score, anticoagulant, drug failures/intolerances, last EP visit summary, interim events, and reason for visit.

Output is a single paragraph of plain text ready to paste into a medical record.

## Abbreviations

Edit `Abbreviations.txt` in the root to add new abbreviations. When updating, also update `.claude/skills/hpi-note/references/abbreviations.txt` to keep them in sync.
