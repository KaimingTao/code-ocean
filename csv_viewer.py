import csv
import tkinter as tk
from tkinter import ttk
from pathlib import Path


def load_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], []
    headers = rows[0]
    data = rows[1:]
    return headers, data


def build_table(parent, headers, data):
    tree = ttk.Treeview(parent, columns=headers, show="headings")

    for col in headers:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="w", stretch=True)

    for row in data:
        # Normalize row length to headers to avoid tree errors.
        row = row + [""] * (len(headers) - len(row))
        tree.insert("", "end", values=row[: len(headers)])

    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    parent.grid_rowconfigure(1, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    return tree


def normalize_path_value(value):
    value = value.strip()
    if value.startswith("/"):
        value = f".{value}"
    return value


def ensure_path_exists(value):
    if not value:
        return
    raw_value = value
    is_dir = raw_value.endswith(("/", "\\"))
    path = Path.cwd() / raw_value
    if is_dir or path.suffix == "":
        path.mkdir(parents=True, exist_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def main():
    csv_path = Path(__file__).with_name("INDEX.csv")
    headers, data = load_csv(csv_path)

    root = tk.Tk()
    root.title(f"CSV Viewer - {csv_path.name}")
    root.geometry("900x600")

    style = ttk.Style()
    style.configure("Treeview", rowheight=28)

    container = ttk.Frame(root, padding=8)
    container.pack(fill="both", expand=True)

    if not headers:
        label = ttk.Label(container, text=f"No data found in {csv_path.name}")
        label.pack()
    else:
        tree = build_table(container, headers, data)
        path_index = next(
            (idx for idx, name in enumerate(headers) if name.strip().lower() == "path"),
            None,
        )

        toolbar = ttk.Frame(container)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        def add_row():
            tree.insert("", "end", values=[""] * len(headers))

        def delete_row():
            for item in tree.selection():
                tree.delete(item)

        def begin_edit(event):
            region = tree.identify("region", event.x, event.y)
            if region != "cell":
                return
            row_id = tree.identify_row(event.y)
            col_id = tree.identify_column(event.x)
            if not row_id or not col_id:
                return
            col_index = int(col_id.replace("#", "")) - 1
            x, y, width, height = tree.bbox(row_id, col_id)
            if width <= 0 or height <= 0:
                return

            value = tree.set(row_id, headers[col_index])
            entry = ttk.Entry(tree)
            entry.insert(0, value)
            entry.select_range(0, "end")
            entry.focus_set()
            entry.place(x=x, y=y, width=width, height=height)

            def save_edit(_event=None):
                value = entry.get()
                if path_index is not None and col_index == path_index:
                    value = normalize_path_value(value)
                    ensure_path_exists(value)
                tree.set(row_id, headers[col_index], value)
                entry.destroy()

            def cancel_edit(_event=None):
                entry.destroy()

            entry.bind("<Return>", save_edit)
            entry.bind("<FocusOut>", save_edit)
            entry.bind("<Escape>", cancel_edit)

        add_button = ttk.Button(toolbar, text="Add Row", command=add_row)
        delete_button = ttk.Button(toolbar, text="Delete Row", command=delete_row)
        add_button.pack(side="left")
        delete_button.pack(side="left", padx=(6, 0))

        tree.bind("<Double-1>", begin_edit)

    root.mainloop()


if __name__ == "__main__":
    main()
