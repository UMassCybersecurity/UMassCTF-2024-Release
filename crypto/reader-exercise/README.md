# reader-exercise
## User Description
Our resident math competition addict has developed this weird verification scheme, but we could only recover this source file that's missing a function that looks pretty important. Before retreating back into his math competition preparation cave, he said that breaking this scheme would be left as "an exercise for the readers", so we now need your help to retrieve the flag!
## Flag
UMASS{1n5p1r3d_6y_pu7n@m_b4_2007}

## Description
**n** is a prime congruent to 1 mod 32 given at the start. Meanwhile, **p** is a polynomial of degree 8, **q** is a polynomial of degree strictly less than 8, and both of them (along with how they are generated) are hidden. The 'challenge' option has an assertion that is guaranteed to never fail, so we're also given that **p(x)<sup>2</sup> + q(x)<sup>2</sup> = x<sup>16</sup> + 1 (mod n)**. The 'verify' option gives a randomly generated **t** along with **p(t)** and **q(t)**, then gives another randomly generated **token** and asks for **p(token)** and **q(token)**. If these matches the expected values, then the flag is given.

## Solve 
**p(x)<sup>2</sup> + q(x)<sup>2</sup> = x<sup>16</sup> + 1** actually implies **(p(x) + w<sup>8</sup>q(x))(p(x) - w<sup>8</sup>q(x)) = (x - w<sup>1</sup>)(x - w<sup>3</sup>)...(x - w<sup>31</sup>)**, where **w** is a 32<sup>nd</sup> primitive root of unity. **w** is guaranteed to exist since **n** is a prime congruent to 1 mod 32 (so **w<sup>32</sup> = 1 (mod n)**). We then get **w<sup>16</sup> = -1**, so **p(x)<sup>2</sup> + q(x)<sup>2</sup> = p(x)<sup>2</sup> - (q(x)w<sup>16</sup>)<sup>2</sup>** can be factored into **(p(x) + w<sup>8</sup>q(x))(p(x) - w<sup>8</sup>q(x))**. Meanwhile, **x<sup>16</sup> + 1** can be factored into **(x - w<sup>1</sup>)(x - w<sup>3</sup>)...(x - w<sup>31</sup>)**. This can be easily seen if we consider  **(x<sup>16</sup> + 1)(x<sup>16</sup> - 1) = x<sup>32</sup> - 1 = (x - w<sup>0</sup>)(x - w<sup>1</sup>)...(x - w<sup>31</sup>)**. Since **w<sup>2</sup>** would also be a 16<sup>th</sup> root of unity, we know that **x<sup>16</sup> - 1 = (x - w<sup>0</sup>)(x - w<sup>2</sup>)...(x - w<sup>30</sup>)**. Removing these factor, we are left with the factorization of **x<sup>16</sup> + 1**.

Next, note that both **p(x) + w<sup>8</sup>q(x)** and **p(x) - w<sup>8</sup>q(x)** are both necessarily of degree 8, since **p(x)** has degree 8 by itself, and **q(x)** has a degree strictly less than 8. This implies that each of the 2 would have 8 distinct factors from the 16 factors of **x<sup>16</sup> + 1**. Given the 8 factors of **p(x) + w<sup>8</sup>q(x)**, along with the sign of its leading term, we can completely determine **p(x)** and **q(x)**. This means that there are **2 * (16 choose 8) = 25740** possible pairs of **p** and **q**, which can easily be bruteforce over by iterating through the combinations of factors of the polynomials, then checking if the corresponding **p** and **q** from the combination gives the same result as the given **t, p(t)** and **q(t)**. Finally, plug **token** into the **p** and **q** pair found through bruteforce to get the flag.