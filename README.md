# Custom Hash Function — Demo

This repository contains:
- `custom_hash.py` — educational custom hash implementation
- `run_tests.py` — runs tests and writes CSV outputs to `results/`
- `results/` — (created after running `run_tests.py`) contains `hash_results.csv`, `avalanche_results.csv`

## Usage

1. Ensure you have Python 3.8+.
2. (Optional) create a venv:
   ```
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```
3. Run:
   ```
   python run_tests.py
   ```
4. Open `results/hash_results.csv` and `results/avalanche_results.csv`.

## Notes

This custom hash is for learning and demonstration only. It is **not** cryptographically secure. Use `hashlib` (SHA-256, SHA-3) for real security needs.
