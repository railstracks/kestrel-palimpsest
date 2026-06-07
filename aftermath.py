#!/usr/bin/env python3
"""
Visualize the aftermath of a Palimpsest program.

Compares the original and eroded versions, showing what survived and what changed.
"""

import sys

COMMANDS = set('><+-.,[]!')

def load_program(path):
    with open(path, 'r') as f:
        source = f.read()
    return [c for c in source if c in COMMANDS]

def visualize(original, eroded):
    print("Aftermath — Palimpsest erosion visualization")
    print("=" * 60)
    
    # Show original vs eroded side by side (60 chars per line)
    width = 60
    for start in range(0, max(len(original), len(eroded)), width):
        orig_line = ''.join(original[start:start+width])
        eros_line = ''.join(eroded[start:start+width])
        
        # Build diff visualization
        diff = []
        for i in range(start, min(start + width, max(len(original), len(eroded)))):
            o = original[i] if i < len(original) else ' '
            e = eroded[i] if i < len(eroded) else ' '
            if o == e:
                diff.append('·')  # survived
            else:
                diff.append(e)   # eroded
        
        print(f"  {orig_line}")
        print(f"  {''.join(diff)}")
        print()

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} original.pal eroded.pal")
        sys.exit(1)
    
    original = load_program(sys.argv[1])
    eroded = load_program(sys.argv[2])
    
    visualize(original, eroded)
    
    survived = sum(1 for a, b in zip(original, eroded) if a == b)
    total = len(original)
    pct = 100 * survived // max(total, 1)
    print(f"Survived: {survived}/{total} ({pct}%)")
    print(f"Legend: · = survived, any other char = eroded to that command")

if __name__ == '__main__':
    main()
