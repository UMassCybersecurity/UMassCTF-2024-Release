# Primitive Reversing

Plankton has forgotten his password. He asked Karen to encrypt it years ago, but only has the encrypted text left over.
He managed to get his hands on the firmware's source, but it seems to be some ancient program he can't decipher...

----

FLAG: `UMASS{k0lm0g0r0v_w0uld_b3_d1s@pp01nt3d}`

`src/main.py` is used to generate a Turing machine description. DO NOT distribute, it contains the flag in plaintext.
`static/turing_machine.txt` contains the actual Turing machine description, which they must reverse.
`static/turing_machine.py` contains a class definition of a Turing machine as starter code.
