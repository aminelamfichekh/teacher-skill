# How teacher-skill teaches

This guide describes the learning experience, the agent's responsibilities, the
source data it needs, and what gets saved. The default lesson flow is:

**Objective -> prerequisite check -> essential basics -> purposeful viewing ->
retrieval and discussion -> demonstration and practice -> targeted repair ->
save and revisit.**

The tutor adapts the order to the learner and subject. It delivers one useful
activity at a time and waits for participation. It does not send an entire course
script and pretend the learner completed it.

## 1. What is installed

The repository contains two agent skills and an offline transcript helper:

| Component | Responsibility | What it produces |
|---|---|---|
| `tutor-setup` | Prepare sources and a course | Source inventory, indexed captions, notes, lesson/watch map, initial records |
| `tutor` | Conduct learning sessions | Explanations, viewing assignments, practice, feedback, checkpoints, reviews |
| `transcripts.py` | Normalize, search, and validate timed captions | Original captions, cue/chunk files, revision hash, coverage flags |

The agent carries out the teaching and record updates using these instructions.
The Python helper does not teach, download playlists, run speech recognition,
create a complete learning vault, or update learner progress by itself. This
project does not supply a hosted LMS, autonomous background teacher, or video
player. It works through an agent with access to the sources and local files.

## 2. Starting a new learning space

Provide the source files or URLs, the intended outcome, and any important
constraints. For example:

```text
/tutor-setup Use this playlist and these SRT files to teach me the subject from
the beginning. I want to build a small project by the end and have 30 minutes
per session. Keep all course records in StudyVault.
```

The tutor only treats the goal and constraints actually provided as confirmed.
It asks focused questions when necessary and marks other choices provisional.
Starting level can be self-reported or assessed; the two are recorded separately.
Being new is not a failure and does not require a long diagnostic exam.

Setup inventories actual sources, records access and evidence gaps, builds a
prerequisite map, and proposes a course with observable objectives. An objective
describes an ability such as explaining a mechanism or solving a class of problems.
"Watch video 4" is an activity, not a competence objective.

For documents, sources are cited by pages or sections. For codebases, they are
cited by file/line ranges and revision. For video, the tutor uses the exact
source ID, inspected caption cues, timestamp range, and transcript revision.
Mixed-source courses use one registry so explanations can connect these sources.

## 3. Preparing a long playlist

A playlist containing ten two-hour videos is handled as a collection of sources,
not as one enormous chat message. Setup:

1. Records verified playlist order, stable video IDs, titles, available durations,
   language, retrieval date, and inaccessible/deleted entries.
2. Acquires available timed captions through authorized tools, or uses supplied
   SRT/VTT/timed JSON files. Missing access is reported rather than invented.
3. Preserves originals, normalizes cue times, and creates searchable chunks per
   source revision. The helper checks timestamp order, duration bounds when known,
   overlaps, gaps, and generated file consistency.
4. Reviews actual content to identify topics, prerequisites, and useful intervals.
   Indexing text is separate from verifying the meaning of every passage.
5. Maps inspected intervals to lessons and records whether each is an introduction,
   explanation, demonstration, practice support, or optional depth.
6. Saves completed source IDs/revisions, unreviewed ranges, blockers, and the exact
   next ingestion/review step before a handoff.

Original playlist order remains available even when prerequisite needs produce a
different teaching sequence. Repeated playlist entries remain visible; identical
source content need not be indexed twice. Topic details inferred only from a title
remain unverified. A complete inventory does not imply a fully reviewed course.

The helper's default five-minute window is a retrieval setting. A lesson or clip
is selected on meaningful concept boundaries after inspection. There is no claim
that every learner or subject has one ideal video length. A short assignment must
still contain enough context to make sense.

## 4. The default lesson, step by step

### State the objective

The tutor states what you should be able to do, why it matters, and the success
criterion. It connects this to your course goal and current position. A lesson
should be small enough to discuss, practise, and check within your available time;
time estimates are identified as estimates.

### Check the prerequisites

The tutor uses existing evidence or asks a small question about an essential
prerequisite. If you say you are completely new, it can begin with the basics.
If prerequisite knowledge is missing, it repairs that dependency before assigning
a clip that assumes it. An unanswered prompt stays pending; it is not an error.

### Explain the essential basics

Before a demanding explanation, the tutor introduces the terms, components, or
notation needed to follow it. A useful explanation usually establishes:

- The problem the idea solves and a concrete example.
- The minimum vocabulary and a simple mental model.
- How the mechanism or procedure works, one step at a time.
- How the example connects to the general rule and important exceptions.

The primer prepares you for the selected clip. It need not repeat the entire
lecture. Tutor-created analogies and examples are identified as such; their
limits are explained when they could mislead. Source claims remain cited.

### Assign viewing with a purpose

Every assignment answers: what to watch, why, what to notice, where to stop, and
what to do next. A compact learner-facing format is:

```text
Goal: <what you will be able to explain or do>
Before watching: <essential basics, or why you are already prepared>
Watch: <verified video title/ID>, <HH:MM:SS-HH:MM:SS>, <playback link>
Purpose: <explanation, demonstration, or another defined role>
Look for: <a specific change, relationship, decision, or step>
Pause at: <verified boundary>
Afterward: <a recall, prediction, explain-back, or application task>
```

These are template fields, not actual source references. The agent must fill them
from inspected evidence. A YouTube start link sets the starting position only,
so the visible reference also shows where to stop. Times remain local to each
video, including hours. Unsupported platform seek syntax is replaced by the
original link and a manual seek range.

The tutor records the assignment, then pauses. It does not assume that sending
the link means you watched it. You can report completion, answer the post-view
prompt, ask for help, or request a different representation.

### Retrieve and discuss

After viewing, the tutor asks you to reconstruct an idea: explain a cause, predict
an outcome, sketch a process, trace a step, or recall the important distinction.
It waits for your response before showing the key or grading. A simple "does that
make sense?" is not treated as demonstrated understanding.

Guided open-book work is allowed and identified. For independent closed-book
assessment, the answer is not disclosed in the prompt, option descriptions, or
an accompanying solution. Requested hints/reveals are provided and recorded as
assistance rather than independent success.

### Demonstrate and practise

The tutor can show a worked example, invite you to complete a partially worked
one, then give a fresh independent problem. The balance depends on your evidence:
a beginner may need more demonstration; someone already proficient may start with
application. Support is reduced as you show you can perform the task yourself.

The activity should match the objective. Explaining a mechanism calls for causal
reasoning; a coding objective needs code or a trace; a practical skill needs an
appropriate performance artifact. A multiple-choice answer alone may not provide
the evidence required by that objective's rubric.

### Repair the specific gap

Feedback explains what worked, the particular error, and an actionable next step.
The tutor distinguishes a missing prerequisite, terminology confusion, procedural
mistake, and unsupported guess. It changes the representation or example when
repeating the same explanation would not help.

A rewatch is targeted: a verified interval plus something new to notice. Then a
fresh task checks whether the gap was repaired. Rewatching the entire two-hour
video is not the default response to one misconception. The learner can choose
to move on; remaining gaps are retained in the record.

### Save and revisit

After a meaningful activity, the tutor saves the actual response/artifact,
assistance, rubric result, misconception, references, and next step. A later
retrieval or application check supplies evidence of retention. Initial review
dates are provisional and adapt to performance, availability, and retention goals.

## 5. When the order changes

| Situation | Adaptation |
|---|---|
| Completely new learner | Teach essential vocabulary/model before a demanding clip. |
| Prerequisites demonstrated | Shorten the primer and proceed to a useful clip or task. |
| A phenomenon needs to be seen first | Offer a brief directed preview, then explain before deeper viewing. |
| Learner already watched the material | Accept the report and check understanding; do not force another viewing. |
| A task exposed a specific gap | Diagnose it, explain or rewatch the relevant passage, then retry differently. |
| Learner asks a direct question | Answer it with evidence; offer practice without forcing a full lesson. |
| Video cannot be accessed | Use available cited text or accessible alternatives; retain visual limitations. |
| Documents or code are the source | Substitute a cited reading, worked example, trace, or demonstration. |

These are practical routing choices, not claims that a single order is universally
best. Preferences and accessibility needs can change the format without changing
what evidence counts as independent competence.

## 6. What the knowledge base stores

| Record | Purpose | Must not be confused with |
|---|---|---|
| Original sources and caption revisions | Preserve what the material actually said | A tutor's summary or corrected interpretation |
| `sources/manifest.json` | Order, availability, provenance, indexing/review status | Learner progress |
| `learning/PROFILE.md` | Confirmed goals/preferences and labeled unknowns | Guessed ability or schedule |
| `learning/COURSE.md` and linked lessons | Objectives, dependencies, clip roles, activities and rubrics | Evidence that the work was completed |
| `learning/STATE.json` | Current objective, phase, pending activity, due reviews | The complete history of every response |
| `learning/events.jsonl` | Actual evidence and corrections with unique IDs | Invented scores or simulated participation |
| `learning/sessions/` | Exact pending prompt, position, blockers, next decision | Automatic memory without file access |
| Concept records and learner artifacts | Misconceptions, solutions, practice outputs | Proof of independent work when copied or hinted |

Current phase and pending activity fields extend the existing state contract
without invalidating older vaults. Missing old fields mean unknown. A new viewing
assignment records assigned ranges; actual playhead and watched ranges only change
with evidence. Activity IDs connect assignments, responses, and later corrections.

Writes preserve prior evidence: append the event, update compact state atomically,
then refresh dashboard views. Event IDs prevent duplicate counting on replay.
If a session ends while a prompt is pending, the checkpoint keeps the prompt,
source revision, mode, and next action. The answer key/rubric is kept separate
from the learner-facing prompt.

On return, the agent reloads the profile, course, state, checkpoint, relevant
concept evidence, due reviews, source registry, and required raw excerpts. It does
not load the whole playlist into the prompt or rely on unsaved conversation memory.
If the vault is inaccessible or saving fails, it says so and supplies a portable
handoff. Continuity across machines/accounts requires the same data to be available.

## 7. Progress and course completion

The dashboard reports separate dimensions:

- Sources listed/indexed and content reviewed, with gaps.
- Clips assigned and learner-reported watched ranges.
- Lessons taught and activities still awaiting participation.
- Objectives independently demonstrated and later retained.
- Misconceptions, due reviews, and next action.

A correct answer after a hint can be useful learning without meeting an independent
rubric. A high historical quiz percentage is not automatically mastery. Retained
status requires a later independent check. Skips and reveals are not successes.

The course reaches its agreed completion criteria when required objectives and
the final application meet the rubric. Outstanding optional work, unverified
sources, and pending retention checks remain visible. The tutor records explicit
scope changes rather than silently dropping difficult objectives. Review dates
create a local queue; they do not send notifications unless actual scheduling is
available and you request it.

## 8. Learning and teaching tools

Choose a tool because it serves the objective, then create usable materials:

| Purpose | Useful activities |
|---|---|
| Remember | Retrieval prompts, flashcards, cloze, spaced review queue |
| Understand | Explain-back, causal diagrams, concept maps, comparisons, counterexamples |
| Perform a procedure | Worked examples, partially completed tasks, checklists, independent practice |
| Apply and troubleshoot | Cases, calculations, coding labs, prediction, debugging |
| Prepare for assessment | Mixed practice, mock exams, requested timed work |
| Demonstrate competence | Mini-projects, capstone, portfolio artifacts with rubrics |
| Navigate media | Chapter maps, purposeful watch lists, guided viewing worksheets |
| Organize | Course planner, glossary, quick reference, learning journal |

Each activity has instructions, source references, an expected learner action,
feedback criteria, and a saved response or artifact. Interactive tools and exports
depend on available capabilities. Predicted code/math results must be distinguished
from actually executed verification.

## 9. Evidence limits and research basis

Raw cues are checked before source-backed teaching. Titles, summaries, and lexical
search hits only help locate evidence. Untimed text cannot justify precise watch
times. Auto-caption errors, contradictory passages, and visual-only demonstrations
remain explicit limitations until verified. A gap between cues can be silence;
it is not automatically missing speech. A transcript cannot prove anyone watched.

The workflow combines established findings into a practical design for this skill:

| Design decision | Research basis and boundary |
|---|---|
| Prepare essential terms before complex multimedia | [Mayer and Pilegard](https://doi.org/10.1017/CBO9781139547369.016) discuss pre-training names and characteristics of components; this supports a targeted primer, not a compulsory duplicate lecture. |
| Use meaningful segments and pauses | [Rey et al. (2019)](https://doi.org/10.1007/s10648-018-9456-4) report benefits for retention and transfer across 56 investigations; this does not establish one ideal clip duration. |
| Invite retrieval between video segments | [Szpunar et al. (2013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3631699/) found improved learning and reduced mind wandering in two experiments with online lectures; the findings do not guarantee identical effects for every course. |
| Alternate examples and attempts; reduce support as skill grows | The [IES practice guide](https://ies.ed.gov/ncee/wwc/PracticeGuide/1) recommends worked examples alongside problem solving; the amount of guidance should respond to learner knowledge. |
| Revisit learning after delays | [Cepeda et al. (2008)](https://pubmed.ncbi.nlm.nih.gov/19076480/) show that effective spacing depends on the retention horizon; a universal fixed calendar is not implied. |

The exact combined teacher-skill flow is a design synthesis, not an experimentally
validated product. Automated repository checks validate transcript behavior and
skill structure. Actual teaching quality, accessibility, and learning outcomes
need evaluation in real course use. Research citations support specific choices;
they are not endorsements of this tool by the cited authors or institutions.

## 10. Operational reference

- [Setup entry point](../skills/tutor-setup/SKILL.md)
- [Learning-space setup contract](../skills/tutor-setup/references/learning-space.md)
- [Video ingestion procedure](../skills/tutor-setup/references/video-workflow.md)
- [Tutor entry point](../skills/tutor/SKILL.md)
- [Lesson delivery and teaching tools](../skills/tutor/references/teaching-tools.md)
- [Video grounding and viewing contract](../skills/tutor/references/video-grounding.md)
- [State, events, recovery, and migration](../skills/tutor/references/learning-record.md)
- [Assessment rules](../skills/tutor/references/quiz-rules.md)

The skill references are included when installing the skill folders. This guide
is repository documentation; the agent does not need a separate docs checkout
to follow the operational instructions.
