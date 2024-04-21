# yellow6-maxxing 

---

### User description

I picked up this signal coming from a Bikini Bottom computer, except this one seems like it has twice as much information as the last one. Can you help me demodulate it?

(The signal has been shifted to baseband. The signal contains an english sentence repeated several times. Enter the key as `UMASS{<some_sentence_here>}`, where everything between the angle brackets has been replaced with the lowercase version of the sentence that was transmitted. Example if `Hello_there` was transmitted the key would be `UMASS{hello_there}`).

---

### Flag

UMASS{hiiii_Kevin}

---

### Maintainer description

This challenge is designed to be similar to `yellow6-maxxing` but using QAM/QPSK instead of BPSK. The intended solution is to implement a QPSK demodulator to recover the bits. The bits can then be reassembled as expected (interleaving I and Q samples like IQIQIQ...) and converting 1 -> 1, -1 -> 0, to recover the original message. A gray code ([0 1 3 2]) was used.
