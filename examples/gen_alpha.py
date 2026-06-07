#!/usr/bin/env python3
"""Generate an alphabet program for Palimpsest that shows progressive erosion."""
# Each letter is loaded via a small loop. Earlier letters use fewer iterations
# and survive; later letters use more iterations and self-destruct.
# The output shows the alphabet becoming progressively corrupted.

output = []
for i, ch in enumerate("ABCDEFGHIJ"):
    val = ord(ch)
    # Use a loop of (val // 10) iterations to load val
    # This means 'A'(65) needs 7 iterations, 'J'(74) needs 8
    # More iterations = more erosion in the loop body
    n = val // 10
    remainder = val - n * 10
    code = '+' * n  # counter
    code += '['
    code += '>' + '+' * 10 + '<' + '-'  # add 10 to target
    code += ']'
    code += '>' + '+' * remainder + '.'  # add remainder and print
    code += '>'  # move to next cell for next char
    output.append(code)

program = ''.join(output)
with open('/tmp/test-alpha.pal', 'w') as f:
    f.write(program)
print(program)
print(f"\nTotal instructions: {len(program)}")
