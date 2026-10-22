"""Exact checks of two insufficient proof contracts, NOT kernel executions.

These examples do not claim to be reachable states of the recorded campaign.
No original A22 module is imported, and no cell is evaluated.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def exp_negative_bounds(x, even_terms=40):
    assert 0 < x <= 1 and even_terms % 2 == 0
    # Alternating Taylor series: decreasing terms, even partial sum above,
    # immediately preceding odd partial sum below exp(-x).
    term = F(1)
    total = term
    lower = None
    for n in range(1, even_terms + 1):
        term *= -x / n
        total += term
        if n == even_terms - 1:
            lower = total
    return lower, total


def pair(x):
    return [str(x.numerator), str(x.denominator)]


def main():
    e1 = exp_negative_bounds(F(1))
    ehalf = exp_negative_bounds(F(1, 2))
    # Same symbolic clock A in [0,2], but conditional absolute anchor boxes
    # [0,1] and [1,2]. Keeping the first box discards the second branch.
    # q(t) = R + (q_anchor-R) exp(-K(t-A)); R=.1, q_anchor=.5, K=.5.
    first_branch_upper = F(1, 10) + F(2, 5) * e1[1]
    second_branch_value_lower = F(1, 10) + F(2, 5) * ehalf[0]
    gap = second_branch_value_lower - first_branch_upper
    assert first_branch_upper < F(1, 4)
    assert second_branch_value_lower > F(3, 10)
    assert gap > F(1, 20)

    # Minimal hybrid contract countermodel: x'=1 until an exterior cut at 1;
    # then x'=0. First threshold x=1 emits and resets. The true root is 1.
    # A closed root enclosure [1,2] and exterior date [1,1] pass the weak
    # exterior-before-root inequality, but exterior-only handling loses it.
    root = (F(1), F(2))
    external = F(1)
    weak_order_lower = root[0] - external
    assert external < sum(root) / 2 and weak_order_lower == 0
    assert (external, root[0]) == (F(1), F(1))

    result = {
        "scope": "countermodels to weaker contracts; not A22 campaign counterexamples",
        "original_kernel_imported_or_executed": False,
        "memory_anchor": {
            "same_token": "A", "global_atom_range": [0, 2],
            "conditional_anchor_boxes": [[0, 1], [1, 2]],
            "evaluation_time": 3,
            "first_box_charge_upper_rational": pair(first_branch_upper),
            "second_branch_charge_lower_rational": pair(second_branch_value_lower),
            "excluded_gap_lower_rational": pair(gap),
            "excluded_gap_exceeds": "1/20",
            "necessary_extra_contract": "retained box must cover the common anchor for every joined branch"
        },
        "threshold_boundary": {
            "model": "x(0)=0; x'=1 before t=1, x'=0 after; reaching x=1 emits",
            "true_first_root": 1, "closed_root_enclosure": [1, 2],
            "external_date": 1, "weak_order_lower": 0,
            "necessary_extra_contract": "strict physical ordering, or explicit equal-time guard handling",
            "a22_reachability_or_acceptance_demonstrated": False
        },
        "all_exact_assertions_passed": True
    }
    out = Path(__file__).parent / 'output/contract_countermodels.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({"exact_assertions_passed": True, "original_engine_executed": False}))


if __name__ == '__main__':
    main()
