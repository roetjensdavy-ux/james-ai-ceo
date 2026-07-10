#!/usr/bin/env python3
"""
Decode frontend assets from compressed base64 chunks.
Run after cloning the repo: python3 decode_frontend.py
"""
import os
import base64
import gzip

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend_assets")
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")

def decode_chunk(filename):
    """Read a gzipped base64 file and return decoded bytes."""
    filepath = os.path.join(ASSETS_DIR, filename)
    with open(filepath, 'r') as f:
        b64_data = f.read()
    gzipped = base64.b64decode(b64_data)
    return gzip.decompress(gzipped)

def main():
    os.makedirs(os.path.join(FRONTEND_DIR, "assets"), exist_ok=True)

    # Decode CSS
    print("[1/2] Decoding CSS...")
    css_data = decode_chunk("index.css.gz.b64")
    css_path = os.path.join(FRONTEND_DIR, "assets", "index.css")
    with open(css_path, 'wb') as f:
        f.write(css_data)
    print(f"      CSS: {len(css_data)} bytes -> {css_path}")

    # Decode JS (combine chunks)
    print("[2/2] Decoding JS (combining chunks)...")
    js_parts = []
    for letter in ['aa', 'ab', 'ac', 'ad', 'ae']:
        chunk_data = decode_chunk(f"index.js.{letter}.gz.b64")
        js_parts.append(chunk_data)
        print(f"      Part {letter}: {len(chunk_data)} bytes")

    # Combine base64 parts and decode
    full_b64 = b''.join(js_parts)
    js_data = base64.b64decode(full_b64)
    js_path = os.path.join(FRONTEND_DIR, "assets", "index.js")
    with open(js_path, 'wb') as f:
        f.write(js_data)
    print(f"      JS: {len(js_data)} bytes -> {js_path}")

    print("\nFrontend assets decoded successfully!")
    print(f"Output: {FRONTEND_DIR}/")

if __name__ == "__main__":
    main()
