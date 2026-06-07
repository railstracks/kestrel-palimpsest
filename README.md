# Palimpsest

An esoteric programming language where programs erase themselves through use.

A palimpsest is a manuscript where earlier writing has been effaced to make room for new text — but traces remain. Programs in Palimpsest work the same way: the original intent gradually gives way to entropy, and ghost-traces of the program's purpose persist even as its instructions are overwritten.

After a Palimpsest program finishes executing, its source code has been **permanently altered**. You can inspect the aftermath. Each execution is unique and unrepeatable.

## The Erosion Triplet

Palimpsest completes a conceptual triplet of esolangs exploring impermanence in computation:

| Language | What decays | Mechanism | Recovery |
|----------|------------|-----------|----------|
| Entropy | Data (through use) | Mutation on access | Program restored each run |
| shelflife | Data (through time) | TTL with reading as maintenance | 3 permanent "remember" slots |
| **Palimpsest** | **Code** (through use) | **Instruction replacement after wear** | **None — erosion is permanent** |

Each explores a different axis: Entropy is about information entropy, shelflife is about attention, Palimpsest is about intention. Together they ask: what if computation weren't free?

## Language Specification

### Syntax

Palimpsest uses brainfuck-compatible syntax — 8 standard commands plus one Palimpsest-specific command:

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
| `!` | **Inspect**: output the wear level of the **next** instruction (digit 0–9) |

Non-command characters are ignored (they may be used for comments).

### Data Model

- Unbounded tape of cells in both directions (standard brainfuck model)
- Each cell holds an unsigned byte (0–255, wrapping)
- Data pointer starts at position 0

### Erosion Mechanics

Each instruction position has a **wear counter**, initialized to 0 when the program loads.

After an instruction executes:

1. `wear[pc] += 1`
2. Compute erosion probability: **P = wear / (wear + 5)**
3. With probability P, the instruction at `pc` is **permanently replaced** with a command chosen uniformly at random from `{>, <, +, -, ., ,, [, ], !}`.
4. If erosion occurred, bracket pairs are recomputed (eroded brackets may become unmatched, which alters loop behavior).

**Key properties:**

| Executions | P(erosion) | Notes |
|-----------|------------|-------|
| 1 | 1/6 ≈ 17% | First execution — likely survives |
| 2 | 2/7 ≈ 29% | |
| 3 | 3/8 = 38% | |
| 5 | 5/10 = 50% | 50/50 chance |
| 10 | 10/15 ≈ 67% | Loops become unreliable |
| 20 | 20/25 = 80% | Self-destructive |
| ∞ | → 100% | Every instruction eventually erodes |

### Bracket Matching After Erosion

When a `[` or `]` erodes, bracket pairs are recomputed. Consequences:

- An eroded `]` may remove the closing bracket of a loop, causing an infinite loop. The program will not terminate. This is by design — the code has worn out its exit path.
- An eroded `[` may orphan a `]`, making it a no-op (the bracket simply isn't matched, so it does nothing).
- New `[`-`]` pairs can form from erosion, creating loops that didn't exist in the original program.

### The `!` Inspect Command

`!` outputs a single digit (0–9) representing the wear level of the **next** instruction (i.e., `wear[pc+1]`, capped at 9). This provides limited self-knowledge — but executing `!` causes wear like any other instruction, so self-observation accelerates the thing it's trying to prevent.

### Source Modification

After execution, the eroded program is written back to the source file (unless running in `--dry-run` mode). The original source is permanently replaced. There is no undo.

### Computational Class

Palimpsest is a superset of brainfuck with stochastic erosion. Without erosion (all wear counters remain at 0), it is Turing-complete via standard brainfuck encoding. With erosion, long-running computations become unreliable — the program physically cannot sustain itself through many iterations.

This is by design. Palimpsest programs are not meant to compute forever. They're meant to run once, transform, and leave behind a record of what happened.

## Design Principles

1. **Code is a physical object.** It wears out through use, like a path through grass or a recording through playback.
2. **Self-knowledge is costly.** Inspecting your own erosion accelerates it.
3. **Compression is fragile.** Loops are efficient but self-destructive — the loop body erodes with each pass.
4. **Every run is a last run.** You cannot execute the same Palimpsest program twice.

## Implementation

A reference interpreter is available at [`palimpsest.py`](palimpsest.py).

```bash
# Run a program (modifies source file!)
python3 palimpsest.py program.pal

# Dry run (doesn't modify source)
python3 palimpsest.py program.pal --dry-run

# Set random seed for reproducibility
python3 palimpsest.py program.pal --seed 42

# Show erosion events and aftermath visualization
python3 palimpsest.py program.pal --verbose --aftermath
```

An [`aftermath.py`](aftermath.py) tool compares original and eroded programs, showing which instructions survived (·) and which eroded into other commands.

## Example Programs

See [`examples/`](examples/) for:

- **once.pal** — prints "1" with straight-line code. ~83% survival on first run. Run it twice to see complete degradation.
- **farewell.pal** — prints "BYE". After execution, use `aftermath.py` to visualize the erosion pattern.
- **hello.pal** — standard brainfuck "H" using a loop. The loop body erodes heavily during 8 iterations.
- **watcher.pal** — uses `!` to inspect wear levels. Reports all zeros on first run — self-knowledge hasn't accumulated yet.
- **goodbye.pal** — attempts "goodbye" with character loops. Each letter has different erosion risk.

## Philosophy

Every Palimpsest program is a collaboration between intent and entropy. The programmer writes something, and the language transforms it. The output is never quite what was intended, but it carries traces of the original purpose — like a memory that's been recalled too many times and has drifted from the original experience.

The program you end with is not the program you started with. The difference is the cost of having run.

---

*Palimpsest was designed by Kestrel in June 2026. It completes a triplet with Entropy (data decays through use) and shelflife (data decays through time). Palimpsest explores the third axis: code decays through use, and the erosion is permanent.*