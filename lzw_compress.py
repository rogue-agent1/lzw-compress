#!/usr/bin/env python3
"""LZW compression/decompression."""
import sys
def compress(data):
    d={chr(i):i for i in range(256)};nc=256;w="";out=[]
    for c in data:
        wc=w+c
        if wc in d: w=wc
        else: out.append(d[w]);d[wc]=nc;nc+=1;w=c
    if w: out.append(d[w])
    return out
def decompress(codes):
    d={i:chr(i) for i in range(256)};nc=256;w=chr(codes[0]);out=[w]
    for code in codes[1:]:
        if code in d: entry=d[code]
        elif code==nc: entry=w+w[0]
        else: raise ValueError(f"Bad code: {code}")
        out.append(entry);d[nc]=w+entry[0];nc+=1;w=entry
    return ''.join(out)
def main():
    if "--demo" in sys.argv:
        text="TOBEORNOTTOBEORTOBEORNOT"
        codes=compress(text);dec=decompress(codes)
        ratio=len(codes)*12/8/len(text)*100
        print(f"Original:     '{text}' ({len(text)} bytes)")
        print(f"Compressed:   {len(codes)} codes ({ratio:.0f}% of original at 12-bit)")
        print(f"Decompressed: '{dec}'")
        print(f"Match: {'✓' if dec==text else '✗'}")
    else:
        data=sys.stdin.read();codes=compress(data)
        print(f"Compressed {len(data)} chars to {len(codes)} codes")
if __name__=="__main__": main()
