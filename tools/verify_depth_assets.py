#!/usr/bin/env python3
"""Read-only integrity check of the v4.0-depth release assets.

Usage:  python3 -I tools/verify_depth_assets.py FOLDER_WITH_DOWNLOADED_ASSETS

Standard library only. It never runs the engine. It checks:
  1. every release asset against depth/RELEASE_ASSETS.json;
  2. every one of the 462 retained layer archives (5 cases x 68 layers, interface
     x 128, minus the 6 lost ones) against the authenticated hash in
     depth/LAYER_INDEX.json, opening nested ZIP files where needed;
  3. the verification replay of the 6 lost archives: each replayed receipt cites
     the receipts of the previous layer (starting from the last authenticated
     production layer), and the replayed layer 68 has the same state, emissions
     and time_dependencies hashes as production layer 68, for all 36 cells.
Exit code 0 only if everything passes.
"""
import hashlib, io, json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'depth'
assets = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
failures = []

def sha(b): return hashlib.sha256(b).hexdigest()

def open_chain(chain):
    z = zipfile.ZipFile(assets / chain[0])
    data = None
    for name in chain[1:]:
        data = z.read(name)
        if name != chain[-1]:
            z = zipfile.ZipFile(io.BytesIO(data))
    return data

def member(z, suffix):
    hits = [n for n in z.namelist() if n.endswith(suffix)]
    if len(hits) != 1: raise RuntimeError('expected one member ending with ' + suffix)
    return z.read(hits[0])

# 1. release assets
for a in json.loads((ROOT / 'RELEASE_ASSETS.json').read_text())['assets']:
    p = assets / a['name']
    if not p.is_file(): failures.append('missing asset ' + a['name']); continue
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''): h.update(block)
    if h.hexdigest() != a['sha256']: failures.append('asset hash ' + a['name'])
print('assets checked')

# 2. layer archives
index = json.loads((ROOT / 'LAYER_INDEX.json').read_text())
ok = 0
by_case = {}
for r in index['checkpoints']:
    by_case.setdefault(r['preparation'], {})[r['layer']] = r
    if r['origin'] != 'original': continue
    if sha(open_chain(r['location'])) == r['sha256']: ok += 1
    else: failures.append('layer hash %s %d' % (r['preparation'], r['layer']))
print('retained layer archives with authenticated hash:', ok)

# 3. verification replay
replay = {}
for r in index['verification_replay']:
    data = open_chain(r['location'])
    if sha(data) != r['sha256']: failures.append('replay hash %s %d' % (r['preparation'], r['layer']))
    replay.setdefault(r['preparation'], {})[r['layer']] = zipfile.ZipFile(io.BytesIO(data))
for case, layers in sorted(replay.items()):
    start = min(layers) - 1
    base = zipfile.ZipFile(io.BytesIO(open_chain(by_case[case][start]['location'])))
    prev = [sha(member(base, 'layer_%03d/cell_%02d/receipt.json' % (start, j))) for j in range(12)]
    for L in sorted(layers):
        recs = [member(layers[L], 'layer_%03d/cell_%02d/receipt.json' % (L, j)) for j in range(12)]
        if any(json.loads(x)['case']['parents'] != prev for x in recs):
            failures.append('replay chain %s %d' % (case, L))
        prev = [sha(x) for x in recs]
    prod = zipfile.ZipFile(io.BytesIO(open_chain(by_case[case][68]['location'])))
    equal = 0
    for j in range(12):
        a = json.loads(member(prod, 'layer_068/cell_%02d/receipt.json' % j))['comparisons']
        b = json.loads(member(layers[68], 'layer_068/cell_%02d/receipt.json' % j))['comparisons']
        if all(a[k]['disk'] == b[k]['disk'] for k in ('state', 'emissions', 'time_dependencies')): equal += 1
        else: failures.append('layer 68 scientific hash %s cell %d' % (case, j))
    print('replay %-15s layers %s, layer-68 cells equal to production: %d/12' % (case, sorted(layers), equal))

print('PASS' if not failures else 'FAIL: ' + '; '.join(failures[:20]))
sys.exit(0 if not failures else 1)
