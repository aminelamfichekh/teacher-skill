# Long video and playlist ingestion

## 1. Inventory without assumptions

Resolve supplied playlist URLs using available tools, or use the user's exported
playlist/files. Record ordered entries, stable platform IDs, titles, durations,
language, availability, and retrieval date in the learning-space.md manifest.
Titles alone do not prove contents. Preserve unavailable entries. Compare listed
entries with a verified count if one exists; otherwise inventory is partial or
unverified. Deduplicate content by platform/source ID without dropping repeated
playlist positions (record occurrences). Never substitute another playlist.

## 2. Obtain evidence

Prefer actual timed captions (SRT, VTT, or normalized timed JSON). Preserve raw
files and record provenance, language, caption type, retrieval date, and hash.
Use available authorized download/transcription capabilities; do not promise
automatic access to every platform, bypass access controls, silently install
tools, or use paid transcription without authorization. If unavailable, request
caption exports or authorized media. Continue available entries, leaving others
blocked. Untimed transcripts remain useful text with line locators; never invent
times from word counts. Local ASR/alignment requires actual media and available
tools; record its method and uncertainty. Inspect formula/code/visual sections
when possible, otherwise record the limitation.

## 3. Normalize and index in resumable batches

The bundled standard-library helper supports SRT/VTT and timed JSON:

```text
python <skill-dir>/scripts/transcripts.py ingest --input <captions.srt> --output <vault>/sources/v01 --source-id v01 --duration 7200
python <skill-dir>/scripts/transcripts.py search --root <vault>/sources --query "gradient descent" --limit 8
python <skill-dir>/scripts/transcripts.py check --root <vault>/sources
```

`--duration` is optional and must be verified, not copied from an example. JSON
input is an array of `{start, end, text}` in seconds, or `{segments: [...]}`;
convert other exports explicitly, preserving original files. No hidden acquisition
or ASR is performed. The script rejects malformed/untimed data rather than guessing.
Use a new empty output directory for each revision; never overwrite old evidence.

Index each video independently, then update its manifest entry after success.
Retain raw cues, stable cue IDs, revision hash, chunks, and gap/coverage reports.
Chunk on cue boundaries at roughly five-minute windows (configurable); split
learning lessons on actual concept boundaries after inspecting the text. Do not
truncate a long cue or discard repeated/overlapping captions silently. Normalize
rolling-caption duplicates only in a separate derivative with provenance.

For ten two-hour videos, iterate all ten source entries. Load/index files in
bounded operations; retrieve only relevant excerpts for teaching. Before a context
handoff, save completed IDs/revisions, pending IDs, current processing step, and
next action. Resume by checking files/hashes, not by trusting an earlier claim.
If interrupted, mark the entry pending until its full generated output validates.
Track extraction/indexing separately from topic analysis and reviewed ranges.

## 4. Build source-backed course materials

Map each verified topic to source ID, raw cue IDs, start/end seconds, and revision.
Generate chapters, concept notes, glossary, practice, watch map, and course plan
from evidence. Repeated topics keep all useful locators. Every substantive video
explanation and exercise solution includes `HH:MM:SS–HH:MM:SS`, title/ID, and
playback link if supported. YouTube verified IDs use a watch URL with `&t=<seconds>s`;
other platforms need verified syntax or original URL plus manual seek range.
Keep times video-local, including hour components for long videos.

Assign each selected range a lesson role (introduction, explanation, demonstration,
practice support, or optional depth). Plan the prerequisite primer, what to notice,
verified stop point, and post-view task. The teacher pauses for actual learner
participation before progressing. A retrieval chunk is not automatically a clip
assignment; inspect concept boundaries and prerequisites before selecting ranges.

Raw caption interval coverage is not semantic completeness: gaps may be silence,
and auto captions may be wrong. Report both index coverage flags and evidence
limitations. Never call a whole playlist understood just because it was indexed.

## 5. Revisions and validation

If transcripts change, retain the old revision and regenerate into a new directory.
Mark dependent notes/items stale until locators and claims are reverified. Preserve
historical learner evidence against its original revision. Verify links resolve
to the intended video/start, ranges are within known duration, cues exist, no
entries disappeared, and the context pack can resume in a fresh conversation.
Use `quality-checklist.md` Learning Space / Video section before reporting done.
