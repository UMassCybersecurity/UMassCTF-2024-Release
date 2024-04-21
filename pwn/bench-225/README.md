# bench-225
Author: RS311
Description: Life is one big tug of war. And you don't win the war by pushing the rope.

## Intended Solution
- Bench-press 225 until the stamina is lower than 50. This will unlock the motivational quotes option.
- Leak the canary, elf address with the motivational quotes.
- Do a motivational quote.
    - Buffer overflow + Canary + RBP overflow + ROP Chain to Open, Read, Write flag.txt

## Flag
`UMASS{wh0$e_g0nn4_c4rry_t3h_r0pz_&nd_d4_ch41nz?}`