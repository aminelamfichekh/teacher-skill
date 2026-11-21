# Durable learning record

## File contract

Use portable UTF-8 files under the selected StudyVault. Preserve existing notes,
paths, dashboards, and user edits; add the learning layer alongside them.

```text
StudyVault/
  00-Dashboard/                 human-readable views, not primary evidence
  sources/manifest.json         ordered source registry and provenance
  sources/<source-id>/          original transcript, cues/chunks/index JSON
  learning/PROFILE.md           confirmed preferences, goals; unknowns/proposals
  learning/COURSE.md            objectives, prerequisites, rubric, lesson/watch map
  learning/STATE.json           compact current position and progress pointers
  learning/events.jsonl         append-only evidence events
  learning/sessions/<id>.md     checkpoints and actionable next steps
  concepts/                    concept evidence and misconception notes
  tools/                       activities and artifacts, created only as needed
```

## State schema

`STATE.json` has `schema_version: 1`, stable `course_id`, integer `revision`,
`updated_at` (ISO datetime with zone), nullable `last_event_id`, nullable
`last_session` (vault-relative path), and `current` containing nullable `lesson_id`,
`source_id`, `position_seconds`. `next_action` is a string or null.
`objectives` is keyed by objective ID, each containing `status`, `evidence_ids`,
nullable `next_review_at`, and `review_rationale`. Status is `not_started`,
`learning`, `practicing`, `demonstrated`, `retained`, or `needs_review`.
`learner_watch_ranges` is keyed by source ID with learner-reported intervals and
event IDs. Teaching a segment does not imply the learner watched it.

### Resuming an unfinished lesson

For active lessons add optional fields inside `current` (schema version stays 1):
`phase` (`objective`, `readiness`, `basics`, `viewing`, `retrieval`, `practice`,
`repair`, `review`), `activity_id`, and `awaiting` (`viewing_report`,
`learner_response`, or null). Missing fields in a legacy vault mean unknown, not
completed. An active session checkpoint stores the exact pending prompt/task,
activity ID, mode (teaching/open-book/closed-book), expected rubric kept separate
from learner-facing answers, assigned source refs, and the next decision.

Record a new viewing assignment as a `lesson` event with `data.action: assigned`,
`activity_id`, phase, purpose/role, observation prompt, post-view task, pause point,
and assigned source refs. It is not a `watch_report` or successful attempt. A watch
report records what the learner actually says they watched and its provenance;
an attempt references the activity ID and actual response/assistance. If viewing
or response is still pending, keep it pending across conversations. The assigned
end time never becomes `position_seconds` without evidence of actual position.
Use a `plan_change` event for an explicit skip/format change and retain the gap.

Each JSONL event has unique `event_id`, `session_id`, `recorded_at`, `type`,
`objective_ids`, `source_refs`, and `data`. Types: `lesson`, `attempt`,
`watch_report`, `review`, `correction`, `plan_change`. Source refs use `source_id`,
`revision` (source hash/version), and locator (cue IDs with seconds, pages, or
file lines). Attempts store task/response or artifact path, rubric/result,
assistance (`independent`, `hinted`, `worked_example`), and feedback. Incomplete,
skipped, or revealed-answer tasks are not successes.

Generate the event ID before writing. Replayed events are not counted twice.
Append evidence first, then write state through a temporary file and atomic
replace, then refresh dashboard views. Verify writes. After interruption,
reconcile events after `last_event_id`; never repeat already logged evidence.
Serialize writes: if revision changed since reading, reload before updating.
Append corrections referencing prior events instead of overwriting responses.
Keep multiple learners/courses separate; store only learning-relevant personal data.

## Every-conversation context pack

Load state, profile, current objectives/prerequisites, latest checkpoint, due
reviews, concept evidence, manifest, and raw excerpts needed for this objective.
Search/page larger files instead of loading twenty hours of transcripts. Preserve
raw sources and source references when summarizing. Reconcile learner corrections
with saved state explicitly, retaining provenance rather than silently discarding it.

Checkpoints include ID/date, objective, lesson summary, learner responses and
assistance, source references, current playhead, blockers, due reviews, and next
action. If persistence fails, return this structure as a copyable handoff and say
it must be supplied next time. No automatic memory across devices/accounts/tools
is promised without accessible records. State what was successfully saved.

## Progress and completion

- Display sources indexed/listed, transcript coverage flags, lessons taught,
  learner-reported watch progress, objectives demonstrated/retained, unresolved
  misconceptions, and due reviews separately. Avoid a misleading combined percent.
- Demonstrated means independent work meets the agreed objective rubric. Retained
  means a later independent retrieval/application check succeeds. Record dates;
  hinted answers support learning but are not independent mastery evidence.
- Propose review intervals from observed difficulty and availability; initial
  defaults are provisional. Due dates are local queue entries, not notifications.
  Offer due reviews on return while honoring the learner's current request.
- Complete when required objectives and final application meet the agreed rubric.
  Report remaining optional work, source gaps, evidence limitations, and retention
  plan. Record explicit scope changes instead of silently dropping objectives.

## Legacy migration

Read old dashboards and concept files. Preserve attempts, correct counts, error
notes, and paths. Add new state with migration provenance; do not fabricate past
sessions or independent mastery from aggregate rates. Keep percentage badges as
quiz accuracy. Update the existing canonical dashboard rather than creating a
competing one. Link old concepts to stable objective IDs; missing historical
source references remain unknown until verified.
