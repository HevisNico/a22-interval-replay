"""Regenerate every committed certificate that needs no campaign output, and compare.
Also checks the depth releases: the G_rel manifest and audit, and the cone and ergodic
certificates (compared without their environment field, which records the machine).

Run from the repository root:  python3 -I tools/check_certificates.py
Standard library only; no engine import. Each check prints PASS or FAIL; the exit code
is 1 if any check fails. Used by .github/workflows/checks.yml.

The future-wave certificates list some margins in set order, which varies between runs,
so they are compared by content; an independent check is compared without its
certificate_sha256 field, which must instead be the hash of the regenerated certificate.
The initial-section certificates are deterministic and compared byte for byte.
"""
import hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROOF = REPO / 'proof'
FUT = REPO / 'sweep' / 'v23' / 'eps_1em3' / 'future'
C7 = REPO / 'sweep' / 'v33_c7'
RESULTS = []


def run(*args):
    out = subprocess.run([sys.executable, '-I'] + [str(a) for a in args],
                         capture_output=True, text=True, cwd=REPO)
    if out.returncode != 0:
        raise RuntimeError((out.stderr.strip().splitlines() or ['?'])[-1][:200])


def run_local(script, *args, cwd=None):
    """For the depth scripts, which import helpers from their own folder."""
    out = subprocess.run([sys.executable, '-B', str(script)] + [str(a) for a in args],
                         capture_output=True, text=True, cwd=cwd or Path(script).parent)
    if out.returncode != 0:
        raise RuntimeError((out.stderr.strip().splitlines() or ['?'])[-1][:200])
    return out.stdout


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def report(name, ok, detail=''):
    RESULTS.append(ok)
    print(f'[{"PASS" if ok else "FAIL"}] {name}' + (f': {detail}' if detail else ''), flush=True)


def check(name, fn):
    try:
        fn()
    except Exception as exc:
        report(name, False, f'{type(exc).__name__}: {exc}')


def same_bytes(new, ref):
    return Path(new).read_bytes() == Path(ref).read_bytes()


def future_pair(name, certify, verify, terminal, ref_cert, ref_check, eps, tmp):
    """Regenerate a future certificate and its independent check; compare by content."""
    slug = hashlib.sha256(name.encode()).hexdigest()[:12]
    cert, ind = tmp / f'{slug}_cert.json', tmp / f'{slug}_check.json'
    run(certify, terminal, cert, *eps)
    run(verify, terminal, cert, ind, *eps)
    c, i = json.loads(cert.read_text()), json.loads(ind.read_text())
    rc, ri = json.loads(Path(ref_cert).read_text()), json.loads(Path(ref_check).read_text())
    strip = lambda d: {k: v for k, v in d.items() if k != 'certificate_sha256'}
    ok_c = c == rc
    ok_i = strip(i) == strip(ri) and i.get('certificate_sha256') == sha(cert)
    report(name, ok_c and ok_i and i.get('status') == 'PASS',
           f'certificate {"same" if ok_c else "DIFFERENT"}, independent check '
           f'{i.get("status")} and {"same" if ok_i else "DIFFERENT"}')


def main():
    if not __debug__:
        raise RuntimeError('run without -O')
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)

        def initial_v33():
            out = tmp / 'initial.json'
            run(PROOF / 'final_entry_audit' / 'certify_initial_section.py', out)
            report('initial section, eps = 1e-4 (proof/final_entry_audit)',
                   same_bytes(out, PROOF / 'final_entry_audit' / 'output' / 'initial_section_certificate.json'))
        check('initial section, eps = 1e-4 (proof/final_entry_audit)', initial_v33)

        def initial_eps():
            for eps, ref in (('1e-4', PROOF / 'final_entry_audit' / 'output' / 'initial_section_certificate.json'),
                             ('1e-3', C7 / 'terminal' / 'initial_section_eps1e-3.json')):
                out = tmp / f'initial_{eps}.json'
                run(C7 / 'certify_initial_section_eps.py', out, eps)
                report(f'initial section, eps = {eps} (sweep/v33_c7)', same_bytes(out, ref))
        check('initial section (sweep/v33_c7)', initial_eps)

        terminal_v33 = PROOF / 'provenance_audit' / 'output' / 'all_terminal_exact.json'
        check('future, v3.3 at eps = 1e-4 (proof/provenance_audit)', lambda: future_pair(
            'future, v3.3 at eps = 1e-4 (proof/provenance_audit)',
            PROOF / 'provenance_audit' / 'certify_future.py',
            PROOF / 'provenance_audit' / 'verify_future_certificate.py',
            terminal_v33, PROOF / 'provenance_audit' / 'output' / 'future_closure_certificate.json',
            PROOF / 'provenance_audit' / 'output' / 'future_independent_check.json', (), tmp))
        check('future, general-eps checkers at eps = 1e-4 on v3.3', lambda: future_pair(
            'future, general-eps checkers at eps = 1e-4 on v3.3',
            FUT / 'certify_future_eps.py', FUT / 'verify_future_certificate_eps.py', terminal_v33,
            FUT / 'check_v33_eps1e-4.json', FUT / 'independent_check_v33_eps1e-4.json', ('1e-4',), tmp))
        check('future, v3.3 + C7 at eps = 1e-3 (sweep/v33_c7)', lambda: future_pair(
            'future, v3.3 + C7 at eps = 1e-3 (sweep/v33_c7)',
            FUT / 'certify_future_eps.py', FUT / 'verify_future_certificate_eps.py',
            C7 / 'terminal' / 'all_terminal_exact.json', C7 / 'terminal' / 'future_certificate_eps1e-3.json',
            C7 / 'terminal' / 'independent_check_eps1e-3.json', ('1e-3',), tmp))
        check('future, scenario launcher at eps = 1e-3 (sweep/v23)', lambda: future_pair(
            'future, scenario launcher at eps = 1e-3 (sweep/v23)',
            FUT / 'certify_future_eps.py', FUT / 'verify_future_certificate_eps.py',
            FUT / 'terminal_eps1e-3.json', FUT / 'future_eps1e-3.json',
            FUT / 'independent_check_eps1e-3.json', ('1e-3',), tmp))
        DEPTH = REPO / 'depth'

        def grel():
            out = run_local(DEPTH / 'g_rel' / 'verify_manifest.py')
            report('depth/g_rel manifest', 'PASS_RELEASE_MANIFEST' in out, out.strip())
            copy = tmp / 'g_rel'
            shutil.copytree(DEPTH / 'g_rel', copy, ignore=shutil.ignore_patterns('__pycache__'))
            run_local(copy / 'audit.py')
            new, ref = (json.loads((d / 'AUDIT.json').read_text()) for d in (copy, DEPTH / 'g_rel'))
            report('depth/g_rel audit', new['status'] == 'PASS' and new['rows'] == ref['rows'],
                   f'{len(new["rows"])} witnesses, {"same" if new["rows"] == ref["rows"] else "DIFFERENT"} rows')
        check('depth/g_rel', grel)

        def without_env(path):
            d = json.loads(Path(path).read_text())
            d.pop('environment', None)
            return d

        def cone():
            out = tmp / 'cone.json'
            run_local(DEPTH / 'cone' / 'verify_cone.py', out)
            report('depth/cone certificate', without_env(out) == without_env(DEPTH / 'cone' / 'cone_certificate.json'))
        check('depth/cone certificate', cone)

        def ergodic():
            out = tmp / 'ergodic.json'
            run_local(DEPTH / 'ergodic' / 'verify.py', out)
            report('depth/ergodic bounds',
                   without_env(out) == without_env(DEPTH / 'ergodic' / 'comparison_and_bounds.json'))
        check('depth/ergodic bounds', ergodic)
    failed = RESULTS.count(False)
    print(f'\n{RESULTS.count(True)} PASS, {failed} FAIL')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
