"""Passive source/AST witnesses for the manual learning-coverage proof.

This is NOT a semantic proof checker. It imports no A22 module and runs no
cell, campaign, or replay. Checks pin the reviewed source and key call order.
"""
from pathlib import Path
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'provenance_audit/source/A22_fresh_launch_v3_3_EN'
LEGACY = 'kernel/R_cycle_local_A20_2026-10-18/'
CURRENT = 'kernel/R_continuation_A22_2026-10-18/'


def digest(b):
    return hashlib.sha256(b).hexdigest()


def function(path, name):
    text = (SOURCE / path).read_text()
    tree = ast.parse(text)
    found = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    assert len(found) == 1, (path, name, len(found))
    n = found[0]
    body = '\n'.join(text.splitlines()[n.lineno-1:n.end_lineno]) + '\n'
    return n, body, {'path': path, 'function': name, 'first_line': n.lineno,
                     'last_line': n.end_lineno, 'function_sha256': digest(body.encode())}


def main():
    specs = [
        ('run.py', 'initialize'), ('run.py', 'worker'),
        ('affine/affine_iv.py', 'make'), ('affine/affine_iv.py', '__mul__'),
        ('affine/affine_iv.py', '_unary'), ('affine/affine_iv.py', 'exp'),
        ('affine/affine_iv.py', 'ln'), ('affine/affine_iv.py', 'hull'),
        ('affine/engine.py', '_plain_root'), ('affine/engine.py', 'affine_refine'),
        ('affine/engine.py', 'ready_root'), ('affine/engine.py', 'compute_cell'),
        ('affine/temporal.py', 'fresh'), ('affine/temporal.py', 'shift'),
        ('affine/temporal.py', 'minus'), ('affine/temporal.py', 'token'),
        (LEGACY+'outils_validation.py', 'ready'),
        (LEGACY+'dependances_A17.py', 'pulse'), (LEGACY+'dependances_A17.py', 'join'),
        (LEGACY+'dependances_A17.py', 'evaluate'),
        (LEGACY+'actuations_A19.py', 'ell'), (LEGACY+'depot_A19.py', 'certain_cap'),
        (LEGACY+'validation_A15.py', 'admissible_orders'),
        (LEGACY+'validation_A15.py', 'unit'),
        (LEGACY+'validation_A15.py', 'flowing'),
        (LEGACY+'validation_A15.py', 'fire_reset'),
        (LEGACY+'validation_A15.py', 'protected_section_cluster'),
        (LEGACY+'validation_A15.py', 'recovery_auxiliary_cluster'),
        (LEGACY+'branche_retour_A19.py', 'return_with_marks'),
        (LEGACY+'cycle_local_A20.py', 'resolve'),
        (LEGACY+'cycle_local_A20.py', 'pending_window'),
        (CURRENT+'garde_relative_A22.py', 'cover'),
        (CURRENT+'garde_relative_A22.py', 'ready_to'),
        (CURRENT+'avance_causale_A22.py', 'advance'),
        ('affine/commutation.py', '_resolve'),
        ('affine/commutation.py', '_fire_root'),
        ('affine/commutation.py', '_first_crossing_cover'),
        ('affine/recovery_group.py', 'resolve'),
        (LEGACY+'profil_largeurs_A19.py', 'export'),
        ('affine/port_box_adapter.py', 'settings'),
    ]
    witnesses = []
    bodies = {}
    nodes = {}
    for path, name in specs:
        node, body, record = function(path, name)
        witnesses.append(record)
        bodies[(path, name)] = body
        nodes[(path, name)] = node

    checks = []

    def require(label, predicate):
        assert predicate, label
        checks.append({'id': label, 'status': 'PASS', 'scope': 'structural source witness'})

    # Important: no original function is compiled, imported, or called here.
    init = nodes[('run.py', 'initialize')]
    require('runner_refuses_optimized_python_with_if',
            any(isinstance(n, ast.If) and ast.unparse(n.test) == 'not __debug__'
                and any(isinstance(q, ast.Raise) for q in ast.walk(n)) for n in init.body))
    for name in ('_plain_root', 'affine_refine'):
        node = nodes[('affine/engine.py', name)]
        loops = [n for n in ast.walk(node) if isinstance(n, ast.For)]
        ok = False
        for loop in loops:
            body = '\n'.join(ast.unparse(n) for n in loop.body)
            marker = 'slope = deriv(x)' if name == '_plain_root' else 'S = deriv(T)'
            if marker in body and 'fun(I(m))' in body:
                ok |= body.index(marker) < body.index('fun(I(m))')
        require(name+'_derivative_precedes_new_guard_evaluation', ok)
    require('time_shift_allocates_atom_for_nonpoint_duration',
            't.expression()+((fresh(),1,u),)' in bodies[('affine/temporal.py', 'shift')])
    require('time_minus_checks_atom_definitions',
            'if not same_form(prev,value)' in bodies[('affine/temporal.py', 'minus')])
    require('time_minus_selects_absolute_or_expression_enclosure',
            'return bx if bx.width()<a.width() else a' in bodies[('affine/temporal.py', 'minus')])
    require('slow_guard_evaluates_expanded_logarithm',
            "I('2.5').ln()-capped_dose(h,t,live)" in bodies[(LEGACY+'actuations_A19.py', 'ell')])
    require('per_order_return_uses_unfinished_history_at_earlier_probes',
            'ac.ell(h,probe(u),False)' in bodies[(LEGACY+'branche_retour_A19.py', 'return_with_marks')])
    require('absolute_restriction_preserves_return_expression',
            'terms=ready.expression()' in bodies[(LEGACY+'cycle_local_A20.py', 'resolve')])
    require('memory_join_compares_anchor_tokens',
            "x['anchor'].token()==first['anchor'].token()" in bodies[(LEGACY+'dependances_A17.py', 'join')])
    require('fast_slow_equal_date_normalization',
            'difference.lo==difference.hi==0' in bodies[(CURRENT+'avance_causale_A22.py', 'advance')])
    require('profile_preserves_complete_relative_order_list',
            'relative_order_proofs=self.relative_order_proofs' in bodies[(LEGACY+'profil_largeurs_A19.py', 'export')])
    require('gain_cap_uses_upper_target',
            'offered(h,t).lo>=TARGET.hi' in bodies[(LEGACY+'depot_A19.py', 'certain_cap')])
    require('first_delay_has_distinct_port_symbols',
            "I.symbol(f'{cell}:D1:{j}',radius)" in bodies[('affine/port_box_adapter.py', 'settings')])
    require('new_cell_uses_fresh_noise_namespace',
            "affine_iv.FRESH=namespace+':remainder'" in bodies[('affine/engine.py', 'compute_cell')])

    unit = bodies[(LEGACY+'validation_A15.py', 'unit')]
    overlap = "if section.lo<=upper and section.hi>=min(t.box().lo for t,_ in group):"
    require('fast_overlap_intercepted_before_multiple_group_advance',
            overlap in unit and unit.index(overlap) < unit.index('if len(group)>1:')
            and 'protected_section_cluster(s,group,upper,cell,count)' in unit)
    require('protected_macro_requires_forward_group_entry',
            "assert min(t.box().lo for t,_ in group)>=s['t'].box().hi" in
            bodies[(LEGACY+'validation_A15.py', 'protected_section_cluster')])
    require('group_extension_uses_complete_suffix_minimum',
            "suffix[k]=min(suffix[k+1],pending[k][0].box().lo)" in unit
            and 'while upper>suffix[stopidx]:' in unit)
    require('local_window_stops_before_every_remaining_event',
            'rest_lower=min(t.box().lo for t,_ in pending[stop:])' in
            bodies[(LEGACY+'cycle_local_A20.py', 'pending_window')]
            and 'if rest_lower>=upper:break' in
            bodies[(LEGACY+'cycle_local_A20.py', 'pending_window')])

    fire_root = bodies[('affine/commutation.py', '_fire_root')]
    cover = bodies[('affine/commutation.py', '_first_crossing_cover')]
    require('commutation_cover_caller_checks_upper_endpoint_before_fallback',
            'if not hi > 0 or f(I(hi)).lo < 0:' in fire_root
            and fire_root.index('f(I(hi)).lo < 0') < fire_root.index('_first_crossing_cover(f, hi)'))
    require('commutation_cover_requires_strictly_below_initial_charge',
            'if not f(I(0)).hi < 0:' in cover)
    require('commutation_cover_scans_left_before_right',
            'a, z, n = stack.pop()' in cover
            and 'stack.append((m, z, n + 1)); stack.append((a, m, n + 1))' in cover)
    require('commutation_cover_preserves_undecided_lower_and_certified_upper',
            'lower = None; upper = hi' in cover
            and 'if val.hi < 0:' in cover and 'if val.lo >= 0:' in cover
            and 'upper = min(upper, a)' in cover
            and 'if lower is None: lower = a' in cover
            and 'return I(lower, upper)' in cover)

    # Pin every shipped file to the previously authenticated supplied ZIP.
    reference = json.loads((HERE.parent/'kernel_soundness/output/source_unchanged.json').read_text())
    for record in reference['files']:
        rel = Path(record['path']).relative_to('A22_fresh_launch_v3_3_EN')
        data = (SOURCE/rel).read_bytes()
        require('source_unchanged:'+rel.as_posix(), digest(data) == record['sha256'] and len(data) == record['bytes'])
    output = {
        'scope': 'Static source witnesses only; no semantic proof certification',
        'original_a22_imported_or_executed': False,
        'original_source_files_unchanged': len(reference['files']),
        'function_witnesses': witnesses,
        'checks': checks,
        'manual_proof': 'LEARNING_COVERAGE_THEOREM_EN.txt',
        'proof_level': 'manual source-level argument under A1-A4; not machine checked'
    }
    path = HERE/'output/source_witness_checks.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'structural_checks': len(checks), 'function_witnesses': len(witnesses),
                      'unchanged_source_files': len(reference['files']),
                      'original_engine_executed': False, 'semantic_proof_machine_checked': False}))


if __name__ == '__main__':
    main()
