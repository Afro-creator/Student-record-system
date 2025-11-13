# Student Record System

Simple command-line student record system implemented in Python. Stores student records (id, name, age, major, GPA, email) in a JSON file and provides basic CRUD + search operations via an interactive menu.

## Features
- Add, list, view, update, delete student records
- Search students by name (case-insensitive substring)
- Persistent storage in `students.json` next to the script
- Minimal validations for numeric inputs

## Requirements
- Python 3.8+

No external packages required.

## Usage (Windows)
1. Open a terminal (PowerShell or CMD).
2. Change to the folder containing `Practice.py`:
   cd "C:\Users\KOECH\Desktop"
3. Run the script:
   python Practice.py
4. Follow the interactive menu.

## Data file
- Records are saved to `students.json` in the same directory as `Practice.py`.
- The file is JSON-formatted and human-readable.

## Notes and improvements
- The loader currently attempts to construct Student objects directly from JSON; malformed/corrupt files will be ignored and the database reset. Consider adding validation and error reporting.
- Writes are not atomic; consider writing to a temp file and renaming to avoid corruption.
- Add validation for fields (e.g., GPA range, email format) and unit tests for persistence logic.

## License
Unlicensed — adapt freely for learning and experimentation.