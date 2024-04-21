# Maltodextrin

## Description:

Maltodextrin is popular; I wish this one can be popular too.

## Flag:

```
UMASS{Th1s_1nstruct10n_S3t_Arch1t3ctur3_1s_3P1C}
```

## Internal description:

This challenge is a multi-byte XOR algorithm compiled for IA-64.
Generated assembly is given to the player.

## Solve:

You can notice the loop described in three pack of instructions.
A little bit understanding of rotating registers is needed here.
We should see strncmp, and if we trace backward, we will find
the instructions for adding data.

