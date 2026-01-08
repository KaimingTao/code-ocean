import csv
from pathlib import Path


def is_text_file(path):
    try:
        with path.open("rb") as f:
            chunk = f.read(8192)
    except OSError:
        return False
    if b"\x00" in chunk:
        return False
    try:
        chunk.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def load_index(path):
    if not path.exists():
        return ["Path"], []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return ["Path"], []
    return rows[0], rows[1:]


def save_index(path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    cwd = Path.cwd()
    index_path = cwd / "INDEX.csv"
    headers, rows = load_index(index_path)

    path_index = next(
        (idx for idx, name in enumerate(headers) if name.strip().lower() == "path"),
        None,
    )
    if path_index is None:
        headers.append("Path")
        path_index = len(headers) - 1
    else:
        headers[path_index] = "Path"

    normalized_rows = []
    existing_paths = set()
    for row in rows:
        row = row + [""] * (len(headers) - len(row))
        normalized_rows.append(row)
        existing_paths.add(row[path_index])

    for item in sorted((cwd / 'code').rglob("*")):
        if not item.is_file():
            continue
        if not is_text_file(item):
            continue
        rel_path = item.relative_to(cwd).as_posix()
        if rel_path in existing_paths:
            continue
        new_row = [""] * len(headers)
        new_row[path_index] = rel_path
        normalized_rows.append(new_row)
        existing_paths.add(rel_path)

    save_index(index_path, headers, normalized_rows)


if __name__ == "__main__":
    main()
