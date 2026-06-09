Examples for the Palimpsest esoteric programming language.

| Example | Strategy | First-run output | Behavior on re-runs |
|---------|----------|------------------|---------------------|
| once.pal | Straight-line | "1" | High survival on first run; degrades across re-runs |
| straight_h.pal | Straight-line | "H" | 73 instructions, each runs once — survives reliably |
| loop_h.pal | Loop (8×9) | "H" (if it survives) | Loop body erodes with each iteration — self-destructive |
| straight_bye.pal | Straight-line | "BYE" | Moderate survival; characters drift on re-runs |
| farewell.pal | Straight-line | "HEY" | Progressive degradation across multiple runs |
| observer.pal | Loop + inspect | Wear levels "012…" | Uses `!` to read its own erosion; self-aware and self-destructive |
| survey.pal | 54× inspect | All zeros | Self-inspection: reads wear levels on first run, erodes on re-runs |

### Key demonstrations

**Verbosity vs. compression:** Compare `straight_h.pal` (73 instructions, survives) with `loop_h.pal` (24 instructions, self-destructs). Same output on paper — completely different reliability.

**Progressive erosion:** Run `farewell.pal` multiple times (without `--dry-run`):
```
Run 1: HEY
Run 2: 01223341525005003304
Run 3: 0500010000ÿ00110000
Run 4: 000010000ÿ0ÿ0
Run 5: 00
```
Each run produces different output as instructions erode. The `!` commands left by erosion output wear digits; cell operations produce random bytes. The program converges toward noise.

**Self-observation:** `observer.pal` uses `!` inside a loop. The `!` command reads the wear level of the next instruction, outputting it as a digit. On first run, it shows increasing wear (0, 1, 2…) as the loop body accumulates uses. Each `!` also causes wear — observing erosion accelerates it.

**Self-inspection:** `survey.pal` is 54 `!` commands. On first run, all wear levels are 0 (fresh program). Each `!` causes wear on itself, so the program is reading its own degradation in real-time. Re-run the eroded source and the landscape changes.