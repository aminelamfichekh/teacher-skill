# Quiz Design Rules

## Zero-Hint Policy (CRITICAL)

Every question must be answerable ONLY by someone who actually knows the material.

1. **Option descriptions**: NEVER reveal correctness
   - BAD: `label: "stderr"`, `description: "Error output stream used by Cloud Run for error classification"`
   - GOOD: `label: "stderr"`, `description: "Standard error stream"`

2. **No "(Recommended)" tag** on any option

3. **Randomize** correct answer position — never always first or last

4. **Question phrasing**: Ask about behavior/purpose/output, don't hint at the answer
   - BAD: "Which error stream does error() use?"
   - GOOD: "Where does error() method output go?"

5. **Plausible distractors**: Wrong options must be real concepts from the domain, representing common misconceptions

## Question Types

1. **Factual recall**: "What HTTP status code is returned when...?"
2. **Conceptual understanding**: "Why does the system use X pattern?"
3. **Behavioral prediction**: "What happens when X fails?"
4. **Comparison/distinction**: "What is the difference between X and Y?"
5. **Debugging scenario**: "Given this error, what is the most likely cause?"

## Difficulty Balancing

- Diagnostic: easy 40%, medium 40%, hard 20%
- Weak-area drill: medium 30%, hard 70%
- Review: all levels evenly

## Drilling Unresolved Concepts

When targeting 🔴 concepts from concept files:
- Do NOT repeat the exact same question — rephrase in a new context
- Test the same underlying knowledge from a different angle
- E.g., if user confused "400 vs 422", ask a scenario question where they must choose the correct status code for a new situation

## Delivery and evidence

Choose the format for the objective: free response, calculation, explain-back,
code, scenario, project, or multiple choice. The legacy format is four questions
with four options each, but adapt length to the learner's time and request.
Use ordinary chat if a suitable quiz interface is unavailable. Do not use a UI
that automatically marks a correct option recommended or reveals it beforehand.
Keep the key/rubric separate until attempt or requested reveal.

Each item has objective/concept IDs, a source locator (video ID, cue IDs,
start/end timestamps and transcript revision for video items), a justified answer,
and a rubric. Cite evidence in post-attempt feedback, including what to rewatch.
Pre-attempt references are allowed for explicitly open-book activities; don't
accidentally reveal a closed-book answer in a watch instruction.
Record actual responses and assistance. Skips, reveals, and incomplete tasks
are not correct answers. Partial credit requires a stated rubric. Do not generate
scores or mastery until evidence exists. Small-round difficulty ratios are guides,
not exact quotas. An independent delayed check is required for retained status.

## File Update Protocol

After grading:
1. Update `concepts/{area}.md` — add/update concept rows + error notes
2. Update dashboard — recalculate area stats from concept files
3. Historical quiz accuracy badges (not mastery proof): 🟥 0-39% · 🟨 40-69% · 🟩 70-89% · 🟦 90-100% · ⬜ no data

## Language Rule

All file content and output in the user's detected language. Badge emojis are universal.
