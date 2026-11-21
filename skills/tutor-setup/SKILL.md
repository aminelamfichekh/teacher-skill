---
name: tutor-setup
description: >
  Build or extend a source-backed StudyVault learning space from documents,
  codebases, videos, timed transcripts, and long playlists. Use to prepare a
  complete course with a persistent knowledge base, timestamped watch map,
  teaching activities, assessments, and cross-conversation learning records.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Tutor Setup — Knowledge to Obsidian StudyVault

Invocation: `/tutor-setup [source-path-or-url]`.

## CWD Boundary Rule (ALL MODES)

> **NEVER access files outside the current working directory (CWD).**
> All source scanning, reading, and vault output MUST stay within CWD and its subdirectories. Skill instructions and bundled scripts may be read from their installed skill directory.
> If the user provides an external path, ask them to copy the files into CWD first.

## Learning-space contract (all modes)

Read [learning-space.md](references/learning-space.md) for persistent data,
course design, source evidence, and resume requirements. Add this layer to every
new vault and migrate existing vaults without replacing notes or progress.
Plan lessons around the adaptive objective -> prerequisites -> basics -> purposeful
viewing -> retrieval/discussion -> demonstration/practice -> targeted repair ->
save/revisit flow. Every assigned clip needs a purpose, observation prompt,
verified stopping point and post-view task. Use equivalent readings/demonstrations
for non-video sources; detailed lesson records are defined in learning-space.md.
Never manufacture source content, learner facts, or completed work. Distinguish
verified sources, supplemental explanations, proposed plans, and unresolved gaps.
Source evidence requirements override any template that suggests unsupported
expansion. Use the learner's requested language; keep IDs/schema keys stable.

## Mode Detection

Select by the user's supplied input and intent before looking at project markers:

1. Video/playlist URL, media file, SRT/VTT, or timed transcript -> **Video/Playlist
   Mode**. Read [video-workflow.md](references/video-workflow.md). Explicit video
   inputs take priority even when a code project exists in CWD.
2. Explicit document inputs -> **Document Mode**. Mixed courses may use multiple
   ingestion modes while keeping a single source registry and learning record.
3. Explicit codebase learning request, or project markers with no explicit source
   selection -> **Codebase Mode**. A `.git` directory alone is insufficient.
4. Otherwise -> **Document Mode**. Announce the selection and proceed when clear;
   ask only when ambiguity materially changes source selection or output.

---

## Document Mode

> Transforms knowledge sources (PDF, text, web, epub) into study notes.
> Templates: [templates.md](references/templates.md)

### Phase D1: Source Discovery & Extraction

1. **Auto-scan CWD** for `**/*.pdf`, `**/*.txt`, `**/*.md`, `**/*.html`, `**/*.epub` (exclude `node_modules/`, `.git/`, `dist/`, `build/`, `StudyVault/`). Report discovered sources; ask only if scope is ambiguous.
2. **Extract text**:
   - **PDF → prefer `pdftotext` CLI**. Extract searchable text first and inspect relevant images/pages only when text cannot verify the material.
     ```bash
     pdftotext -layout "source.pdf" "source-extracted.txt"
     ```
   - If unavailable, use an available extraction tool or report the limitation. Do not install dependencies without authorization. Scanned/image-heavy pages require OCR or visual inspection; flag unverified extraction.
   - URL → WebFetch
   - Other formats (`.md`, `.txt`, `.html`) → Read directly.
3. **Read extracted `.txt` files** — understand scope, structure, depth. Preserve page boundaries; inspect relevant source visuals when needed, recording extraction gaps.
4. **Source Content Mapping (MANDATORY for multi-file sources)**:
   - Read **cover page + TOC + 3+ sample pages from middle/end** for EVERY source file
   - **NEVER assume content from filename** — file numbering often ≠ chapter numbering
   - Build verified mapping: `{ source_file → actual_topics → page_ranges }`
   - Flag non-academic files and missing sources
   - Report verified mapping and unresolved gaps; continue with available evidence

### Phase D2: Content Analysis

1. Identify topic hierarchy — sections, chapters, domain divisions.
2. Separate concept content vs practice questions.
3. Map dependencies between topics.
4. Identify key patterns — comparisons, decision trees, formulas.
5. **Full topic checklist (MANDATORY)** — every topic/subtopic listed. Drives all subsequent phases.

> Match depth to source evidence and learning goals. Briefly mentioned topics stay brief unless supplementary material is clearly labeled and verified; never attribute textbook expansions to the source.

6. **Classification completeness**: When source enumerates categories ("3 types of X"), every member gets a dedicated note. Scan for: "types of", "N가지", "categories", "there are N".
7. **Source-to-note cross-verification (MANDATORY)**: Record which source file(s) and page range(s) cover each topic. Flag untraceable topics as "source not available".

### Phase D3: Tag Standard

Define tag vocabulary before creating notes:
- **Format**: English, lowercase, kebab-case (e.g., `#data-hazard`)
- **Hierarchy**: top-level → domain → detail → technique → note-type
- **Registry**: Only registered tags allowed. Detail tags co-attach parent domain tag.

### Phase D4: Vault Structure

Create `StudyVault/` with numbered folders per [templates.md](references/templates.md). Group 3-5 related concepts per file.

### Phase D5: Dashboard Creation

Create `00-Dashboard/`: MOC, Quick Reference, Exam Traps. See [templates.md](references/templates.md).

- **MOC**: Topic Map + Practice Notes + Study Tools + Tag Index (with rules) + Weak Areas (with links) + Non-core Topic Policy
- **Quick Reference**: every heading includes `→ [[Concept Note]]` link; all key formulas
- **Exam Traps**: per-topic trap points in fold callouts, linked to concept notes

### Phase D6: Concept Notes

Per [templates.md](references/templates.md). Key rules:
- YAML frontmatter: `source_pdf`, `part`, `keywords` (MANDATORY)
- **source_pdf MUST match verified Phase D1 mapping** — never guess from filename
- If unavailable: `source_pdf: 원문 미보유`
- `[[wiki-links]]`, callouts (`[!tip]`, `[!important]`, `[!warning]`), comparison tables > prose
- ASCII diagrams for processes/flows/sequences
- **Simplification-with-exceptions**: general statements must note edge cases

### Phase D7: Practice Questions

Per [templates.md](references/templates.md). Key rules:
- Every topic folder MUST have a practice file (8+ questions)
- **Active recall**: answers use `> [!answer]- 정답 보기` fold callout
- Patterns use `> [!hint]-` / `> [!summary]-` fold callouts
- **Question type diversity**: ≥60% recall, ≥20% application, ≥2 analysis per file
- `## Related Concepts` with `[[wiki-links]]`

### Phase D8: Interlinking

1. `## Related Notes` on every concept note
2. MOC links to every concept + practice note
3. Cross-link concept ↔ practice; siblings reference each other
4. Quick Reference sections → `[[Concept Note]]` links
5. Weak Areas → relevant note + Exam Traps; Exam Traps → concept notes

### Phase D9: Self-Review (MANDATORY)

Verify against [quality-checklist.md](references/quality-checklist.md) **Document Mode** section. Fix and re-verify until all checks pass.

---

## Video/Playlist Mode

Read [video-workflow.md](references/video-workflow.md). Inventory the complete
ordered playlist, acquire available timed transcripts, preserve raw evidence,
index resumable batches, record gaps, and build timestamp-linked lessons.
A playlist of ten two-hour videos is processed as independent versioned sources,
not a single prompt or a title-based summary. Report actual progress and pending
sources if access or context limits prevent completion; save an exact resume point.

---

## Codebase Mode

> Generates a new-developer onboarding StudyVault from a source code project.
> Full workflow: [codebase-workflow.md](references/codebase-workflow.md)
> Templates: [codebase-templates.md](references/codebase-templates.md)

### Phase Summary

| Phase | Name | Key Action |
|-------|------|------------|
| C1 | Project Exploration | Scan files, detect tech stack, read entry points, map directory layout |
| C2 | Architecture Analysis | Identify patterns, trace request flow, map module boundaries and data flow |
| C3 | Tag Standard | Define `#arch-*`, `#module-*`, `#pattern-*`, `#api-*` tag registry |
| C4 | Vault Structure | Create `StudyVault/` with Dashboard, Architecture, per-module, DevOps, Exercises folders |
| C5 | Dashboard | MOC (Module Map + API Surface + Getting Started + Onboarding Path) + Quick Reference |
| C6 | Module Notes | Per-module notes: Purpose, Key Files, Public Interface, Internal Flow, Dependencies |
| C7 | Onboarding Exercises | Code reading, configuration, debugging, extension exercises (5+ per major module) |
| C8 | Interlinking | Cross-link modules, architecture ↔ implementations, exercises ↔ modules |
| C9 | Self-Review | Verify against [quality-checklist.md](references/quality-checklist.md) **Codebase Mode** section |

See [codebase-workflow.md](references/codebase-workflow.md) for detailed per-phase instructions.

---

## Language

- Match source material language (Korean → Korean notes, etc.)
- **Tags/keywords**: ALWAYS English
