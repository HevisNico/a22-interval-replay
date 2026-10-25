# Exploratory simulations (not certified)

These studies test the A22 physical kernel with a point simulator, outside the certified setting:
noise, other inputs, other topologies, ablations of the learning rule and longer training. They are
sampled simulations, not proofs. The certified engine is never used. Each claim below holds for the
stated protocol and sample only.

## The main finding so far

**Training under noise produces a network that transmits reliably under that noise, at 130 layers.**
With noisy training continued until the training pulses reach the output, 20 networks out of 20
transmit every test pulse on all 12 output lanes, under 10 % amplitude noise and 0.03 jitter on every
connection. Networks trained for the same duration without noise, then tested under the same noise,
recover 85 % of the pulses and never a complete word (0 out of 20). Freezing the gains during the test
does not change the result: the robustness is stored in the learned state, not repaired on line.
The timing remains noisy: about 1 % relative RMS error on the intervals.

## The three studies

| Folder | Question | Key result |
|---|---|---|
| [`robustness/`](robustness/README.md) | How does the kernel react to noise, closer pulses, other shapes and topologies? (18 and 130 layers, 128 training pulses) | Gradual degradation for small noise; discrete losses for larger noise; losses accumulate with depth. Works with gaps down to 7 and with all tested topologies without noise. |
| [`ablations_130/`](ablations_130/README.md) | Which part of the learning rule matters? (130 layers, 128 training pulses, 20 seeds) | Without learning, the network never ignites. Plasticity left active during protection breaks exact transmission even without noise. With noise, 128 training pulses are not enough for the training to reach layer 130. |
| [`noisy_training_130/`](noisy_training_130/README.md) | Does longer noisy training install a robust regime at 130 layers? (20 seeds, paired controls) | Yes in 20/20 seeds (see above), against 0/20 for clean training of the same duration. |

## What is still open

- Whether protection-gated plasticity is *necessary* for robustness under noise: the ablation of the
  gate was not repeated with the longer training.
- Other noise levels, continuous noise, physical-parameter uncertainty and other topologies with the
  longer training.
- Any guarantee for every realization: these are 2 to 20 sampled runs per condition.

The code, runs and reports were produced with AI assistants under the author's direction. The
detailed reports (`rapport.html`) are in French; each folder has an English README.
