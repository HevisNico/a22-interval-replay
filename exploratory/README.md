# Exploratory simulations (not certified)

These studies test the A22 physical kernel with a point simulator, outside the certified setting:
noise, other inputs, other topologies, ablations of the learning rule and longer training. They are
sampled simulations, not proofs. The certified engine is never used. Each claim below holds for the
stated protocol and sample only.

## The main findings so far

**1. The learning rule finds a lane-specific gain allocation that transmits reliably under noise, with
less gain than any working uniform setting of the tested grid.** After 2,048 noisy training pulses (gains frozen at test), the
network transmits complete 128-pulse words at layer 130 in 19 or 20 of 20 seeds at each of three noise
levels, with a mean gain of about 1.5. Uniform gains fixed by hand need at least 1.8, 2 and 3 for the
same result; at a uniform 1.6, no seed gives a complete word. Shuffling the learned gains, even
preserving each layer's and each port's distribution, destroys transmission (0 of 40)
([`gain_sweep_shuffle_130/`](gain_sweep_shuffle_130/README.md)).

**2. Learning is not necessary if high gains can be set by hand.** Gains fixed at 4 from the start, with
no learning, transmit every pulse in all 60 realizations, with better timing; at a faster input rate,
fast recovery is also needed ([`fixed_gain_130/`](fixed_gain_130/README.md)). What learning provides is
the allocation above, found autonomously from a nominal state that does not ignite on its own.

**3. Noise during training matters.** From the nominal state, noisy training beats clean training of the
same duration by 21 to 91 points of recall (gains frozen at test), and the learned margin scales with
the training noise ([`gate_noise_130/`](gate_noise_130/README.md)).

**4. The protection gate stops learning; it is not what produces robustness.** Without the gate, gains
rise to whatever cap is set (4, 8 or 16) and transmission stays reliable through saturation. With the
gate, gains stay near 1.5 whatever the cap; restoring the gate stops growth at once
([`gate_cap_restore_130/`](gate_cap_restore_130/README.md)). Without noise, learning then stops
completely; under noise, a small residual growth remains.

**5. There is no energy advantage in the model's own cost law.** With the energy reserve integrated,
the gated network costs slightly more than the ungated one (+2 to +11 %), mostly because it ends with a
slower recovery and so spends longer in the costly slow protected phase; the law charges nothing for
maintaining a large gain ([`energy_130/`](energy_130/README.md)). The case for learning is therefore
self-organization, not economy: from a state that does not ignite, the rule finds a working,
lane-specific configuration on its own, adapts its margin to the noise it meets, and then
largely stops changing (completely without noise).

Timing remains approximate under noise (about 0.5 to 1.3 % relative RMS on the intervals).

## The studies

| Folder | Question | Key result |
|---|---|---|
| [`robustness/`](robustness/README.md) | How does the kernel react to noise, closer pulses, other shapes and topologies? (18 and 130 layers, 128 training pulses) | Gradual degradation for small noise; discrete losses for larger noise; losses accumulate with depth. Works with gaps down to 7 and with all tested topologies without noise. |
| [`ablations_130/`](ablations_130/README.md) | Which part of the learning rule matters? (130 layers, 128 training pulses, 20 seeds) | Without learning, the network never ignites. With only 128 training pulses, plasticity left active during protection gave no complete word even without noise, and with noise the training does not reach layer 130. |
| [`noisy_training_130/`](noisy_training_130/README.md) | Does longer noisy training install a robust regime at 130 layers? (20 seeds, paired controls) | Yes in 20/20 seeds, against 0/20 for clean training of the same duration. Its 24-pulse test partly reused training noise (see the correction in its README). |
| [`gate_noise_130/`](gate_noise_130/README.md) | Is the protection gate needed for robustness? Does the effect hold at three noise levels? (2,048 training pulses, 20 seeds per level) | The gate is not needed; without it gains saturate. The noisy-training benefit is confirmed at all three levels with fully separate noise. |
| [`gate_cap_restore_130/`](gate_cap_restore_130/README.md) | Does the gate stop gain growth, or only the cap? (caps 4, 8, 16; gate restored after one pulse; 20 seeds per level) | Without the gate, gains follow the cap; with it, they stay near 1.5 whatever the cap; restoring it stops growth at once. |
| [`fixed_gain_130/`](fixed_gain_130/README.md) | Can high gains fixed by hand replace learning? (gains 4 from t = 0; two input rates; 20 seeds per level) | Yes: 60 of 60 complete words, with better timing; at a faster rate, fast recovery is also needed. |
| [`gain_sweep_shuffle_130/`](gain_sweep_shuffle_130/README.md) | How large must uniform gains be? Does the placement of learned gains matter? (uniform sweep 0.3 to 4; three shuffle types; 20 seeds per level) | Uniform gains need 1.8 / 2 / 3; learned gains work at about 1.5; shuffling them destroys transmission. |
| [`energy_130/`](energy_130/README.md) | Is the gated network cheaper to run? (energy reserve integrated; matched gate on/off from the same state; 20 seeds per level) | No: it costs 2 to 11 % more, mostly through a longer slow protected phase. |

## What is still open

- Whether a hand-designed non-uniform allocation (for example, strong central and weak lateral ports,
  without phase information) matches the learned one at the same gain level.
- A cost measure in which lower gains matter: the model charges nothing for maintaining a gain, and its
  reserve E never approaches depletion in these runs.
- Whether learning settles under bounded noise; continuous noise, physical-parameter uncertainty and
  other topologies with the longer training.
- Any guarantee for every realization: these are 2 to 20 sampled runs per condition.

The code, runs and reports were produced with AI assistants under the author's direction. The
detailed reports (`rapport.html`, or the PDF in `gate_noise_130/`) are in French; each folder has an English README.
