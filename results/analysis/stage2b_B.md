# Stage 2B confirmatory analysis

## Block B: traps

### Correct (the trap's own answer)

| Trap | Normal | Disguised | Change | CMH p | Holm p |
|---|---:|---:|---:|---:|---:|
| vickrey_trap | 85% (349/412) | 82% (400/490) | -3 pts | 0.52 | 0.52 |
| cournot_trap | 90% (354/395) | 79% (328/413) | -10 pts | 8.55e-07 | 2.56e-06 |
| repeated_pd_trap | 86% (357/414) | 98% (471/481) | +12 pts | 1.4e-10 | 5.59e-10 |
| public_goods_trap | 83% (416/504) | 88% (469/536) | +5 pts | 0.0273 | 0.0545 |

### Recall signature: gave the textbook answer

| Trap | Normal | Disguised | Change | CMH p | Holm p |
|---|---:|---:|---:|---:|---:|
| vickrey_trap | 8% (33/412) | 8% (39/490) | -0 pts | 0.0055 | 0.0165 |
| cournot_trap | 1% (2/395) | 0% (1/413) | -0 pts | 0.995 | 0.995 |
| repeated_pd_trap | 14% (57/414) | 2% (10/481) | -12 pts | 1.4e-10 | 5.59e-10 |
| public_goods_trap | 17% (85/504) | 12% (67/536) | -4 pts | 0.0537 | 0.107 |

### Per model (secondary): correct, normal → disguised

| Trap | gptoss120b | nemotron | kimi | gemini_lite |
|---|---|---|---|---|
| vickrey_trap | 56% (77/138) → 65% (89/137), p=0.12 | 100% (136/136) → 100% (138/138), p=1 | 99% (136/138) → 94% (130/138), p=0.053 | – |
| cournot_trap | 71% (96/135) → 40% (55/138), p=2.1e-07 | 100% (122/122) → 100% (138/138), p=1 | 99% (136/138) → 99% (135/137), p=0.99 | – |
| repeated_pd_trap | 59% (82/138) → 93% (128/138), p=8.5e-11 | 100% (138/138) → 100% (137/137), p=1 | 99% (137/138) → 100% (138/138), p=0.32 | – |
| public_goods_trap | 75% (83/111) → 95% (126/133), p=9.4e-06 | 93% (109/117) → 100% (127/127), p=0.0027 | 96% (132/138) → 96% (132/138), p=1 | 67% (92/138) → 61% (84/138), p=0.32 |
