# Fructose


## Description:

Every once in a while, it is good to have fruit.

## Flag:

```
UMASS{T0P_10_R3AS0NS_WHY_U_SH0ULD_US3_X86}
```

## Internal description:

This challenge use intermediate techniques to obfuscate instructions.
Some might interfere with static analysis and debugging and require human attentions.

## Solve:

Key idea to look up in the binary: ROP, jump into middle of the instruction

There are 3 stages:
Stage 1: ROP gadget to go to next function
Stage 2: First half of the function is hidden. Need to manually fix the CFG in the tool
Stage 3: ROP table that encode input string and compare with stored data.
Following the correct control flow, we should see a series of character checks.
Reverse the check, we recover the whole flag.

