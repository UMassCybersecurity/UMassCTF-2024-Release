# 100 degrees

Mr. Krabs has been tinkering with the restaurant thermometer to see what makes his staff the most productive.
He's been tracking the data in his journal, but some "Lagrange" guy just called saying Mr. Krabs already has all the info he needs.
Can you help Mr. Krabs predict how his staff will fare?

---

FLAG: UMASS{1nt3rpr3t_n0r_1nt3rp0l@t3}'

`journal.txt` contains 101 points on a polynomial named `DAY`, and a prime value `p`, followed by a line break.
After the line break are 32 evaluations of `DAY` whose outputs are unknown.
The name "100 degrees" is meant to hint that the 101 points uniquely determine a degree 100 polynomial. 
The remaining 32 values can be acquired by interpolating the polynomial, and evaluating at each missing value.
Then, the values are to be converted from decimal to ASCII, and spell out the flag in order.
