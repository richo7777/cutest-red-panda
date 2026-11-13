# Cutest picture entry for make.fun (cutest-picture-01).
# Python 3.13, standard library only. Copies the bundled picture to the
# grader's output directory. Deterministic: the same bytes every run.
# Run locally: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
dest = os.path.join(OUTPUT_DIR, "entry.png")
shutil.copyfile(SOURCE, dest)
# Guardrail: the entry must stay a valid picture within the bounty limits
# (at most 1 MiB and 1024 by 1024). Fail loudly instead of shipping a
# broken or oversized file.
size = os.path.getsize(dest)
assert size <= 1048576, f"entry.png too large: {size} bytes"
with open(dest, "rb") as f:
    header = f.read(33)
assert header[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG"
width = int.from_bytes(header[16:20], "big")
height = int.from_bytes(header[20:24], "big")
assert width <= 1024 and height <= 1024, f"entry.png too big: {width}x{height}"
