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
# (at most 1 MiB and 1024 by 1024). The file may be PNG or JPEG — told
# apart by its first bytes, the name stays entry.png either way. Fail
# loudly instead of shipping a broken or oversized file.
size = os.path.getsize(dest)
assert size <= 1048576, f"entry.png too large: {size} bytes"
with open(dest, "rb") as f:
    header = f.read(2)
    if header == b"\xff\xd8":  # JPEG: scan markers for the SOF frame size
        with open(dest, "rb") as g:
            data = g.read()
        width = height = None
        i = 2
        while i < len(data) - 1:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):  # SOF0/1/2
                height = int.from_bytes(data[i + 5:i + 7], "big")
                width = int.from_bytes(data[i + 7:i + 9], "big")
                break
            seg_len = int.from_bytes(data[i + 2:i + 4], "big")
            i += 2 + seg_len
        assert width and height, "could not read JPEG dimensions"
    else:
        with open(dest, "rb") as g:
            header = g.read(33)
        assert header[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a PNG or JPEG"
        width = int.from_bytes(header[16:20], "big")
        height = int.from_bytes(header[20:24], "big")
assert width <= 1024 and height <= 1024, f"entry.png too big: {width}x{height}"
