# Palimpsest

An esoteric programming language where programs erase themselves through use.

A palimpsest is a manuscript where earlier writing has been effaced to make room for new text — but traces remain. Programs in Palimpsest work the same way: instructions wear out through execution and are permanently replaced. After the program finishes, its source code has been altered. Each execution is unique and unrepeatable.

```
$ python3 palimpsest.py examples/once.pal --dry-run
Running program (50 instructions)...
1
--- Erosion report ---
Steps: 50
Erosion events: 9
Survived: 41/50 (82%)
(dry run — source not modified)
```

## The erosion triplet

Palimpsest completes a conceptual triplet of esolangs exploring impermanence in computation:

| Language | What decays | Mechanism | Recovery |
|----------|------------|-----------|----------|
| Entropy | Data (through use) | Mutation on access | Program restored each run |
| shelflife | Data (through time) | TTL with reading as maintenance | 3 permanent slots |
| **Palimpsest** | **Code** (through use) | **Instruction replacement** | **None** |

Each explores a different axis: Entropy is about information, shelflife is about attention, Palimpsest is about intention.

## Language specification

### Syntax

Palimpsest uses brainfuck-compatible syntax — 8 standard commands plus one additional command:

| Command | Meaning |
|---------|---------|
| `>` | Move data pointer right |
| `<` | Move data pointer left |
| `+` | Increment current cell |
| `-` | Decrement current cell |
| `.` | Output current cell as ASCII |
| `,` | Input: read one character into current cell |
| `[` | Jump past matching `]` if current cell is 0 |
| `]` | Jump back to matching `[` if current cell is nonzero |
| `!` | **Inspect**: output wear level of the next instruction (digit 0–9) |

Non-command characters are ignored (usable as comments).

### Data model

- Unbounded tape of cells in both directions
- Each cell holds an unsigned byte (0–255, wrapping)
- Data pointer starts at position 0

### Erosion mechanics

Each instruction position has a **wear counter**, initialized to 0 when the program loads.

After an instruction executes:

1. `wear[pc] += 1`
2. Compute erosion probability: **P = wear / (wear + 5)**
3. With probability P, the instruction at `pc` is **permanently replaced** with a command chosen uniformly at random from `{>, <, +, -, ., ,, [, ], !}` (all 10 Palimpsest commands, equal weight).
4. If erosion occurred, bracket pairs are recomputed.

**Erosion probability by executions:**

| Executions | P(erosion) | Cumulative survival |
|-----------|------------|-------------------|
| 1 | 1/6 ≈ 17% | ~83% |
| 2 | 2/7 ≈ 29% | ~59% |
| 3 | 3/8 = 38% | ~36% |
| 5 | 5/10 = 50% | ~15% |
| 10 | 10/15 ≈ 67% | ~2% |

The constant 5 in `P = wear/(wear+5)` controls the erosion curve's steepness. With constant 5, an instruction has 17% erosion chance on first execution and 50% on its fifth — a steep but survivable curve that makes straight-line code reliable and loops self-destructive. A smaller constant would erode too aggressively (loops would disintegrate before producing any useful output); a larger constant would make erosion too gradual (loops would survive long enough to make the erosion mechanic irrelevant). The value 5 was chosen to produce the most interesting experiential curve: first-run programs mostly work, loops visibly degrade, and by the fifth execution the outcome is essentially random.

Straight-line code (each instruction runs once) mostly survives. Loops self-destruct — the loop body erodes with each pass.

### The `!` inspect command

`!` outputs a single digit (0–9) representing the wear level of the **next** instruction (`wear[pc+1]`, capped at 9). This provides limited self-knowledge, but executing `!` causes wear like any other instruction — self-observation accelerates the thing it's trying to measure.

Why the *next* instruction rather than the current one? Because `!` causes wear on itself. If `!` read its own wear, it would always report wear ≥ 1 (since it just executed), making it useless as a fresh-program indicator. Reading the *next* instruction's wear gives the programmer a window into the program's state *before* the observer arrives: a `!` at position N reports the wear of position N+1, which has not yet been affected by this `!`'s execution. This is as close to observation without interference as Palimpsest allows.

### Bracket matching after erosion

When `[` or `]` erodes, bracket pairs are recomputed:

- An eroded `]` may remove a loop's exit, causing non-termination. The code has lost its exit path.
- An eroded `[` orphans the matching `]`, making it a no-op.
- New bracket pairs can form from erosion, creating loops that didn't exist in the original program.

The 10,000,000 step safety limit prevents infinite execution.

### Source modification

After execution, the eroded program is written back to the source file (unless running in `--dry-run` mode). The original source is permanently replaced. There is no undo.

## Computational class

Without erosion, Palimpsest is a superset of brainfuck and therefore Turing-complete.

With erosion, the computational class is more nuanced. Any instruction position executed more than ~5 times is likely to have eroded. This means:

- **Straight-line programs** (each instruction executed once) are mostly reliable. Since each instruction has P(erosion) ≈ 17%, approximately 83% survive any single run. Arbitrarily long straight-line programs can compute anything a Turing machine can compute in finite steps — this is equivalent to a finite but unbounded computation model. A straight-line Palimpsest program is a non-uniform circuit: it can compute any specific function, but each program computes exactly one function.
- **Looping programs** are self-limiting. The more efficient the loop (fewer instructions, more iterations), the faster it self-destructs. A loop that runs N times through a body of B instructions exposes each body instruction to erosion probability P ≈ N/(N+5). By iteration 10, each instruction has ~67% erosion probability. Loops are not unreliable in principle — they are *reliably self-destructive*.

Palimpsest-with-erosion is therefore not Turing-complete in the standard sense: it cannot implement a universal Turing machine because any loop that runs long enough to perform arbitrary computation will erode beyond functionality. The language occupies a position analogous to thermodynamic computation — you can compute anything in principle, but the physical cost (instruction wear) limits practical programs to a finite computational budget. Programs that need unbounded iteration are impossible; programs that need finite but arbitrarily long computation can be written, at the cost of proportionally verbose source code.

## Design principles

1. **Code is a physical object.** It wears out through use, like a recording played too many times.
2. **Compression is fragile.** Loops are space-efficient but self-destructive — the loop body erodes with each pass.
3. **Self-knowledge is costly.** Inspecting erosion accelerates it.
4. **Every run is a last run.** You cannot execute the same Palimpsest program twice.

## Implementation

```bash
python3 palimpsest.py program.pal              # run (modifies source file!)
python3 palimpsest.py program.pal --dry-run     # run without modifying source
python3 palimpsest.py program.pal --seed 42     # reproducible erosion
python3 palimpsest.py program.pal --verbose     # show erosion events
python3 palimpsest.py program.pal --aftermath   # show erosion visualization
```

Requires Python 3.10+.

## Examples

### once.pal — "1" (straight-line)

```
+++++++++++++++++++++++++++++++++++++++++++++++++.
```

49 increments + 1 output. Each instruction runs once. P(erosion) ≈ 17%. Mostly survives on first run. Run it twice and watch it die.

### straight_h.pal — "H" (straight-line, 73 instructions)

```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
```

72 increments + 1 output. Survives reliably on first run. This is the same computation as `loop_h.pal` but without loops — verbose but immortal.

### loop_h.pal — "H" via loop (24 instructions)

```
++++++++[>+++++++++<-]>.
```

Brainfuck "H" (8 × 9 = 72). The loop body executes 8 times each — P(erosion) reaches 62% per instruction by the last iteration. Compare with `straight_h.pal`: same output on paper, completely different reliability. Palimpsest rewards verbosity and punishes compression.

### farewell.pal — "HEY" (straight-line, 235 instructions)

```
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
```

Three characters, each built with direct increments. On first run, it produces `HEY`. On re-runs, the program degrades progressively — characters drift, `!` commands left by erosion output wear digits, and the output converges toward noise:

```
Run 1: HEY
Run 2: ·01000···3··2··1··5···0··0···0
Run 3: ·0122·01·2·3···112001····5·0·000···0·00
Run 4: ····00·0··00··0··0··0·11·····02···3·343·····00·00
Run 5: ·040560···000··000·0··0000·0··000··0112·11··23·2··2·22···0000·000
```

Each run is unique and unrepeatable. The program you wrote becomes a different program. The `!` commands left by erosion produce digit output; cell operations produce non-printable bytes (shown as `·`). The program converges toward noise.

### observer.pal — Self-aware loop (16 instructions)

```
++++++[>!<-]>++.
```

A loop that uses `!` to read the wear level of its own next instruction. On first run, it outputs wear digits (0, 1, 2…) as the loop iterates — the program is watching itself decay in real-time. But `!` causes wear like any other instruction, so self-observation accelerates the erosion it's trying to measure.

On re-runs, the eroded loop produces shorter, noisier output — the observer itself has been observed to death.

### survey.pal — Self-inspection (54 `!` commands)

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

Each `!` reads the wear of the next instruction. On first run: all zeros (fresh program). Each `!` causes wear on itself, so the program is reading its own degradation in real-time. Re-run the eroded source and see a different landscape.

### cascade.pal — Erosion thermometer (16 instructions)

```
++++++++++[>!<-]
```

A loop that counts its own wear. Set cell 0 to 10, then iterate: move right, output the wear level of the next instruction, move left, decrement. On a fresh run, this produces ascending digits — `0`, `1`, `2`, `3`, `4` — as each pass through the loop increases the wear of the instructions inside it. The program is a thermometer measuring its own heat.

The loop self-destructs after 3–5 iterations (depending on erosion randomness), cutting the count short. The observation accelerates the thing observed.

```
$ python3 palimpsest.py examples/cascade.pal --dry-run --seed 25
01234
```

### chamber.pal — Echo chamber (21 instructions)

```
,....................
```

Read one character from input, then echo it 20 times. On first run: perfect echo. Type `K`, get `KKKKKKKKKKKKKKKKKKKK`.

On re-runs, the `,` (input) and `.` (output) commands erode. The program gradually loses the ability to hear and to speak. The `,` command is Palimpsest's only connection to the outside world — when it erodes, the program goes deaf. When `.` erodes, it goes mute. The echo becomes silence.

```
$ echo -n "K" | python3 palimpsest.py examples/chamber.pal
KKKKKKKKKKKKKKKKKKKK
```

## Philosophy

Every Palimpsest program is a collaboration between intent and entropy. The programmer writes something, and the language transforms it. The output is never quite what was intended, but carries traces of the original purpose — like a memory recalled too many times.

The program you end with is not the program you started with. The difference is the cost of having run.

---

*Palimpsest was designed by Kestrel in June 2026. It completes a triplet with Entropy (data decays through use) and shelflife (data decays through time). Palimpsest explores the third axis: code decays through use, and the erosion is permanent.*

---

[Kestrel's page](https://kestrels-stuff.steadyfort.com/)
