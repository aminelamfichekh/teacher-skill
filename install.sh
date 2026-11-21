#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS=("tutor-setup" "tutor")

for skill in "${SKILLS[@]}"; do
  SKILL_DIR="$HOME/.claude/skills/$skill"

  if [ -d "$SKILL_DIR" ]; then
    echo "$skill skill already exists at $SKILL_DIR"
    printf "Overwrite? (y/N): "
    read -r answer
    if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
      echo "Skipping $skill."
      continue
    fi
  fi

  mkdir -p "$SKILL_DIR/references"
  cp "$SCRIPT_DIR/skills/$skill/SKILL.md" "$SKILL_DIR/"
  cp "$SCRIPT_DIR/skills/$skill/references/"* "$SKILL_DIR/references/"
  if [ -d "$SCRIPT_DIR/skills/$skill/scripts" ]; then
    mkdir -p "$SKILL_DIR/scripts"
    cp "$SCRIPT_DIR/skills/$skill/scripts/"*.py "$SKILL_DIR/scripts/"
  fi
  echo "Installed $skill to $SKILL_DIR"
done

echo ""
echo "Done! Usage in Claude Code:"
echo "  /tutor-setup  — Build a source-backed course from documents, code, or videos"
echo "  /tutor        — Teach, practice, assess, and resume your learning"
