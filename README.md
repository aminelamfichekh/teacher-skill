# teacher-skill

Two skills for a persistent, source-backed learning space. Build a course from
documents, code, or a video playlist, then learn through explanations, guided
practice, independent assessment, projects, and retention reviews. Files in a
StudyVault carry the knowledge base and progress across conversations.

The default teaching flow is **objective -> prerequisites -> essential basics ->
purposeful viewing -> retrieval and discussion -> demonstration and practice ->
targeted repair -> save and revisit**. The tutor adapts to your actual knowledge
and pauses for your participation between activities.

Read the [complete learning guide](docs/learning-guide.md) for the lesson process,
video assignments, knowledge-base records, progress rules, research basis, and
practical limitations.

| Skill | Purpose |
|---|---|
| `tutor-setup` | Inventory sources, build a knowledge base, index timed transcripts, create a course and learner records |
| `tutor` | Teach, answer questions with source references, practice, assess, and resume from saved evidence |

These are agent instructions and a local transcript utility, not a hosted LMS or
a video player. Obsidian is optional; the vault uses ordinary Markdown and JSON.
Continuity requires access to the same vault or a supplied portable checkpoint.

## Install

```bash
npx skills add aminelamfichekh/teacher-skill
```

Or clone this repository and use the included Bash installer for Claude Code:

```bash
git clone https://github.com/aminelamfichekh/teacher-skill.git
cd teacher-skill
./install.sh
```

The Bash installer copies both skills, their references, and the Python helpers
to `~/.claude/skills/`. On Windows use a Bash environment, or copy each skill
folder to the skill directory supported by your agent. This edit does not change
any already-installed copy. Python 3.10+ is required only for transcript helpers.
No packages, model providers, or transcription services are installed automatically.

## Start a course

Example requests:

```text
/tutor-setup Turn these PDFs into a course with explanations and practice.
/tutor-setup Build a learning space from this playlist and these caption exports.
/tutor Teach the next lesson and show the precise video sections I should watch.
/tutor Explain this idea using the original transcript, then give me a practice task.
/tutor Resume where we stopped, review what is due, and continue my project.
```

Supply actual source paths or URLs in place of descriptions. The skills retain
document study notes and codebase onboarding workflows. Explicit video input takes
priority over incidental project markers; mixed-source courses share one registry.

## How a lesson works

| Step | What happens |
|---|---|
| Objective | Define what you should be able to explain or do. |
| Prerequisites | Use saved evidence or a small prompt to check essential prior knowledge. |
| Basics | Introduce unfamiliar terms, a concrete example, and the simplest useful model. |
| Purposeful viewing | Give a verified timestamp range, playback link, purpose, what to notice, stop point, and post-view task. |
| Retrieval and discussion | Ask you to explain, predict, sketch, or reconstruct before revealing the answer. |
| Demonstration and practice | Show an example if needed, guide an attempt, then invite independent application. |
| Targeted repair | Diagnose the gap, change the explanation or assign a focused rewatch, then check again. |
| Save and revisit | Record actual evidence, pending activity, source position, next step, and a later review. |

For a beginner, the essentials usually come before a demanding clip. If you
already demonstrate the prerequisites, the tutor can shorten the primer. A brief
visual preview can come first when it introduces the phenomenon. Direct questions
receive direct supported answers; documents and code use equivalent cited excerpts
or demonstrations. The eight steps guide delivery without forcing every step
into every interaction.

Every video assignment follows a before/during/after contract:

```text
Goal: <observable outcome>
Before watching: <essential basics or confirmed readiness>
Watch: <verified title/ID>, <HH:MM:SS-HH:MM:SS>, <playback link>
Purpose: <why this segment helps>
Look for: <specific relationship, change, decision, or step>
Pause at: <verified boundary>
Afterward: <one meaningful task>
```

The tutor fills those fields from real source evidence, saves the assignment,
then waits. A link being sent does not count as watched or understood. If you
return in a new conversation, the pending prompt and references remain available
in the checkpoint. See the [detailed guide](docs/learning-guide.md) for adaptation,
feedback, completion, and worked-example guidance.

## Long playlists and timestamps

A ten-video playlist of two-hour videos is indexed one source at a time, with raw
captions, version hashes, stable cue IDs, searchable chunks, coverage flags, and
checkpoints. It is never squeezed into a single conversation context. Relevant
raw excerpts are retrieved before teaching.

Video explanations, notes, and exercise solutions cite the title/ID, supporting
`HH:MM:SS-HH:MM:SS` range, transcript revision, and a playback link when supported.
A watch plan shows what to watch, why, prerequisites, and unique viewing time.
Times stay local to each video. Missing captions, uncertain ASR, unavailable videos,
and unsupported visual claims are reported explicitly. Untimed text cannot produce
verified playback timestamps. A transcript is not evidence that someone watched.

Automatic caption acquisition depends on the tools and permissions available to
the agent. The bundled offline utility accepts SRT, VTT, or JSON arrays containing
`start`, `end`, and `text` (seconds), including a `segments` wrapper. It does not
fetch playlists, download videos, transcribe audio, or infer timestamps.

```bash
python skills/tutor-setup/scripts/transcripts.py ingest --input video01.srt --output StudyVault/sources/v01 --source-id v01 --duration 7200
python skills/tutor-setup/scripts/transcripts.py search --root StudyVault/sources --query "your concept" --limit 8
python skills/tutor-setup/scripts/transcripts.py check --root StudyVault/sources
```

Use `--duration` only with a verified duration; omit it if unknown. Each output
directory must be new. Preserve old revisions when captions change. Ingestion
produces `original.*`, `cues.json`, `chunks.json`, and `index.json`; the agent adds
source metadata and availability to the course manifest. Search is lexical, not
semantic, and returns evidence candidates to inspect. Caption gaps can be silence
or omitted speech, so they are inspection flags rather than proof of missing content.

Retrieval windows do not prescribe lesson or clip duration. The agent inspects
concept boundaries and prerequisites, then assigns each useful interval a role:
introduction, explanation, demonstration, practice support, or optional depth.

## Persistent course data

```text
StudyVault/
  00-Dashboard/              overview and resume links
  sources/manifest.json      ordered inventory, availability, provenance
  sources/<source-id>/       original captions, cues, chunks, index
  learning/PROFILE.md        confirmed goals, preferences, unknowns
  learning/COURSE.md         objectives, prerequisites, watch map, rubrics
  learning/STATE.json        current lesson/playhead, objective status, due reviews
  learning/events.jsonl      actual learning evidence and corrections
  learning/sessions/         checkpoints and next actions
  concepts/                  concept notes, misconceptions, legacy records
```

Every conversation reloads the relevant record and source excerpts. Legacy notes,
quiz statistics, and paths are preserved. Indexed content, learner-reported watching,
lessons taught, demonstrated competence, and later retention are tracked separately.
The skill must not fabricate learner responses, scores, previous sessions, or mastery.
If persistence fails, it returns a portable handoff instead of claiming it saved.
Review dates form a local queue; proactive notifications require actual scheduling
support and an explicit scheduling request.

## Teaching and learning tools

Select activities for the objective: explanations, worked examples, Socratic
questions, explain-back, concept maps, flashcards, cloze, worksheets, calculations,
coding labs, debugging, scenarios, mock exams, projects, capstones, journals,
planners, glossaries, quick references, and spaced review queues. Interactive tools
are used only when available and useful. Responses and artifacts are evaluated
against an explicit rubric; guided answers stay distinct from independent work.

At course level, setup establishes the goal, prerequisite-aware path and final
application rubric. Lessons use the adaptive flow above. Completion depends on
required objective evidence and the final application; later retention checks
remain visible. Learners can request explanations, guided work or quizzes.

The [research section of the guide](docs/learning-guide.md#9-evidence-limits-and-research-basis)
explains the evidence for pre-training, segmenting, retrieval, worked examples,
and spacing, alongside the limits of applying those findings to this skill.

## Validation

```bash
python skills/tutor-setup/scripts/test_transcripts.py
python -X utf8 /path/to/skill-creator/scripts/quick_validate.py skills/tutor
python -X utf8 /path/to/skill-creator/scripts/quick_validate.py skills/tutor-setup
```

Tests use synthetic sources, including ten two-hour transcripts. They exercise
source retrieval, exact cue linkage, hour timestamps, Unicode, overlap/gap accounting,
malformed input, duration bounds, immutable revisions, tamper detection, and
interrupted indexes. Real platform access and full teaching behavior still require
an actual course run; these checks do not imply those were tested.

## Uninstall

Run `./uninstall.sh` for copies installed by the Bash installer. Back up any
learning vault separately; uninstalling instructions should not delete learner data.

## License

[MIT](LICENSE)

