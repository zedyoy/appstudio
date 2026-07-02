from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


DEFAULT_VIDEO_DIR = Path(r"C:\Users\Admin\Videos\ARCHITETTURA E CALCOLATORI")
DEFAULT_OUTPUT_DIR = Path("data") / "architecture_video_transcripts"

TOPIC_KEYWORDS = {
    "conversioni": [
        "binario",
        "ottale",
        "esadecimale",
        "conversione",
        "base",
        "complemento",
        "virgola",
        "floating",
        "ieee",
    ],
    "porte_logiche": [
        "and",
        "or",
        "not",
        "nor",
        "nand",
        "xor",
        "boole",
        "karnaugh",
        "mintermini",
        "sop",
    ],
    "mips_assembly": [
        "mips",
        "assembly",
        "registro",
        "registri",
        "load",
        "store",
        "branch",
        "beq",
        "bne",
        "lw",
        "sw",
        "lb",
        "sb",
        "addi",
    ],
    "memoria_bus": [
        "memoria",
        "cache",
        "bus",
        "indirizzo",
        "temporizzazione",
        "ram",
        "rom",
        "word",
    ],
    "microarchitettura": [
        "microarchitettura",
        "microistruzione",
        "mic",
        "ijvm",
        "datapath",
        "alu",
        "controllo",
    ],
    "clock_prestazioni": [
        "clock",
        "ciclo",
        "frequenza",
        "cpi",
        "prestazioni",
        "tempo",
        "latenza",
    ],
    "registri_flip_flop": [
        "flip flop",
        "latch",
        "registro",
        "registri",
        "propagazione",
    ],
}


def slugify(value: str) -> str:
    text = value.lower()
    text = text.replace("à", "a").replace("è", "e").replace("é", "e")
    text = text.replace("ì", "i").replace("ò", "o").replace("ù", "u")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "lezione"


def lesson_number(path: Path) -> int:
    match = re.search(r"lez(?:ione|ione)?\s*(\d+)|(\d+)\s*lex?ione", path.stem.lower())
    if match:
        for group in match.groups():
            if group:
                return int(group)
    match = re.search(r"\d+", path.stem)
    return int(match.group(0)) if match else 999


def run_json(command: list[str]) -> dict:
    proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def probe_duration(video_path: Path) -> float:
    data = run_json(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(video_path),
        ]
    )
    return float(data.get("format", {}).get("duration") or 0)


def fmt_time(seconds: float | int) -> str:
    seconds = int(seconds or 0)
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def ensure_dirs(output_dir: Path) -> dict[str, Path]:
    paths = {
        "root": output_dir,
        "raw": output_dir / "raw_json",
        "text": output_dir / "text",
        "markdown": output_dir / "markdown",
        "tmp": output_dir / "_tmp_audio",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def transcript_text(raw_data: dict) -> str:
    segments = raw_data.get("segments") or []
    if not segments:
        return str(raw_data.get("text") or "").strip()
    lines = []
    for segment in segments:
        start = fmt_time(segment.get("start", 0))
        end = fmt_time(segment.get("end", 0))
        text = re.sub(r"\s+", " ", str(segment.get("text") or "")).strip()
        if text:
            lines.append(f"[{start} - {end}] {text}")
    return "\n".join(lines).strip()


def topic_scores(text: str) -> list[dict]:
    lowered = text.lower()
    scores = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        hits = []
        for keyword in keywords:
            count = lowered.count(keyword)
            if count:
                score += count
                hits.append(keyword)
        if score:
            scores.append({"topic": topic, "score": score, "hits": hits[:8]})
    scores.sort(key=lambda item: item["score"], reverse=True)
    return scores[:5]


def write_lesson_files(video_path: Path, slug: str, raw_path: Path, paths: dict[str, Path], duration: float) -> dict:
    raw_data = json.loads(raw_path.read_text(encoding="utf-8"))
    text = transcript_text(raw_data)
    topics = topic_scores(text)

    text_path = paths["text"] / f"{slug}.txt"
    text_path.write_text(text + "\n", encoding="utf-8")

    md_path = paths["markdown"] / f"{slug}.md"
    md_lines = [
        f"# {video_path.stem}",
        "",
        f"- File: `{video_path}`",
        f"- Durata: {fmt_time(duration)}",
        f"- Trascrizione: `{raw_path.name}`",
        "",
        "## Argomenti probabili",
    ]
    if topics:
        for item in topics:
            md_lines.append(
                f"- {item['topic']} ({item['score']}): {', '.join(item['hits'])}"
            )
    else:
        md_lines.append("- Da classificare")
    md_lines.extend(["", "## Trascrizione", "", text])
    md_path.write_text("\n".join(md_lines).strip() + "\n", encoding="utf-8")

    return {
        "slug": slug,
        "title": video_path.stem,
        "source_path": str(video_path),
        "duration_seconds": round(duration, 2),
        "raw_json": str(raw_path),
        "text": str(text_path),
        "markdown": str(md_path),
        "topics": topics,
        "segments": len(raw_data.get("segments") or []),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }


def write_manifest(output_dir: Path, lessons: list[dict], status: str, extra: dict | None = None) -> None:
    payload = {
        "status": status,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "lesson_count": len(lessons),
        "lessons": lessons,
    }
    if extra:
        payload.update(extra)
    (output_dir / "manifest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    index_lines = [
        "# Trascrizioni Architettura dei Calcolatori",
        "",
        f"Stato: **{status}**",
        f"Aggiornato: {payload['updated_at']}",
        "",
    ]
    for lesson in lessons:
        topics = ", ".join(item["topic"] for item in lesson.get("topics", [])[:3]) or "da classificare"
        index_lines.append(
            f"- [{lesson['title']}](markdown/{lesson['slug']}.md) - {fmt_time(lesson['duration_seconds'])} - {topics}"
        )
    (output_dir / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def transcribe_video(video_path: Path, slug: str, raw_path: Path, paths: dict[str, Path], args) -> None:
    tmp_audio = paths["tmp"] / f"{slug}.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            "16000",
            str(tmp_audio),
        ],
        check=True,
    )

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    command = [
        "whisper",
        str(tmp_audio),
        "--language",
        args.language,
        "--model",
        args.model,
        "--device",
        "cpu",
        "--fp16",
        "False",
        "--output_dir",
        str(paths["raw"]),
        "--output_format",
        "json",
        "--verbose",
        "False",
        "--threads",
        str(args.threads),
        "--initial_prompt",
        "Lezione universitaria in italiano di Architettura dei Calcolatori: MIPS, registri, ALU, memoria, bus, clock, porte logiche, complemento a due, IEEE 754, microarchitettura, IJVM.",
    ]
    subprocess.run(command, check=True, env=env)

    produced = paths["raw"] / f"{tmp_audio.stem}.json"
    if produced != raw_path:
        produced.replace(raw_path)

    if not args.keep_audio:
        tmp_audio.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-dir", type=Path, default=DEFAULT_VIDEO_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="it")
    parser.add_argument("--threads", type=int, default=max((os.cpu_count() or 4) - 1, 2))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--only", default="")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--keep-audio", action="store_true")
    args = parser.parse_args()

    paths = ensure_dirs(args.output_dir)
    videos = sorted(args.video_dir.glob("*.mp4"), key=lambda p: (lesson_number(p), p.name.lower()))
    if args.only:
        wanted = {item.strip().lower() for item in args.only.split(",") if item.strip()}
        videos = [video for video in videos if slugify(video.stem).lower() in wanted or video.stem.lower() in wanted]
    if args.limit:
        videos = videos[: args.limit]

    lessons: list[dict] = []
    if (args.output_dir / "manifest.json").exists():
        try:
            current = json.loads((args.output_dir / "manifest.json").read_text(encoding="utf-8"))
            lessons = current.get("lessons") or []
        except Exception:
            lessons = []

    by_slug = {lesson.get("slug"): lesson for lesson in lessons}
    write_manifest(args.output_dir, list(by_slug.values()), "running", {"model": args.model})

    for index, video_path in enumerate(videos, start=1):
        slug = f"{lesson_number(video_path):02d}_{slugify(video_path.stem)}"
        raw_path = paths["raw"] / f"{slug}.json"
        duration = probe_duration(video_path)
        print(f"[{index}/{len(videos)}] {video_path.name} ({fmt_time(duration)})", flush=True)

        started = time.time()
        try:
            if args.overwrite or not raw_path.exists():
                transcribe_video(video_path, slug, raw_path, paths, args)
            lesson = write_lesson_files(video_path, slug, raw_path, paths, duration)
            lesson["transcription_seconds"] = round(time.time() - started, 2)
            by_slug[slug] = lesson
            write_manifest(args.output_dir, list(by_slug.values()), "running", {"model": args.model})
        except Exception as exc:
            write_manifest(
                args.output_dir,
                list(by_slug.values()),
                "error",
                {"model": args.model, "failed_video": str(video_path), "error": str(exc)},
            )
            raise

    write_manifest(args.output_dir, list(by_slug.values()), "complete", {"model": args.model})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
