"""Every number in index.html's SNAP_ROWS against the source page's table (data/live-wall.json,
from checks/parse_live.py), compared as the table's text, for every decoder."""
import re, json
src = open("index.html").read()
i = src.index("const SNAP_ROWS = ") + len("const SNAP_ROWS = ")
snap = json.loads(re.sub(r",\s*\]$", "]", src[i:src.index("];", i) + 1]))
live = json.load(open("data/live-wall.json"))
H = [h.rstrip(" ¹") for h in live["heads"]]
n = bad = 0
for r in live["rows"]:
    corpus, size = re.fullmatch(r"(\S+) \(([^,]+), [\d.]+×\)", r[0]).groups()
    s = [x for x in snap if x[0] == corpus and x[2] == int(r[1])]
    if len(s) != 1: bad += 1; print("no single snapshot row for", corpus, r[1]); continue
    s = s[0]
    pairs = [(s[1], size), (s[3], float(r[2].removesuffix(" s"))), (s[4], float(r[3]))]
    for d, x in s[5].items():
        lo = re.fullmatch(r"([\d.]+)× \(([\d.]+)–([\d.]+)\)", r[H.index(d)]).groups()
        pairs += list(zip(x, map(float, lo)))
    for a, b in pairs:
        n += 1
        if a != b: bad += 1; print("DIFF", corpus, r[1], a, b)
decs = set(H) & set(snap[0][5])
print(f"{len(snap)} snapshot rows, {len(live['rows'])} table rows, {len(decs)} decoders; {n} values compared, {bad} differ")
raise SystemExit(1 if bad else 0)
