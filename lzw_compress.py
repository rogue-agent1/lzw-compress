#!/usr/bin/env python3
"""LZW compression/decompression — zero deps."""

def lzw_compress(data):
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256; w = ""; output = []
    for c in data:
        wc = w + c
        if wc in dictionary: w = wc
        else: output.append(dictionary[w]); dictionary[wc] = next_code; next_code += 1; w = c
    if w: output.append(dictionary[w])
    return output

def lzw_decompress(codes):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256; w = chr(codes[0]); output = [w]
    for code in codes[1:]:
        if code in dictionary: entry = dictionary[code]
        elif code == next_code: entry = w + w[0]
        else: raise ValueError(f"Bad code: {code}")
        output.append(entry)
        dictionary[next_code] = w + entry[0]
        next_code += 1; w = entry
    return ''.join(output)

def test():
    text = "TOBEORNOTTOBEORTOBEORNOT"
    compressed = lzw_compress(text)
    decompressed = lzw_decompress(compressed)
    assert decompressed == text
    ratio = len(compressed) / len(text)
    print(f"Original: {len(text)} chars → Compressed: {len(compressed)} codes (ratio: {ratio:.2f})")
    # Highly repetitive = better compression
    rep = "AAAAAAAAAAAAAAAAAAAAAAAAA"
    c2 = lzw_compress(rep)
    assert len(c2) < len(rep)
    assert lzw_decompress(c2) == rep
    print("All tests passed!")

if __name__ == "__main__": test()
