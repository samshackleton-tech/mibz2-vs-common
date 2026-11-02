"""Build index.html from src/page.html, filling SNAP_ROWS from the source page's table.

    python3 checks/parse_live.py data/alternatives.html   # writes data/live-wall.json from a saved copy of
                                                     # https://lmmx.github.io/mibz2/benchmarks/alternatives/
    python3 build.py                                 # writes index.html

Every value is the table's own text, parsed as a number; nothing is derived or rounded."""
import json, os, re
DECODERS = ["lbzip2", "libbz2-rs", "libbzip2", "pbz2", "indexed_bzip2", "fbz", "lbzip2-rs", "bz2ngrs", "bz2ng"]
live = json.load(open("data/live-wall.json"))
heads = [h.rstrip(" ¹") for h in live["heads"]]
ratio = lambda s: [float(x) for x in re.fullmatch(r"([\d.]+)× \(([\d.]+)–([\d.]+)\)", s).groups()]
rows = []
for r in live["rows"]:
    m = re.fullmatch(r"(\S+) \(([^,]+), [\d.]+×\)", r[0])
    rows.append([m.group(1), m.group(2), int(r[1]), float(r[2].removesuffix(" s")), float(r[3]),
                 {d: ratio(r[heads.index(d)]) for d in DECODERS}])
assert len(rows) == 21 and all(r[-1] == "yes" for r in live["rows"])
lit = "[\n" + "".join("  " + json.dumps(r, ensure_ascii=False) + ",\n" for r in rows) + "]"
page = open("src/page.html").read()
assert page.count("__SNAP_ROWS__") == 1 and page.count("__HOME__") == 1
# This repository's page, and the copy for mibz2's own site (docs/site/benchmarks/vs-common.html).
for out, home in [("index.html", "https://samshackleton-tech.github.io/mibz2-vs-common/"),
                  ("upstream/vs-common.html", "https://lmmx.github.io/mibz2/benchmarks/vs-common.html")]:
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    open(out, "w").write(page.replace("__SNAP_ROWS__", lit).replace("__HOME__", home))
    print(f"{out}: {len(rows)} rows, {sum(3 * len(r[5]) + 2 for r in rows)} values")
