# Spec

## CSV Viewer GUI
- Build a Python GUI that loads `INDEX.csv` and renders a table with a vertical scrollbar.
- Add editing: add row, delete row, update a cell (in-place edit).
- Increase row height for better readability.
- When the `path` column is added or edited:
  - Treat it as relative to the current folder.
  - If the value starts with `/`, auto-insert `.` (e.g., `/foo` -> `./foo`) after editing.
  - Create a folder or file based on the path:
    - If it ends with `/` (or has no file extension), create a folder.
    - Otherwise create the file, ensuring parent folders exist.

## Index Text Files
- Create another Python program that scans the current folder for text files.
- Insert each text file path into `INDEX.csv` if it does not already exist.
  - Ensure there is a `path` column (add it if missing).
  - Only add missing paths.
