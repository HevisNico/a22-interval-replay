"""Rebuild WIDTHS_BY_LAYER.csv from the run summaries (standard library only).

Run from the repository root:  python3 sweep/make_width_table.py
The 1e-4 column is the v3.3 campaign (results/campaign_summary.json).
"""
import csv, json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [('1e-4', ROOT / 'results/campaign_summary.json'),
        ('3e-4', ROOT / 'sweep/eps_3em4/RUN_SUMMARY.json'),
        ('1e-3', ROOT / 'sweep/eps_1em3/RUN_SUMMARY.json'),
        ('3e-3', ROOT / 'sweep/eps_3em3/RUN_SUMMARY.json')]


def per_layer(path):
    out = {}
    for layer in json.loads(path.read_text())['layers']:
        active = [c for c in layer['cells'] if c.get('pulses', 0) > 0 and 'max_date_width' in c]
        if len(active) != len([c for c in layer['cells'] if c.get('pulses', 0) > 0]) or not active:
            continue                       # refused or incomplete layer
        if any(c.get('status') != 'research_cell_complete' for c in layer['cells']):
            continue
        out[layer['layer']] = (statistics.median(c['max_date_width'] for c in active),
                               max(c['max_date_width'] for c in active),
                               max(c.get('gain_width', 0) for c in active))
    return out


data = {eps: per_layer(p) for eps, p in RUNS}
with open(ROOT / 'sweep/WIDTHS_BY_LAYER.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['layer'] + [f'{k}_eps_{e}' for e, _ in RUNS for k in ('median_date_width', 'max_date_width', 'max_gain_width')])
    for n in range(1, 19):
        row = [n]
        for e, _ in RUNS:
            row += [f'{x:.4g}' for x in data[e][n]] if n in data[e] else ['', '', '']
        w.writerow(row)
print('wrote sweep/WIDTHS_BY_LAYER.csv')
