"""Offline timed-caption ingestion and retrieval. Python standard library only."""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
import sys


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seconds(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a timestamp")
    if isinstance(value, (int, float)):
        result = float(value)
    elif isinstance(value, str):
        parts = value.strip().replace(",", ".").split(":")
        if len(parts) not in (2, 3):
            raise ValueError(f"invalid timestamp: {value}")
        nums = [float(p) for p in parts]
        if any(n < 0 for n in nums) or any(n >= 60 for n in nums[1:]):
            raise ValueError(f"invalid timestamp: {value}")
        # MM:SS is the WebVTT short form; minutes must be below 60.
        if len(nums) == 2 and nums[0] >= 60:
            raise ValueError(f"invalid WebVTT minutes: {value}")
        result = sum(n * 60 ** i for i, n in enumerate(reversed(nums)))
    else:
        raise ValueError("timestamp must be seconds or a timed-caption timestamp")
    if not math.isfinite(result) or result < 0:
        raise ValueError("timestamp must be finite and nonnegative")
    return result


def parse(path):
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
        rows = data.get("segments") if isinstance(data, dict) else data
        if not isinstance(rows, list):
            raise ValueError("JSON must be an array or contain a segments array")
    elif path.suffix.lower() in (".srt", ".vtt"):
        rows = []
        for block in re.split(r"\n[ \t]*\n", raw.strip()):
            lines = block.splitlines()
            if not lines or lines[0].startswith(("NOTE", "STYLE", "REGION")):
                continue
            timing = [i for i, line in enumerate(lines) if "-->" in line]
            if not timing:
                if block.startswith("WEBVTT"):
                    continue
                raise ValueError("caption block has no timing line")
            if len(timing) != 1:
                raise ValueError("caption block has multiple timing lines")
            i = timing[0]
            start, end = lines[i].split("-->", 1)
            # WebVTT cue settings follow the end timestamp.
            rows.append({"start": start.strip(), "end": end.strip().split()[0],
                         "text": "\n".join(lines[i + 1:])})
    else:
        raise ValueError("supported input formats: .srt, .vtt, timed .json")
    cues = []
    for row in rows:
        if not isinstance(row, dict) or not all(k in row for k in ("start", "end", "text")):
            raise ValueError("each cue needs start, end, text")
        start, end = seconds(row["start"]), seconds(row["end"])
        if end <= start or (cues and start < cues[-1]["start"]):
            raise ValueError("cue ends must follow starts; starts must be ordered")
        if not isinstance(row["text"], str) or not row["text"].strip():
            raise ValueError("cue text must be a nonempty string")
        text = html.unescape(re.sub(r"<[^>]*>", "", row["text"]))
        cues.append({"cue_id": f"c{len(cues)+1:06}", "start": start, "end": end,
                     "text": text.strip()})
    if not cues:
        raise ValueError("no timed cues found")
    return cues


def coverage(cues, duration):
    merged = []
    overlaps = 0
    for cue in cues:
        a, b = cue["start"], cue["end"]
        if merged and a <= merged[-1][1]:
            overlaps += int(a < merged[-1][1])
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    gaps, previous = [], 0
    for a, b in merged:
        if a > previous:
            gaps.append([previous, a])
        previous = b
    if duration is not None and previous < duration:
        gaps.append([previous, duration])
    return {"covered_seconds": sum(b-a for a, b in merged), "intervals": merged,
            "timestamp_gaps": gaps, "overlapping_cues": overlaps,
            "duration_seconds": duration,
            "note": "Intervals describe captions, not verified speech or learning coverage."}


def make_chunks(cues, window):
    groups, group = [], []
    for cue in cues:
        if group and cue["start"] - group[0]["start"] >= window:
            groups.append(group)
            group = []
        group.append(cue)
    if group:
        groups.append(group)
    return [{"chunk_id": f"k{i:06}", "start": g[0]["start"],
             "end": max(c["end"] for c in g), "cue_ids": [c["cue_id"] for c in g],
             "text": "\n".join(c["text"] for c in g)} for i, g in enumerate(groups, 1)]


def ingest(args):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", args.source_id):
        raise ValueError("source ID must use letters, digits, underscores, or hyphens")
    if not math.isfinite(args.window) or args.window <= 0:
        raise ValueError("window must be finite and positive")
    duration = None if args.duration is None else seconds(args.duration)
    cues = parse(args.input)
    if duration is not None and max(c["end"] for c in cues) > duration:
        raise ValueError("cue exceeds verified video duration")
    if args.output.exists():
        raise ValueError("output already exists; choose a new revision directory")
    digest = hashlib.sha256(args.input.read_bytes()).hexdigest()
    chunks = make_chunks(cues, args.window)
    # Validate before creating anything. index.json is the completion marker.
    args.output.mkdir(parents=True)
    original = "original" + args.input.suffix.lower()
    shutil.copyfile(args.input, args.output / original)
    write_json(args.output / "cues.json", cues)
    write_json(args.output / "chunks.json", chunks)
    report = coverage(cues, duration)
    write_json(args.output / "index.json", {"schema_version": 1, "source_id": args.source_id,
               "sha256": digest, "original": original, "cue_count": len(cues),
               "chunk_count": len(chunks), "window_seconds": args.window, "coverage": report})
    print(json.dumps({"source_id": args.source_id, "cues": len(cues), "chunks": len(chunks),
                      "coverage": report}, ensure_ascii=False))


def check_index(path):
    base = path.parent
    index = read_json(path)
    original = base / index["original"]
    if original.parent.resolve() != base.resolve():
        raise ValueError(f"invalid original path: {path}")
    if hashlib.sha256(original.read_bytes()).hexdigest() != index["sha256"]:
        raise ValueError(f"raw transcript hash mismatch: {path}")
    cues, chunks = read_json(base / "cues.json"), read_json(base / "chunks.json")
    expected = parse(original)
    if cues != expected or len(cues) != index["cue_count"]:
        raise ValueError(f"cue mismatch: {path}")
    if chunks != make_chunks(cues, index["window_seconds"]) or len(chunks) != index["chunk_count"]:
        raise ValueError(f"chunk mismatch: {path}")
    duration = index["coverage"]["duration_seconds"]
    if duration is not None and max(c["end"] for c in cues) > duration:
        raise ValueError(f"duration mismatch: {path}")
    if index["coverage"] != coverage(cues, duration):
        raise ValueError(f"coverage mismatch: {path}")
    return index


def query_or_check(args):
    paths = sorted(args.root.rglob("index.json"))
    if not paths:
        raise ValueError("no completed source indexes found")
    # An interrupted ingestion must not disappear from a successful check.
    partials = list(args.root.rglob("cues.json")) + list(args.root.rglob("original.*"))
    for partial in partials:
        if not (partial.parent / "index.json").exists():
            raise ValueError(f"incomplete source directory: {partial.parent}")
    results = []
    terms = set(re.findall(r"\w+", args.query.casefold())) if args.command == "search" else set()
    if args.command == "search" and (not terms or args.limit < 1):
        raise ValueError("search needs a nonempty query and positive limit")
    for path in paths:
        index = check_index(path)
        if args.command == "search":
            for chunk in read_json(path.parent / "chunks.json"):
                words = set(re.findall(r"\w+", chunk["text"].casefold()))
                score = len(terms & words)
                if score:
                    results.append({"source_id": index["source_id"], "revision": index["sha256"],
                                    "index_path": str(path), "score": score, **chunk})
    if args.command == "check":
        print(json.dumps({"validated_indexes": len(paths)}))
    else:
        results.sort(key=lambda r: (-r["score"], r["source_id"], r["start"]))
        print(json.dumps(results[:args.limit], ensure_ascii=False, indent=2))


def main():
    # Stable UTF-8 JSON output on Windows, including redirected pipelines.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("ingest")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--source-id", required=True)
    p.add_argument("--duration", type=float)
    p.add_argument("--window", type=float, default=300)
    for command in ("search", "check"):
        p = subs.add_parser(command)
        p.add_argument("--root", type=Path, required=True)
        if command == "search":
            p.add_argument("--query", required=True)
            p.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    try:
        ingest(args) if args.command == "ingest" else query_or_check(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
