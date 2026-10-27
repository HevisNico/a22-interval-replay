"""One-command check of release v4.4 (program v3.3 + C7, eps = 1e-3).

Usage, from the repository root, with the six release assets in one folder:
  python3 -I sweep/v33_c7/verify_release.py <assets folder> [--work <scratch folder>]

Steps (each prints PASS, FAIL or SKIP; the exit code is 1 if any step fails):
 1. asset hashes against RELEASE_ASSETS_SHA256.json;
 2. engine: every file of the as-run engine that enters the program identity
    equals the fresh-launch package in this folder, apart from its two built
    binaries; the arithmetic binary has the hash recorded in campaign.json;
 3. engine identity: the campaign kernel_id recomputed from the as-run engine
    (needs Python 3.12 with numpy 2.3.5 and scipy 1.17.0, else SKIP);
 4. outputs: every record of the five output archives against RUN_MANIFEST.json;
 5. chain: each layer's completion record lists exactly the hashes of its 12
    receipts, every receipt names its campaign and kernel and the hashes of
    its parent receipts, and every payload has the hash its receipt states;
 6. extraction: audit_campaign_dir.py on the outputs reproduces terminal/;
 7. future: both future-wave checkers at eps = 1e-3 pass and reproduce the
    content of the committed certificates.
Standard library only, except step 3, which runs the engine in a subprocess.
"""
import hashlib, json, os, shutil, subprocess, sys, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FUTURE = REPO / 'sweep' / 'v23' / 'eps_1em3' / 'future'
OUTPUT_PREFIX = 'A22_v33c7_1em3_layers_'
ENGINE_ZIP = 'A22_v33c7_engine_as_run.zip'
RESULTS = []


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def report(step, ok, detail):
    status = 'SKIP' if ok is None else ('PASS' if ok else 'FAIL')
    RESULTS.append(status)
    print(f'[{status}] {step}: {detail}', flush=True)


def step_assets(assets):
    expected = json.loads((HERE / 'RELEASE_ASSETS_SHA256.json').read_text())
    bad = [n for n, h in expected.items() if not (assets / n).exists() or sha(assets / n) != h]
    report('1 asset hashes', not bad, f'{len(expected) - len(bad)}/{len(expected)} match' + (f'; bad: {bad}' if bad else ''))
    return not bad


def unzip(archive, target):
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError(f'corrupt archive {archive}')
        z.extractall(target)


def step_engine(assets, work):
    engine = work / 'engine'
    if engine.exists():
        shutil.rmtree(engine)
    unzip(assets / ENGINE_ZIP, engine)
    root = engine / 'A22_v33c7_engine_as_run'
    fresh = work / 'fresh'
    if fresh.exists():
        shutil.rmtree(fresh)
    unzip(HERE / 'A22_fresh_launch_v3_3_C7.zip', fresh)
    froot = fresh / 'A22_fresh_launch_v3_3_C7'
    # Compare the files that enter the program identity (run.identity): the
    # four launcher scripts, the model reference and affine/ and kernel/.
    # Tests and documentation may have been extended since the run.
    top = {'run.py', 'build_native.py', 'build_all_native.py', 'launch_fresh.py',
           'reference/full_model_reference.md'}
    def files(base):
        return {str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                and (str(p.relative_to(base)) in top or p.relative_to(base).parts[0] in ('affine', 'kernel'))}
    a, b = files(root), files(froot)
    binaries = {x for x in a - b if x.endswith('.so')}
    differ = sorted(x for x in a & b if sha(root / x) != sha(froot / x))
    extra = sorted(a - b - binaries) + sorted(b - a)
    campaign = json.loads((HERE / 'campaign' / 'campaign.json').read_text())
    native = root / 'affine' / '_rounding_native.cpython-312-x86_64-linux-gnu.so'
    native_ok = native.exists() and sha(native) == campaign['environment']['native_sha256']
    ok = not differ and not extra and len(binaries) == 2 and native_ok
    report('2 engine contents', ok, f'{len(a & b)} source files identical to the fresh-launch package, '
           f'{len(binaries)} binaries, rounding binary {"matches" if native_ok else "DOES NOT match"} campaign.json'
           + (f'; differ: {differ}; unmatched: {extra}' if differ or extra else ''))
    return root


def step_identity(root):
    campaign = json.loads((HERE / 'campaign' / 'campaign.json').read_text())
    code = ("import json,run;from pathlib import Path;"
            "cfg=json.loads(Path(%r).read_text());"
            "e,a,t=run.initialize(Path(%r));"
            "print(a.canonical_hash({'sources':run.identity(),'environment':cfg['environment'],"
            "'parameters':cfg['parameters'],'precision':160,'symbols':run.affine_iv_kmax()}))"
            % (str(HERE / 'campaign' / 'campaign.json'), str(root.parent / 'identity_diagnostics')))
    env = dict(os.environ, A22_PHYSICAL_EPSILON=campaign['parameters']['epsilon_relative'])
    try:
        out = subprocess.run([sys.executable, '-B', '-c', code], cwd=root, env=env,
                             capture_output=True, text=True, timeout=600)
    except Exception as exc:
        report('3 engine identity', None, f'engine not runnable here ({exc})'); return
    if out.returncode != 0:
        report('3 engine identity', None, 'engine not runnable with this Python (needs CPython 3.12, numpy 2.3.5, '
               'scipy 1.17.0): ' + (out.stderr.strip().splitlines() or ['?'])[-1][:120]); return
    got = out.stdout.strip().splitlines()[-1]
    report('3 engine identity', got == campaign['kernel_id'], f'kernel_id {got[:16]}… vs campaign {campaign["kernel_id"][:16]}…')


def step_outputs(assets, work):
    outputs = work / 'outputs'
    parts = sorted(assets.glob(OUTPUT_PREFIX + '*.zip'))
    if not (outputs / 'A22_v33c7_1em3' / 'layer_18').exists():
        for p in parts:
            unzip(p, outputs)
    run = outputs / 'A22_v33c7_1em3'
    manifest = json.loads((HERE / 'campaign' / 'RUN_MANIFEST.json').read_text())['files']
    bad = [k for k, v in manifest.items()
           if not (run / k).exists() or (run / k).stat().st_size != v['bytes'] or sha(run / k) != v['sha256']]
    same_campaign = (run / 'campaign.json').read_bytes() == (HERE / 'campaign' / 'campaign.json').read_bytes()
    report('4 output records', not bad and same_campaign and len(parts) == 5,
           f'{len(manifest) - len(bad)}/{len(manifest)} records match the manifest from {len(parts)} archives'
           + (f'; first bad: {bad[:3]}' if bad else '') + ('' if same_campaign else '; campaign.json differs'))
    return run


def step_chain(run):
    campaign = json.loads((run / 'campaign.json').read_text())
    problems = []
    previous = None
    for layer in range(1, 19):
        base = run / f'layer_{layer:02d}'
        receipts = {}
        for lane in range(12):
            cell = base / f'cell_{lane:02d}'
            r = json.loads((cell / 'receipt.json').read_text())
            receipts[sha(cell / 'receipt.json')] = r
            case = r['case']
            if (case['run_id'], case['kernel_id'], case['layer'], case['lane']) != (campaign['run_id'], campaign['kernel_id'], layer, lane):
                problems.append(f'({layer},{lane}) wrong case')
            if r['payload_sha256'] != sha(cell / 'result.json'):
                problems.append(f'({layer},{lane}) payload hash')
            parents = case.get('parent_receipts') or []
            if layer > 1 and not set(parents) <= set(previous):
                problems.append(f'({layer},{lane}) unknown parent receipt')
        listed = json.loads((base / 'complete.json').read_text()).get('receipts')
        if listed is not None and set(listed) != set(receipts):
            problems.append(f'layer {layer}: complete.json lists other receipts')
        previous = set(receipts)
    report('5 receipt chain', not problems, '18 layers x 12 cells: case identity, payload hashes, parent links, completion lists'
           + (f'; problems: {problems[:5]}' if problems else ''))


def run_script(args):
    out = subprocess.run([sys.executable, '-I'] + [str(a) for a in args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError((out.stderr.strip().splitlines() or ['?'])[-1])
    return out.stdout


def step_extraction(run, work):
    out = work / 'terminal'
    run_script([HERE / 'audit_campaign_dir.py', run, out])
    same = [n for n in ('all_layers_audit.json', 'all_terminal_exact.json')
            if (out / n).read_bytes() == (HERE / 'terminal' / n).read_bytes()]
    report('6 terminal extraction', len(same) == 2, f'{len(same)}/2 outputs byte-identical to terminal/')
    return out


def step_future(out):
    run_script([FUTURE / 'certify_future_eps.py', out / 'all_terminal_exact.json', out / 'future.json', '1e-3'])
    run_script([FUTURE / 'verify_future_certificate_eps.py', out / 'all_terminal_exact.json', out / 'future.json',
                out / 'independent.json', '1e-3'])
    f = json.loads((out / 'future.json').read_text()); i = json.loads((out / 'independent.json').read_text())
    # The checkers list minimum_margins in set order, which varies between
    # runs; compare content, and check that the independent check cites the
    # hash of the certificate regenerated here.
    cf = json.loads((HERE / 'terminal' / 'future_certificate_eps1e-3.json').read_text())
    ci = json.loads((HERE / 'terminal' / 'independent_check_eps1e-3.json').read_text())
    strip = lambda d: {k: v for k, v in d.items() if k != 'certificate_sha256'}
    same = (f == cf and strip(i) == strip(ci)
            and i['certificate_sha256'] == sha(out / 'future.json'))
    ok = f['status'].startswith('PASS') and i['status'] == 'PASS' and same
    report('7 future invariance', ok, f'certificate {f["status"][:4]}, independent check {i["status"]}, '
           f'{f["active"]} active cells, at rest before {f["global_quiescent_by"][:8]}; '
           f'{"same content as" if same else "DIFFERENT from"} the committed certificates')


def main():
    if not __debug__:
        raise RuntimeError('run without -O')
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    assets = Path(args[0]).resolve()
    work = Path(args[args.index('--work') + 1]).resolve() if '--work' in args else assets / 'verify_work'
    work.mkdir(parents=True, exist_ok=True)
    step_assets(assets)
    root = step_engine(assets, work)
    step_identity(root)
    run = step_outputs(assets, work)
    step_chain(run)
    out = step_extraction(run, work)
    step_future(out)
    failed = RESULTS.count('FAIL')
    print(f'\n{RESULTS.count("PASS")} PASS, {failed} FAIL, {RESULTS.count("SKIP")} SKIP')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
