# Palimpsest — Example Programs

## hello.pal
```brainfuck
++++++++[>+++++++++<-]>.
```
Standard brainfuck "H". The loop runs 8 times, causing heavy erosion in the loop body. On first run, output is approximately correct. The source degrades permanently.

## straight_h.pal
```brainfuck
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.
```
Same "H" but without any loops. 72 increments then print. Each instruction executes once, so erosion probability is only ~17%. Most of the program survives the first run. But it's already changed.

## once.pal
```brainfuck
+++++++++++++++++++++++++++++++++++++++++++++++++.
```
Prints "1" (ASCII 49) with straight-line code. Each instruction executed once. ~83% first-run survival. But after running, the source is permanently altered — you can never run the same program again.

## farewell.pal
Prints "BYE" using straight-line character loads (B=66, Y=89, E=69). After execution, the aftermath shows which parts survived and which eroded. Run the eroded source a second time to see complete degradation.

## goodbye.pal
```brainfuck
+++++++++++++++[>+<-]>.<++++++++++++[>+<-]>.<++++++++++[>+<-]>.<+++++++++[>+<-]>.<+++++++++++[>+<-]>.<++++++[>+<-]>.
```
Attempts to print "goodbye" using individual character loops. Each letter has different erosion risk — letters requiring more loop iterations accumulate more wear. Heavily self-destructive.

## watcher.pal
```brainfuck
!!>!!<!!+!!-!!.
```
Uses the `!` inspect command to output wear levels of subsequent instructions. On first run, all wear levels are 0 — the program reports a pristine state that's already changing as it reports it. Self-knowledge has a cost.

## alphabet/
Run `python3 gen_alpha.py` to generate an alphabet program (A-J) that demonstrates progressive erosion: earlier letters (shorter loops) partially survive, later letters become noise.

## Running Examples

```bash
# Run once (MODIFIES source file!)
cp examples/once.pal /tmp/test.pal
python3 palimpsest.py /tmp/test.pal --verbose

# Dry run (safe — doesn't modify source)
python3 palimpsest.py examples/farewell.pal --dry-run --verbose

# Set seed for reproducibility
python3 palimpsest.py /tmp/test.pal --seed 42 --verbose

# Show aftermath visualization
cp examples/farewell.pal /tmp/orig.pal
python3 palimpsest.py /tmp/orig.pal
python3 aftermath.py examples/farewell.pal /tmp/orig.pal

# Second run on eroded source
cp /tmp/orig.pal /tmp/eroded.pal
python3 palimpsest.py /tmp/eroded.pal --verbose
# Output will be garbage — the program has eaten itself
```

## Key Demonstrations

1. **First run works, second run doesn't** — Run `once.pal` twice. First: `1`. Second: garbage.
2. **Loops self-destruct** — Run `hello.pal` with `--verbose`. The loop body erodes heavily.
3. **Aftermath visualization** — Run `farewell.pal` then use `aftermath.py` to compare original vs eroded.
4. **Progressive corruption** — Generate and run the alphabet program to see letters degrade in real-time.