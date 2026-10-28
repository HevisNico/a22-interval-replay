"""One-command check of release v4.4 (program v3.3 + C7, eps = 1e-3).

Usage, from the repository root, with the six release assets in one folder:
  python3 -I sweep/v33_c7/verify_release.py <assets folder> [--work <scratch folder>] [--strict]

Each step prints PASS, FAIL or SKIP. The verification is complete only when every
step passes. Exit code: 0 complete; 1 a step failed; 3 with --strict, no step
failed but one was skipped (without --strict a skip gives 0 and the verdict
INCOMPLETE). A failure of step 1 or 2 stops the run at once: an archive whose hash or
engine sources do not match is never extracted further, imported or executed. Steps:
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
    content of the committed certificates;
 8. initial section: certify_initial_section_eps.py reproduces the published
    certificate at eps = 1e-4 and the committed one at 1e-3, and passes;
 9. commutations: audit_commutations.py on the outputs reproduces
    terminal/commutation_usage_eps1e-3.json, and every recorded group is made
    of the actions lemma E covers (COVERAGE_THEOREM_GENERAL_EPS_EN.txt).
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
    return root if ok else None


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
    """Exact lineage, as the engine writes it (run.py): a receipt of layer 1 has no
    parent; a receipt of layer n > 1 lists, in lane order, the hashes of the 12
    receipts of layer n - 1; complete.json lists, in lane order, the hashes of the
    12 receipts of its layer. A missing or partial list is a failure."""
    campaign = json.loads((run / 'campaign.json').read_text())
    problems = []
    previous = []
    for layer in range(1, 19):
        base = run / f'layer_{layer:02d}'
        hashes = []
        for lane in range(12):
            cell = base / f'cell_{lane:02d}'
            r = json.loads((cell / 'receipt.json').read_text())
            hashes.append(sha(cell / 'receipt.json'))
            case = r.get('case', {})
            if (case.get('run_id'), case.get('kernel_id'), case.get('layer'), case.get('lane')) != (
                    campaign['run_id'], campaign['kernel_id'], layer, lane):
                problems.append(f'({layer},{lane}) wrong case')
            if r.get('payload_sha256') != sha(cell / 'result.json'):
                problems.append(f'({layer},{lane}) payload hash')
            if case.get('parent_receipts') != previous:
                problems.append(f'({layer},{lane}) parent receipts are not the 12 receipts of layer {layer - 1}'
                                if layer > 1 else f'(1,{lane}) a layer-1 receipt has parents')
        listed = json.loads((base / 'complete.json').read_text()).get('receipts')
        if listed != hashes:
            problems.append(f'layer {layer}: complete.json does not list its 12 receipts'
                            if listed is not None else f'layer {layer}: complete.json has no receipt list')
        previous = hashes
    report('5 receipt chain', not problems, '18 layers x 12 cells: case identity, payload hashes, exact parent '
           'lists, exact completion lists' + (f'; problems: {problems[:5]}' if problems else ''))


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


def step_initial(work):
    out = work / 'initial'
    out.mkdir(exist_ok=True)
    script = HERE / 'certify_initial_section_eps.py'
    published = REPO / 'proof' / 'final_entry_audit' / 'output' / 'initial_section_certificate.json'
    same = []
    for eps, ref in (('1e-4', published), ('1e-3', HERE / 'terminal' / 'initial_section_eps1e-3.json')):
        run_script([script, out / f'initial_{eps}.json', eps])
        if (out / f'initial_{eps}.json').read_bytes() == ref.read_bytes():
            same.append(eps)
    status = json.loads((out / 'initial_1e-3.json').read_text())['status']
    report('8 initial section', status == 'PASS' and len(same) == 2,
           f'status {status} at 1e-3; byte-identical to the reference at {", ".join(same) or "neither eps"}')


COVERED = {'raw_on', 'raw_off', 'mark_on', 'mark_off', 'error_on', 'error_off'}


def step_commutations(run, work):
    out = work / 'commutation_usage.json'
    run_script([HERE / 'audit_commutations.py', run, out])
    same = out.read_bytes() == (HERE / 'terminal' / 'commutation_usage_eps1e-3.json').read_bytes()
    u = json.loads(out.read_text())
    actions = {a for p in u['event_patterns'] for group in p['events'] for a in group}
    recorded = json.loads((HERE / 'terminal' / 'all_layers_audit.json').read_text())['recorded_guards']['fire_arrival_commutation']
    ok = same and actions <= COVERED and u['count'] == recorded
    report('9 commutations', ok, f'{u["count"]} recorded (audit: {recorded}), actions {sorted(actions)}'
           + ('' if actions <= COVERED else f'; NOT covered by lemma E: {sorted(actions - COVERED)}')
           + f'; {"same as" if same else "DIFFERENT from"} the committed summary')


def guarded(step, fn, *args):
    try:
        return fn(*args)
    except Exception as exc:
        report(step, False, f'{type(exc).__name__}: {str(exc)[:160]}')
        return None


def stop(reason):
    """End the run at an integrity failure, before any later step."""
    print(f'\nSTOPPED: {reason}')
    passed, failed = RESULTS.count('PASS'), RESULTS.count('FAIL')
    print(f'{passed} PASS, {failed} FAIL, later steps not run: verification FAILED')
    sys.exit(1)


def main():
    if not __debug__:
        raise RuntimeError('run without -O')
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    assets = Path(args[0]).resolve()
    work = Path(args[args.index('--work') + 1]).resolve() if '--work' in args else assets / 'verify_work'
    strict = '--strict' in args
    work.mkdir(parents=True, exist_ok=True)
    # Integrity gates: after a failure of step 1 nothing is extracted, and after a
    # failure of step 2 nothing from the archives is imported or executed.
    if guarded('1 asset hashes', step_assets, assets) is not True:
        stop('step 1 failed: no archive is extracted or executed')
    root = guarded('2 engine contents', step_engine, assets, work)
    if root is None:
        stop('step 2 failed: the extracted engine is not imported or executed')
    guarded('3 engine identity', step_identity, root)
    run = guarded('4 output records', step_outputs, assets, work)
    if run is None:
        for step in ('5 receipt chain', '6 terminal extraction', '7 future invariance'):
            report(step, False, 'not run: step 4 failed')
        guarded('8 initial section', step_initial, work)
        report('9 commutations', False, 'not run: step 4 failed')
    else:
        guarded('5 receipt chain', step_chain, run)
        out = guarded('6 terminal extraction', step_extraction, run, work)
        if out is None:
            report('7 future invariance', False, 'not run: step 6 failed')
        else:
            guarded('7 future invariance', step_future, out)
        guarded('8 initial section', step_initial, work)
        guarded('9 commutations', step_commutations, run, work)
    passed, failed, skipped = (RESULTS.count(k) for k in ('PASS', 'FAIL', 'SKIP'))
    verdict = 'FAILED' if failed else ('INCOMPLETE (a step was skipped)' if skipped else 'COMPLETE')
    print(f'\n{passed} PASS, {failed} FAIL, {skipped} SKIP: verification {verdict}')
    sys.exit(1 if failed else (3 if skipped and strict else 0))


if __name__ == '__main__':
    main()
