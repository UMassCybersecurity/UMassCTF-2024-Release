# Magic Conch
Come one, come all! For a limited time only, The Magic Conch is answering your most pressing queries!
Fun and knowledge will collide as you learn the deepest secrets of the unvierse!
If your queries are thought-provoking enough, The Magic Conch may even present you with the flag!
(Please keep your queries to 32 bytes or less; The Magic Conch does not have the patience for yappers)

# Solution
- Flag: `UMASS{dYN4M1C_an4ly$1s_4_Th3_w1n}`
- Note: You can ignore warning about `memfd_create` during compilation, it works just fine.

To solve this challenge, players need to provide two distinct queries that result in a hash collision
based on the custom hash algorithm in the given binary. The catch is that binary for this challenge is
actually a loader for the real program. The loader contains the encrypted program as a string in memory, and
decrypts it at run-time and writes the result to an in-memory file, which is then loaded as a dynamic libary
using `dlopen`. The hash function implementation is in the encrypted program, so to find the vulnerability
in the hashing algorithm they will need to obtain the decrypted program.

Since the main program is encrypted, static analysis will not be easy (although it is possible to solve this
challenge using only static analysis). An easier method is to run the binary in GDB and wait for it to perform
the decryption, and then dump the in-memory file using the GDB command:
`dump binary memory outfile.bin <start address> <end address>`
This file can then be analyzed in Ghidra to see the real program logic. The only function they need to reverse
is the `HASH` function. In pseduocode, `HASH` does:
```
X <- first 16 bytes of input
Y <- second 16 bytes of input
return SHA256(X XOR Y)
```
So all it comes down to is finding 2 messages where the first half and second half XOR to the same result.
In `solve.py`, we use:
- 16 `B` characters followed by 16 `\x03` characters
- 16 `C` characters followed by 16 `\x02` characters
These two messages both result in `HASH` being fed `AAAAAAAAAAAAAAAA` as input. Since SHA256 is deterministic,
it will result in a hash collision. This is just one example of colliding queries; there are many many possible
inputs that can solve this challenge.