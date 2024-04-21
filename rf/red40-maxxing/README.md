# red40-maxxing 

---

### User description

I picked up this signal coming from a Bikini Bottom computer, but I have no idea what it means. Can you help me demodulate it?

(The signal has been shifted to baseband. The signal contains an english sentence repeated several times. Enter the key as `UMASS{<some_sentence_here>}`, where everything between the angle brackets has been replaced with the lowercase version of the sentence that was transmitted. Example if `Hello_there` was transmitted the key would be `UMASS{hello_there}`).

---

### Flag

UMASS{its_not_just_a_boulder_its_a_rock}

---

### Maintainer description

This challenge is designed to be an introduction to modulation detection. It uses BPSK modulation to encode the message bits as is (repeated several times). Each 1 bit becomes a 1 symbol and each 0 bit becomes a -1 symbol. A small amount of noise has been added to each symbol. They are written to a `.wav` file which can be read by many different lanugages, although Matlab is suggested for completing this challenge. The intended solution is for people to realize that the bits are separated into two different levels when plotted in time domain. From there they should interpret each sample as mentioned above to recover the bits and recover the message. The noise should be low enough that the message is obvious, however it is also repeated several times so they can do a index of coincidence analysis to determine the correct message.
