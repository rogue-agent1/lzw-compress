#!/usr/bin/env python3
"""lzw_compress - LZW compression (used in GIF, Unix compress)."""
import sys
def compress(data):
    dict_size=256; dictionary={chr(i):i for i in range(dict_size)}
    w=""; result=[]
    for c in data:
        wc=w+c
        if wc in dictionary: w=wc
        else:
            result.append(dictionary[w]); dictionary[wc]=dict_size; dict_size+=1; w=c
    if w: result.append(dictionary[w])
    return result
def decompress(compressed):
    dict_size=256; dictionary={i:chr(i) for i in range(dict_size)}
    w=chr(compressed[0]); result=[w]
    for code in compressed[1:]:
        if code in dictionary: entry=dictionary[code]
        elif code==dict_size: entry=w+w[0]
        else: raise ValueError(f"Bad code: {code}")
        result.append(entry); dictionary[dict_size]=w+entry[0]; dict_size+=1; w=entry
    return "".join(result)
if __name__=="__main__":
    text=sys.argv[1] if len(sys.argv)>1 else "TOBEORNOTTOBEORTOBEORNOT"
    compressed=compress(text); decompressed=decompress(compressed)
    orig_bits=len(text)*8; comp_bits=len(compressed)*12
    print(f"Original: {text} ({orig_bits} bits)")
    print(f"Compressed: {len(compressed)} codes ({comp_bits} bits, ratio: {comp_bits/orig_bits:.1%})")
    print(f"Decompressed: {decompressed} (match: {decompressed==text})")
