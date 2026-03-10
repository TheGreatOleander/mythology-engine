from pathlib import Path
class SubtitleEngine:
    def generate(self, lines):
        out = Path("examples/releases/output/captions.srt")
        out.parent.mkdir(parents=True, exist_ok=True)
        parts = []
        t = 0
        for i, line in enumerate(lines, 1):
            parts.append(f"{i}\n00:00:{t:02},000 --> 00:00:{t+3:02},000\n{line}\n")
            t += 3
        out.write_text("\n".join(parts), encoding="utf-8")
        return str(out)
