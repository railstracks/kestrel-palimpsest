#!/usr/bin/env python3
"""
Palimpsest interpreter — programs that erase themselves through use.

An esoteric programming language where each instruction erodes through execution.
After enough uses, instructions are permanently replaced with random commands.
The program is modified in place — every run is unique and unrepeatable.

Usage:
    python3 palimpsest.py program.pal              # run (modifies source file!)
    python3 palimpsest.py program.pal --dry-run     # run without modifying source
    python3 palimpsest.py program.pal --seed N      # set random seed
    python3 palimpsest.py program.pal --aftermath   # show erosion diff after run
"""

import sys
import random
import argparse

COMMANDS = '><+-.,[]!'
VALID = set(COMMANDS)

def load_program(path):
    """Load program, filtering to valid commands."""
    with open(path, 'r') as f:
        source = f.read()
    return [c for c in source if c in VALID]

def save_program(path, instructions):
    """Save (possibly eroded) program back to file."""
    with open(path, 'w') as f:
        f.write(''.join(instructions))

def match_brackets(program):
    """
    Build bracket pair map. Returns dict of matched pairs.
    Unmatched brackets are simply excluded — they become no-ops.
    """
    pairs = {}
    stack = []
    for i, c in enumerate(program):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if stack:
                j = stack.pop()
                pairs[j] = i
                pairs[i] = j
            # else: orphaned ], ignored
    # Unmatched [ are just left unmatched — they become single-pass conditionals
    return pairs

def run(program, dry_run=False, seed=None):
    """
    Execute a Palimpsest program.
    Returns (output, erosion_events, eroded_program, step_count).
    """
    if seed is not None:
        random.seed(seed)
    
    instructions = list(program)
    wear = [0] * len(instructions)
    brackets = match_brackets(instructions)
    
    tape = [0]
    dp = 0  # data pointer
    pc = 0  # program counter
    
    output = []
    erosion_events = []
    
    def ensure_cell():
        """Extend tape as needed to reach dp."""
        nonlocal tape, dp
        if dp < 0:
            # Grow left — prepend zeros
            pad = [-dp]
            tape = [0] * pad[0] + tape
            dp = 0
        while dp >= len(tape):
            tape.append(0)
    
    max_steps = 10_000_000  # safety limit for eroded infinite loops
    steps = 0
    
    while pc < len(instructions) and steps < max_steps:
        cmd = instructions[pc]
        
        # Execute command
        if cmd == '>':
            dp += 1
            ensure_cell()
        elif cmd == '<':
            dp -= 1
            ensure_cell()
        elif cmd == '+':
            ensure_cell()
            tape[dp] = (tape[dp] + 1) % 256
        elif cmd == '-':
            ensure_cell()
            tape[dp] = (tape[dp] - 1) % 256
        elif cmd == '.':
            ensure_cell()
            output.append(chr(tape[dp] % 256))
        elif cmd == ',':
            ensure_cell()
            try:
                ch = sys.stdin.read(1)
                tape[dp] = ord(ch) if ch else 0
            except:
                tape[dp] = 0
        elif cmd == '[':
            ensure_cell()
            if tape[dp] == 0:
                # Jump past matching ] — if bracket was eroded, just fall through
                if pc in brackets:
                    pc = brackets[pc]
            # else: enter loop body
        elif cmd == ']':
            ensure_cell()
            if tape[dp] != 0:
                # Jump back to matching [ — if bracket was eroded, fall through
                if pc in brackets:
                    pc = brackets[pc]
            # else: exit loop
        elif cmd == '!':
            # Inspect: output wear level of the NEXT instruction (0-9)
            next_pc = pc + 1
            if next_pc < len(wear):
                w = min(wear[next_pc], 9)
                output.append(str(w))
        
        # Erosion: wear increases, then probability check
        wear[pc] += 1
        p_erode = wear[pc] / (wear[pc] + 5)
        
        if random.random() < p_erode:
            old = instructions[pc]
            # Replace with random command (uniform from all 10 commands)
            new = random.choice(list(COMMANDS))
            instructions[pc] = new
            if old != new:
                erosion_events.append((pc, old, new, wear[pc]))
            # Rebuild bracket map after every erosion check
            # (even if replacement happened to be the same command,
            # the wear state has changed)
            brackets = match_brackets(instructions)
        
        pc += 1
        steps += 1
    
    hit_limit = steps >= max_steps
    
    return ''.join(output), erosion_events, instructions, steps, hit_limit

def main():
    parser = argparse.ArgumentParser(
        description='Palimpsest: programs that erase themselves through use'
    )
    parser.add_argument('program', help='Path to .pal program file')
    parser.add_argument('--dry-run', action='store_true',
                       help="Run without modifying source file")
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show erosion event log')
    parser.add_argument('--aftermath', action='store_true',
                       help='Show erosion diff visualization')
    args = parser.parse_args()
    
    program = load_program(args.program)
    
    if not program:
        print("Empty program (no valid commands found).", file=sys.stderr)
        sys.exit(1)
    
    print(f"Running program ({len(program)} instructions)...", file=sys.stderr)
    
    output, erosions, eroded, steps, hit_limit = run(
        program, dry_run=args.dry_run, seed=args.seed
    )
    
    # Show output
    print(output, end='')
    
    # Erosion summary
    print(f"\n--- Erosion report ---", file=sys.stderr)
    print(f"Steps: {steps}", file=sys.stderr)
    if hit_limit:
        print(f"⚠ Hit step limit ({10_000_000}) — program did not terminate (eroded into infinite loop?)", file=sys.stderr)
    print(f"Erosion events: {len(erosions)}", file=sys.stderr)
    
    if args.verbose and erosions:
        print("\nErosion log:", file=sys.stderr)
        for pos, old, new, w in erosions:
            print(f"  [{pos:3d}] {old} -> {new}  (wear={w})", file=sys.stderr)
    
    # Count survivors
    survived = sum(1 for a, b in zip(program, eroded) if a == b)
    total = len(program)
    pct = 100 * survived // max(total, 1)
    print(f"Survived: {survived}/{total} ({pct}%)", file=sys.stderr)
    
    # Aftermath visualization
    if args.aftermath:
        print("\n--- Aftermath ---", file=sys.stderr)
        width = 60
        for start in range(0, total, width):
            orig = ''.join(program[start:start+width])
            erod = ''.join(eroded[start:start+width])
            diff = ''.join(
                '·' if i < len(program) and i < len(eroded) and program[i] == eroded[i]
                else (eroded[i] if i < len(eroded) else '?')
                for i in range(start, min(start + width, total))
            )
            print(f"  {orig}", file=sys.stderr)
            print(f"  {diff}", file=sys.stderr)
            print(file=sys.stderr)
    
    # Write back (unless dry run)
    if not args.dry_run:
        save_program(args.program, eroded)
        print(f"Eroded program written to {args.program}", file=sys.stderr)
        if hit_limit:
            print(f"⚠ Source was saved despite non-termination. Inspect the aftermath.", file=sys.stderr)
    else:
        print("(dry run — source not modified)", file=sys.stderr)

if __name__ == '__main__':
    main()