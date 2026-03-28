#!/usr/bin/env python3
"""lzw_compress - LZW compression/decompression."""
import sys, struct

def compress(data):
    d = {bytes([i]): i for i in range(256)}
    next_code = 256; w = b""; codes = []
    for byte in data:
        wb = w + bytes([byte])
        if wb in d: w = wb
        else: codes.append(d[w]); d[wb] = next_code; next_code += 1; w = bytes([byte])
    if w: codes.append(d[w])
    return codes

def decompress(codes):
    d = {i: bytes([i]) for i in range(256)}
    next_code = 256; w = d[codes[0]]; result = [w]
    for code in codes[1:]:
        if code in d: entry = d[code]
        elif code == next_code: entry = w + w[:1]
        else: raise ValueError(f"Bad code: {code}")
        result.append(entry)
        d[next_code] = w + entry[:1]; next_code += 1; w = entry
    return b"".join(result)

if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: lzw_compress.py <compress|decompress> <file> [output]"); sys.exit(1)
    cmd = sys.argv[1]; inf = sys.argv[2]; outf = sys.argv[3] if len(sys.argv) > 3 else None
    if cmd == "compress":
        data = open(inf, "rb").read()
        codes = compress(data)
        out = struct.pack(f">{len(codes)}H", *codes)
        if outf: open(outf, "wb").write(out); print(f"{len(data)} → {len(out)} bytes ({len(out)/len(data)*100:.1f}%)")
        else: print(f"Codes: {len(codes)}, ratio: {len(codes)*2/len(data)*100:.1f}%")
    elif cmd == "decompress":
        raw = open(inf, "rb").read()
        codes = list(struct.unpack(f">{len(raw)//2}H", raw))
        data = decompress(codes)
        if outf: open(outf, "wb").write(data); print(f"Decompressed: {len(data)} bytes")
        else: sys.stdout.buffer.write(data)
