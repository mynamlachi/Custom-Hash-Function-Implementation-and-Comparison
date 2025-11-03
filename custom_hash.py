"""
custom_hash.py

A learning-oriented custom hash implementation (not cryptographically secure).
Provides:
- custom_hash(plaintext, out_hex_len=32)
- sha256_hex(plaintext)
- hamming_distance_hex(h1, h2)

Author: Generated for user by ChatGPT
"""

import struct
import hashlib

def rotl32(x, r):
    return ((x << r) & 0xFFFFFFFF) | (x >> (32 - r))

def custom_hash(plaintext: str, out_hex_len: int = 32) -> str:
    """
    Custom educational hash function (128-bit default output -> 32 hex chars).
    Not intended for production cryptography.
    Parameters:
      plaintext: input string
      out_hex_len: number of hex chars in output (even number, <= 64)
    Returns:
      hex string of length out_hex_len
    """
    if out_hex_len % 2 != 0 or out_hex_len < 2:
        raise ValueError("out_hex_len must be even and >= 2")
    max_hex = 64
    if out_hex_len > max_hex:
        raise ValueError(f"out_hex_len must be <= {max_hex}")

    data = plaintext.encode('utf-8')
    length = len(data)

    # Initialize 128-bit state with constants XORed with length
    state = [
        0x243F6A88 ^ (length & 0xFFFFFFFF),
        0x85A308D3 ^ ((length << 8) & 0xFFFFFFFF),
        0x13198A2E ^ ((length << 16) & 0xFFFFFFFF),
        0x03707344 ^ ((length << 24) & 0xFFFFFFFF),
    ]

    i = 0
    while i < length:
        block = data[i:i+16]
        pad_len = 16 - len(block)
        if pad_len:
            block = block + bytes([(pad_len * 31) & 0xFF]) * pad_len
        words = list(struct.unpack(">LLLL", block))

        for r in range(4):
            for j in range(4):
                b0 = (words[j] >> 24) & 0xFF
                shift = (b0 % 31) + 1
                words[j] = rotl32((words[j] + state[j] + (j*0x9E3779B1 & 0xFFFFFFFF)) & 0xFFFFFFFF, shift) ^ ((words[(j+1)%4] * 0x5bd1e995) & 0xFFFFFFFF)
            for j in range(4):
                state[j] = rotl32((state[j] + words[j]) & 0xFFFFFFFF, (r*7 + j*3) % 32) ^ ((state[(j+1)%4] + 0x6A09E667) & 0xFFFFFFFF)
        i += 16

    a = state[0] ^ ((state[1] << 5) & 0xFFFFFFFF) ^ (state[2] >> 7)
    b = state[1] ^ ((state[2] << 3) & 0xFFFFFFFF) ^ (state[3] >> 11)
    c = state[2] ^ ((state[3] << 7) & 0xFFFFFFFF) ^ (state[0] >> 13)
    d = state[3] ^ ((state[0] << 11) & 0xFFFFFFFF) ^ (state[1] >> 3)
    final_bytes = struct.pack(">LLLL", a & 0xFFFFFFFF, b & 0xFFFFFFFF, c & 0xFFFFFFFF, d & 0xFFFFFFFF)

    needed_bytes = out_hex_len // 2
    out = bytearray()
    counter = 0
    while len(out) < needed_bytes:
        ctr_word = (counter & 0xFFFFFFFF)
        block = bytearray(final_bytes)
        for idx in range(len(block)):
            block[idx] = (block[idx] ^ ((ctr_word >> ((idx%4)*8)) & 0xFF) + 0xA3) & 0xFF
        out.extend(block)
        counter += 1
    out = out[:needed_bytes]
    return out.hex()[:out_hex_len]

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def hamming_distance_hex(h1: str, h2: str) -> int:
    b1 = bytes.fromhex(h1)
    b2 = bytes.fromhex(h2)
    L = max(len(b1), len(b2))
    b1 = b1.ljust(L, b'\x00')
    b2 = b2.ljust(L, b'\x00')
    dist = 0
    for x,y in zip(b1,b2):
        dist += bin(x ^ y).count('1')
    return dist

if __name__ == "__main__":
    samples = ["", "hello", "Hello", "The quick brown fox"]
    for s in samples:
        print(f"Input: {repr(s)}")
        print("  custom:", custom_hash(s, out_hex_len=32))
        print("  sha256:", sha256_hex(s))
        print()
