Examples for the Palimpsest esoteric programming language.

| Example | Strategy | Expected output | Reliability |
|---------|----------|----------------|-------------|
| once.pal | Straight-line | "1" | High (first run), degrades on re-runs |
| straight_h.pal | Straight-line | "H" | High — 73 instructions, each runs once |
| loop_h.pal | Loop (8×9) | "H" | Low — loop body erodes after ~3 iterations |
| straight_bye.pal | Straight-line | "BYE" | Moderate — long but no loops |
| survey.pal | 54× inspect | Wear readings (all 0 on first run) | Self-destructive — `!` causes wear |
