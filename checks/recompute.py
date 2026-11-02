"""Recompute the wall-time ratios (alternative / mibz2: geometric mean of the rounds' paired ratios,
95% interval) from the raw rounds, and compare them with the site's table (data/live-wall.json).
Single-threaded arms: their 1-thread run in the same round against mibz2 at T threads."""
import json, math, re, statistics as st, collections
raw = [json.loads(l) for l in open('data/raw.jsonl')]
rec = json.load(open('data/record.json'))
wall = {(r['round'], r['corpus'], r['threads'], r['arm'].split('@')[0]): r['wall'] for r in raw if not r['err']}  # 'fbz@alts/ab' -> 'fbz'
T95 = {9: 2.262, 8: 2.306, 7: 2.365}
live = json.load(open('data/live-wall.json')); H = [h.rstrip(' ¹') for h in live['heads']]
parse = lambda s: [float(x) for x in re.match(r'([\d.]+)× \(([\d.]+)–([\d.]+)\)', s).groups()]
n = bad = 0; worst = 0
for row in live['rows']:
    corpus = row[0].split()[0]; t = int(row[1])
    # mibz2's median wall
    mw = [wall[(k, corpus, t, 'mibz2')] for k in range(10) if (k, corpus, t, 'mibz2') in wall]
    site_med = float(row[2].rstrip(' s'))
    if abs(st.median(mw) - site_med) > 0.0005: print('median DIFF', corpus, t, st.median(mw), site_med)
    for arm in ('lbzip2', 'libbz2-rs', 'libbzip2', 'pbz2', 'bz2ngrs', 'bz2ng', 'fbz', 'indexed_bzip2', 'lbzip2-rs'):
        ta = t if rec['parallel'][arm] else 1
        logs = [math.log(wall[(k, corpus, ta, arm)] / wall[(k, corpus, t, 'mibz2')]) for k in range(10)
                if (k, corpus, ta, arm) in wall and (k, corpus, t, 'mibz2') in wall]
        m = st.mean(logs); h = T95[len(logs) - 1] * st.stdev(logs) / math.sqrt(len(logs))
        mine = [math.exp(m), math.exp(m - h), math.exp(m + h)]
        site = parse(row[H.index(arm)])
        for a, b in zip(mine, site):
            n += 1; d = abs(round(a, 2) - b); worst = max(worst, d)
            if d > 0.0051: bad += 1; print('DIFF', corpus, t, arm, [round(x, 3) for x in mine], site)
print(f'{n} values recomputed from {len(raw)} raw rows; {bad} differ by more than 0.01 after rounding; worst {worst:.3f}')
