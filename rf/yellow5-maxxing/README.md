# yellow5-maxxing 

---

### User description

I picked up another signal coming from a Bikini Bottom computer, but this time it is full of noise, it's spectrum is all spreadout. Can you help me demodulate it?

(The signal has been shifted to baseband. The signal contains an english sentence repeated several times. Enter the key as `UMASS{<some_sentence_here>}`, where everything between the angle brackets has been replaced with the lowercase version of the sentence that was transmitted. Example if `Hello_there` was transmitted the key would be `UMASS{hello_there}`).

---

### Flag

UMASS{krusty_krab_pizza_is_the_pizza_for_you_and_me}

---

### Maintainer description

This challenge is designed to be similar to `red40-maxxing` but with greatly increased noise. The modulation is similar (BPSK 1 -> 1 0 -> -1) however this time in order to compensate for the greatly increased noise, the signal uses DSSS code words (specifically a 5 bit LFSR) to increase redundancy. In this case it either inverts the DSSS sequence to send a 1 or uprights it to send a 0. The intended solution is for people to recognize that there is an autocorrelation of 33
