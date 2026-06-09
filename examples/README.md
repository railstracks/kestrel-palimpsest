Examples for the Palimpsest esoteric programming language.

| Example | Strategy | First-run output | Behavior on re-runs |
|---------|----------|------------------|---------------------|
| once.pal | Straight-line | "1" | High survival on first run; degrades across re-runs |
| straight_h.pal | Straight-line | "H" | 73 instructions, each runs once — survives reliably |
| loop_h.pal | Loop (8×9) | "H" (if it survives) | Loop body erodes with each iteration — self-destructive |
| straight_bye.pal | Straight-line | "BYE" (approx.) | Moderate survival; characters drift on re-runs |
| farewell.pal | Straight-line | "HEY" | Progressive degradation across multiple runs |
| observer.pal | Loop + inspect | Wear levels "012…" | Uses `!` to read its own erosion; self-aware and self-destructive |
| survey.pal | 54× inspect | All zeros | Self-inspection: reads wear levels on first run, erodes on re-runs |
| cascade.pal | Loop + inspect | "01234" (ascending wear) | Self-counting erosion thermometer; loop degrades after 3–5 digits |
| chamber.pal | Input + echo | Input char × 20 | Echo degrades; the program goes deaf as `,` erodes |

### Key demonstrations

**Verbosity vs. compression:** Compare `straight_h.pal` (73 instructions, survives) with `loop_h.pal` (24 instructions, self-destructs). Same output on paper — completely different reliability. Palimpsest rewards verbosity and punishes compression.

**Progressive erosion:** Run `farewell.pal` multiple times (without `--dry-run`):
```
Run 1: HEY
Run 2: ·01000···3··2··1··5···0··0···0
Run 3: ·0122·01·2·3···112001····5·0·000···0·00
Run 4: ····00·0··00··0··0··0·11·····02···3·343·····00·00
Run 5: ·040560···000··000·0··0000·0··000··0112·11··23·2··2·22···0000·000
```
Each run produces different output as instructions erode. The `!` commands left by erosion output wear digits; cell operations produce non-printable bytes (shown as `·`). The program converges toward noise.

**Self-observation:** `observer.pal` uses `!` inside a loop. The `!` command reads the wear level of the next instruction, outputting it as a digit. On first run, it shows increasing wear (0, 1, 2…) as the loop iterates. Each `!` also causes wear — observing erosion accelerates it.

**Erosion cascade:** `cascade.pal` counts its own wear in real-time. A loop iterates 10 times, outputting the wear level of the next instruction each pass. On a fresh run, this produces ascending digits: `0`, `1`, `2`, `3`, `4` — the program is counting how many times each instruction has been used. The loop self-destructs after a few iterations, cutting the count short. Each re-run produces different digits as accumulated wear shifts the baseline.

```
$ python3 palimpsest.py examples/cascade.pal --dry-run --seed 25
01234
```

**Echo chamber:** `chamber.pal` reads one character from input and echoes it 20 times. On first run, this is a perfect echo — type `K`, get `KKKKKKKKKKKKKKKKKKKK`. On re-runs, the `,` (input) and `.` (output) commands erode. The program gradually goes deaf: it can no longer hear input, and it can no longer speak. The echo becomes silence.

```
$ echo -n "K" | python3 palimpsest.py examples/chamber.pal
KKKKKKKKKKKKKKKKKKKK
```

**Self-inspection:** `survey.pal` is 54 `!` commands. On first run, all wear levels are 0 (fresh program). Each `!` causes wear on itself, so the program is reading its own degradation in real-time. Re-run the eroded source and see a different landscape.