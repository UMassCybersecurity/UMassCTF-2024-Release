# shuffling-as-a-service
## User Description
We've developed a SaaS (shuffling as a service) encryption scheme. Have fun with the free trials!

## Flag
UMASS{cHu443d_2_b1t5}

## Description
The challenge pads the flag with random characters so that the flag will have 1024 bits. It then outputs the result of shuffling the flag by a random permutation. Then, it allows the user to shuffle the bits of 10 inputs with the same permutation.

## Solve 
We need to identify the position each bit gets shuffled to. Since permutation doesn't affect the values of any bits, any 1-bits in our input remains 1 in the output. Therefore, we get the set of output positions for 10 sets of input positions. The problem then becomes picking 10 sets of numbers from 0 to 1023 so that we can uniquely identify each number by their membership of the 10 sets. Since 1024 = 2<sup>10</sup>, we can choose the i<sup>th</sup> set to include all numbers whose i<sup>th</sup> bit is 0. Then, we can take the bitwise and of the outputs (or their inverses) to know where individual bits are shuffled to. Let's consider a scaled down example, where there are 4 bits and we get 2 inputs. The hidden permutation take 3210 to 0132. Every number from 0 to 3 can be written in binary as **ab**. We choose our inputs to be 0011 (*a* is 0) or 0101 (*b* lowest bit is). Then, to find out where the 2<sup>nd</sup> bit gets shuffled to, for example, we first note that 2 is 10 in binary. Equivalently, if we take 0101 and & (bitwise and) it with the inverse of 0011, we would get 0100, which is the 2<sup>nd</sup> bit. Therefore, if we take the output of 0101 & inverted output of 0011, we would get a number with a single 1-bit that is where the 2<sup>nd</sup> bit get shuffled to. In this specific example, the output for 0101 would be 1001, and the output for 0011 would be 1100, which inverted would become 0011. 1001 & 0011 gives 0001, which is the output for 0100. We can do the same for 0, 1 and 3 to recover the entire permutation. After this, we simply revert the permutation to recover the flag.