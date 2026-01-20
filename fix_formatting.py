from pathlib import Path

FILES = [
    Path("battle_ships/ai.py"),
    Path("battle_ships/board.py"),
    Path("battle_ships/game.py"),
    Path("battle_ships/main.py"),
    Path("battle_ships/utils.py"),
]

for file_path in FILES:
    if not file_path.exists():
        print(f"SKIP (not found): {file_path}")
        continue

    # Read as raw text, then normalise line endings to LF
    text = file_path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing whitespace from every line
    lines = [line.rstrip(" \t") for line in text.split("\n")]

    # Remove ALL empty/whitespace-only lines at end of file
    while lines and lines[-1].strip(" \t") == "":
        lines.pop()

    # Write back with exactly ONE newline at end of file
    cleaned = "\n".join(lines) + "\n"
    file_path.write_text(cleaned, encoding="utf-8")

    print(f"FIXED: {file_path}")

print("Formatting cleanup complete.")
