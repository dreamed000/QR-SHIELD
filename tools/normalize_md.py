import sys
from pathlib import Path


def normalize_md(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Trim trailing spaces
        line = line.rstrip()

        # Normalize code fence start
        if line.strip().startswith("```"):
            # ensure blank line before fence
            if out and out[-1].strip() != "":
                out.append("")
            # ensure language specified
            if line.strip() == "```":
                line = "```text"
            out.append(line)
            i += 1
            # copy until closing fence
            while i < len(lines):
                out.append(lines[i])
                if lines[i].strip().startswith("```"):
                    # ensure blank line after closing fence
                    if i + 1 < len(lines) and lines[i + 1].strip() != "":
                        out.append("")
                    i += 1
                    break
                i += 1
            continue
        # Ensure blank line before and after any heading
        if line.lstrip().startswith("#"):
            # remove trailing colon from headings (MD026)
            if line.rstrip().endswith(":"):
                line = line.rstrip()[:-1]
            if out and out[-1].strip() != "":
                out.append("")
            out.append(line)
            # Ensure there's a blank line after heading if next line isn't blank
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                out.append("")
            i += 1
            continue

        # Normalize table separators like '|--------|----|' to '| --- | --- |'
        if line.strip().startswith("|") and set(line.strip()) <= set("|- "):
            cols = line.count("|") - 1
            sep = "| " + " | ".join(["---"] * cols) + " |"
            out.append(sep)
            i += 1
            continue

        # Ensure blank lines around list items and normalize ordered list numbering
        # to '1.'
        stripped_line = line.lstrip()
        if stripped_line.startswith(("-", "*")) or (
            stripped_line and stripped_line.split()[0].rstrip(".").isdigit()
        ):
            if out and out[-1].strip() != "":
                out.append("")
            # normalize ordered list numbers to '1.'
            stripped = stripped_line
            if stripped and stripped[0].isdigit():
                parts = stripped.split(".", 1)
                if len(parts) > 1 and parts[0].isdigit():
                    line = line.replace(parts[0] + ".", "1.", 1)
            out.append(line)
            # ensure a blank line after list block (peek ahead)
            if i + 1 < len(lines) and lines[i + 1].strip() != "":
                out.append("")
            i += 1
            continue
        out.append(line)
        i += 1
    new_text = "\n".join(out).rstrip() + "\n"
    path.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: normalize_md.py <file1.md> [file2.md ...]")
        sys.exit(2)
    for p in sys.argv[1:]:
        normalize_md(Path(p))
        print("Normalized", p)
