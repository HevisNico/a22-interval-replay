# Exploratory simulations (not certified)

These studies test the A22 physical kernel with a point simulator, outside the certified setting:
noise, other inputs, other topologies, ablations of the learning rule and longer training. They are
sampled simulations, not proofs. The certified engine is never used. Each claim below holds for the
stated protocol and sample only.

## The main findings so far

**Training under noise produces a network that transmits reliably under that noise, at 130 layers.**
With 2,048 noisy training pulses and gains frozen at test, the network recovers 99.5 to 100 % of test
pulses at layer 130 under 5 to 15 % amplitude noise plus jitter, against 9 to 79 % for the same network
trained for the same duration without noise ([`gate_noise_130/`](gate_noise_130/README.md), 20 seeds per
level, separate training and test noise). The margin learned scales with the training noise. The timing
remains noisy: about 0.5 to 1.3 % relative RMS error on the intervals.

**The protection gate is not what produces this robustness.** Removing the gate (gains may also grow
during protection) gives the same or slightly better transmission, but drives almost every gain to its
cap (97.7 % of ports, against about 2 % with the gate). The gate keeps the learned gains moderate; a
benefit of that, if any, has not been tested.

## The studies

| Folder | Question | Key result |
|---|---|---|
| [`robustness/`](robustness/README.md) | How does the kernel react to noise, closer pulses, other shapes and topologies? (18 and 130 layers, 128 training pulses) | Gradual degradation for small noise; discrete losses for larger noise; losses accumulate with depth. Works with gaps down to 7 and with all tested topologies without noise. |
| [`ablations_130/`](ablations_130/README.md) | Which part of the learning rule matters? (130 layers, 128 training pulses, 20 seeds) | Without learning, the network never ignites. With only 128 training pulses, plasticity left active during protection gave no complete word even without noise, and with noise the training does not reach layer 130. |
| [`noisy_training_130/`](noisy_training_130/README.md) | Does longer noisy training install a robust regime at 130 layers? (20 seeds, paired controls) | Yes in 20/20 seeds, against 0/20 for clean training of the same duration. Its 24-pulse test partly reused training noise (see the correction in its README). |
| [`gate_noise_130/`](gate_noise_130/README.md) | Is the protection gate needed for robustness? Does the effect hold at three noise levels? (2,048 training pulses, 20 seeds per level) | The gate is not needed; without it gains saturate. The noisy-training benefit is confirmed at all three levels with fully separate noise. |

## What is still open

- Whether the gate has another benefit (keeping gains away from saturation, resource use, remaining
  plasticity), and whether learning settles under bounded noise.
- Continuous noise, physical-parameter uncertainty and other topologies with the longer training.
- Any guarantee for every realization: these are 2 to 20 sampled runs per condition.

The code, runs and reports were produced with AI assistants under the author's direction. The
detailed reports (`rapport.html`, or the PDF in `gate_noise_130/`) are in French; each folder has an English README.
