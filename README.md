# mibz2 against the common bzip2 decoders

**Page: https://samshackleton-tech.github.io/mibz2-vs-common/**

A one-page chart of [mibz2](https://github.com/lmmx/mibz2)'s decode time against lbzip2,
libbzip2 and libbz2-rs (and, one click away, all nine decoders mibz2's benchmark measures),
from the benchmark record of commit
[`ae942bd`](https://github.com/lmmx/mibz2/commit/ae942bdb135569224473116ffaa706f1c9e389ed).
Each bar is drawn in blocks of mibz2's own time on that corpus, so a bar of three blocks is a
decoder taking three times as long.

The page is one self-contained file (`index.html`, no dependencies). By default it fetches
[the mibz2 site's alternatives page](https://lmmx.github.io/mibz2/benchmarks/alternatives/),
reads its "Wall time against mibz2" table, and checks it value for value against the snapshot
built into the page. URL parameters:

| parameter | effect |
|---|---|
| `?pinned` | the built-in snapshot only, no network |
| `?threads=1` / `2` / `4` | mibz2's thread count |
| `?show=all` | all ten decoders, not the common four |
| `?source=URL` | read another page rendering the same table (a fork's site) |
| `?data=URL` | load a `data.json` saved from the page (schema `mibz2-alt-subset/2`) |

## How it was checked

| check | result |
|---|---|
| `checks/compare_snapshot.py`: the snapshot against the source table, every decoder | 630 values, 0 differ |
| `checks/recompute.py`: every ratio and 95% interval recomputed from the 1,540 raw runs (`data/raw.jsonl`, the record's own blob `0eba6ba1…`) | 567 values agree to the table's last digit; 2 differ only in rounding a tie |
| The provenance (commit, tree, signature, PR, workflow, run, job, artifact, record blobs, crate checksums) | read back from git and the GitHub API, 2026-11-02 |

## Files

- `src/page.html`: the page, with `__SNAP_ROWS__` where the snapshot goes.
- `build.py`: writes `index.html`, filling the snapshot from `data/live-wall.json`.
- `checks/parse_live.py`: reads the table out of a saved copy of the source page
  (`data/alternatives.html`, fetched 2026-11-02T03:26:26Z; headers in
  `data/alternatives.headers.txt`) into `data/live-wall.json`.
- `data/record.json`, `data/raw.jsonl`: the record's summary and raw runs, from the mibz2
  repository's `bench-results` branch at
  [`a02eaf65`](https://github.com/lmmx/mibz2/commit/a02eaf65a8b2c65be4dc53f8622558d3c8a89564)
  (git blobs `d0ae7649…` and `0eba6ba1…`).

To rebuild and check:

```sh
python3 checks/parse_live.py data/alternatives.html
python3 build.py
python3 checks/compare_snapshot.py
python3 checks/recompute.py
```

## Corrections to v1.1.0

The page began as `mibz2-vs-common.html` v1.1.0, written in a chat session. v2.0.0:

- **It rendered nothing:** a syntax error (`e.append(.kids…)`) stopped the script, so only the
  header showed. Once that was fixed, the thread buttons read `[object HTMLButtonElement]`, the
  footer read `ae942bdnull`, and the live lbzip2 version read `?`.
- **"4 cores" is 4 CPUs on 2 cores** (the record's `env`: `cpus 4, cores 2`). The 4-thread
  runs share each core between two hardware threads. The source page has the same wording.
- **The "not captured" list** named the kernel, the image and the synthetic corpora's
  checksums, which the record holds; they are now on the page.
- **The other six decoders** measured in the same run are one click away, and the page says
  where any of them is faster than mibz2, by the whole 95% interval: pbz2 on `onebyte` and
  `runs` at every thread count and on `records` at 2; bz2ngrs on `runs` at 2 and 4 threads and
  on `onebyte` at 4.
- A headline, corpus descriptions, a legend, dark mode and a phone layout.

## License

MIT OR Apache-2.0, as mibz2. `data/` holds copies of mibz2's own benchmark output and site page.
