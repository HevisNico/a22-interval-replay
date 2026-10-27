"""Extract terminal enclosures of a scenario campaign into the certify_future.py input format.

One scenario per cell is required (true for the eps=1e-3 campaign). Fields:
g = exp(z) box per port, or the cap box C = 4(1 +- eps) for a capped port; b, q boxes;
main/aux phases; E = [50,100] (analytic invariant of the model).
m (auxiliary charge) is not stored in the scenario state: a READY auxiliary that has
received input ends its cycle exactly at r_m = 1/40 (section reset), so m = [.025,.025];
a port that never received input keeps the initial box r_m +- delta.
"""
import sys, os, json, glob, hashlib
from decimal import Decimal
pkg, root, eps, out = sys.argv[1:5]
os.environ['A22_PHYSICAL_EPSILON'] = eps
sys.path.insert(0, os.path.join(pkg, 'engine'))
from pathlib import Path
import run
e, a, t = run.initialize(Path(out).parent / 'diag_extract')
I = e.I
C = 4 * (1 + I(-Decimal(eps), Decimal(eps)))
cfg = json.loads((Path(root) / 'campaign.json').read_text())
cells = []
for n in range(1, 19):
    for lane in range(12):
        rs = sorted(glob.glob(f'{root}/layer_{n:02d}/cell_{lane:02d}/*/receipt.json'))
        assert len(rs) == 1, (n, lane, len(rs))
        d = json.load(open(rs[0]))
        data = a.read(Path(rs[0]).parent / 'result.json', d['payload_sha256'])
        assert len(data['scenarios']) == 1, (n, lane)
        s = data['scenarios'][0]; st = s['state']
        assert st['p'] == 0 and st['aux'] == [0, 0, 0] and st['raw'] == [None] * 3
        assert st['t'].box().pair() == ['1116', '1116']
        g = [(C if st['caps'][j] else st['z'][j].exp()).pair() for j in range(3)]
        received = [bool(st['depot'][j]) or bool(st['err'][j] is not None) for j in range(3)]
        m = [['0.025', '0.025'] if received[j] else ['0.02499', '0.02501'] for j in range(3)]
        cells.append(dict(layer=n, lane=lane, q=st['q'].pair(), g=g, b=st['b'].pair(), E=[50, 100], m=m,
                          main_phase=st['p'], aux_phases=list(st['aux']), pending=[], raw_inputs=[None] * 3,
                          caps=list(st['caps']), pulses=data['metrics']['pulses'],
                          outputs=len(s['outputs']), payload_sha256=d['payload_sha256']))
json.dump(dict(schema='A22-passive-terminal-extraction-1', campaign=cfg, time='1116',
               status='scenario-campaign terminal enclosures, one scenario per cell; m derived from READY auxiliary semantics',
               cells=cells), open(out, 'w'), indent=1)
print('cells', len(cells), 'active (pulses>0)', sum(c['pulses'] > 0 for c in cells))
