# Third Times the Charm

This didn't work the first two times

---

FLAG: UMASS{sunz1_su@nj1ng}

The user opens a `nc` connection and is served 6 numbers in the following form:
```
m1: 8109723817604055669986804973369824182970671326024797706691447118734058232552
N1: 34713648916861985619082341504869714777655578065122361668923489079776977192157

m2: 39132072052485017885556951726849375906969010332637060693303500998147823089096
N2: 51882251809878414349447857267510347380703063107770805951322120833783922367881

m3: 23394806392196634909383660208846135475353710086951765926729947942251364698198
N3: 76830766085319721179955513207830355395421479419364018367327799074042233474103
```
The user is statically given the source code, and there are no other static components.

We have three equations of the form
$$FLAG^3 \equiv mi \mod Ni$$
The intended solution is to take the three encrypted messages m1, m2, and m3, and solve the corresponding system of
congruences via Chinese remainder theorem. This gives value $x = FLAG^3$. We can then just take the normal cube root of
x to obtain FLAG, convert it back to bytes and print.

