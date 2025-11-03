"""
run_tests.py

Runs a set of tests for custom_hash.py, writes CSV outputs and a short report.
"""
import csv
import os
from custom_hash import custom_hash, sha256_hex, hamming_distance_hex

out_dir = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(out_dir, exist_ok=True)

tests = [
    ("empty_string", ""),
    ("short_hello", "hello"),
    ("short_hello_cap", "Hello"),
    ("hello_space", "hello "),
    ("hello_extra", "hello!"),
    ("long_text", "The quick brown fox jumps over the lazy dog" * 10),
    ("single_char_a", "a"),
    ("single_char_b", "b"),
    ("incremental1", "password1"),
    ("incremental2", "password2"),
    ("similar1", "This is a test."),
    ("similar2", "This is a test!"),
]

# Write hash_results.csv
csv_path = os.path.join(out_dir, "hash_results.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["case","input","custom_128_hex","sha256_hex"])
    writer.writeheader()
    for name, txt in tests:
        custom = custom_hash(txt, out_hex_len=32)
        sha = sha256_hex(txt)
        writer.writerow({
            "case": name,
            "input": txt,
            "custom_128_hex": custom,
            "sha256_hex": sha
        })

# Avalanche pairs
pairs = [
    ("hello","Hello"),
    ("password1","password2"),
    ("This is a test.","This is a test!"),
    ("a","b"),
    (""," "),
]
av_path = os.path.join(out_dir, "avalanche_results.csv")
with open(av_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["input_a","input_b","custom_a","custom_b","custom_hamming","sha256_hamming"])
    writer.writeheader()
    for a,b in pairs:
        c1 = custom_hash(a, out_hex_len=32)
        c2 = custom_hash(b, out_hex_len=32)
        s1 = sha256_hex(a)
        s2 = sha256_hex(b)
        writer.writerow({
            "input_a": a,
            "input_b": b,
            "custom_a": c1,
            "custom_b": c2,
            "custom_hamming": hamming_distance_hex(c1, c2),
            "sha256_hamming": hamming_distance_hex(s1, s2),
        })

# Short textual report
report_path = os.path.join(out_dir, "report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("Custom Hash Demo Report\\n")
    f.write("Results written to:\\n")
    f.write(" - " + csv_path + "\\n")
    f.write(" - " + av_path + "\\n")

print("Results written to:", out_dir)
