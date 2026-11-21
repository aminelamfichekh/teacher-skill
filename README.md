# teacher-skill

Two skills for a persistent, source-backed learning space. Build a course from
documents, code, or a video playlist, then learn through explanations, guided
practice, independent assessment, projects, and retention reviews. Files in a
StudyVault carry the knowledge base and progress across conversations.

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

## Long playlists and timestamps

A ten-video playlist of two-hour videos is indexed one source at a time, with raw
captions, version hashes, stable cue IDs, searchable chunks, coverage flags, and
checkpoints. It is never squeezed into a single conversation context. Relevant
raw excerpts are retrieved before teaching.

Video explanations, notes, and exercise solutions cite the title/ID, supporting
`HH:MM:SS?HH:MM:SS` range, transcript revision, and a playback link when supported.
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

The course flow is intake, prerequisite-aware plan, teaching, guided practice,
independent application, feedback and repair, checkpoints, final application,
and retention review. Learners can ask for direct teaching or choose a quiz;
there is no forced quiz-only flow or mandatory session menu.

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

